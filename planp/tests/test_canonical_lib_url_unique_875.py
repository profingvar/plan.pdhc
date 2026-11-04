"""#875 — `canonical_lib_url` is unique, and the resolver refuses to guess.

The defect, measured in production: `icd10` held a copy of `snomed`'s URL,
`resolve_canonical_lib` queried that column with `.first()`, and the two
libraries collapsed into one. `.first()` returned `snomed` by row order, so
every `icd10` value was skipped by `scoped_validate_code` — `$validate-code`
answered FALSE for 89 correctly-stored codes — and `_build_compose`, which
groups by the same column, SERVED those ICD-10 codes under the SNOMED CT
system URI.

What makes it worth a test file rather than a one-line fix is the failure
mode: it answered CONFIDENTLY with the wrong library, and nothing in the
response said "ambiguous". Four layers now stand against a recurrence, and
each is tested here:

  1. a UNIQUE constraint on the column
  2. `normalise_lib_url`, so `''` becomes NULL and blank-URL libraries do
     not collide with each other under that constraint
  3. all four write paths checking before they write
  4. the resolver RAISING if it ever sees two rows anyway

Layer 4 looks redundant against layer 1 and is not: a constraint can be
absent in an older deployment, in a database built from a stale model, or
after someone drops it. A guard whose only job is to be unreachable still
has to exist, or the next duplicate is silent again.
"""
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from app.api.fhir_valueset import AmbiguousCanonicalLib, resolve_canonical_lib
from app.models.concept_models import CanonicalLib
from app.services.canonical_libs import normalise_lib_url, url_conflict
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _u(tag):
    """A unique suffix. The app fixture is session-scoped over one sqlite
    file, so a fixed name or URL here would collide with another test's
    leftovers rather than with the thing under test."""
    return f"{tag}-{uuid.uuid4()}"


@pytest.fixture
def lib_factory(client):
    """Create libraries and remove them afterwards, so the injectivity test
    below sees the database it expects rather than this file's debris."""
    made = []

    def make(url=None, name=None):
        item = CanonicalLib(
            # A REAL uuid: the JSON API runs `_is_valid_uuid(guid)` before it
            # looks a row up, so a decorated guid like 'cl-<uuid>' (which
            # other test files use for rows the API never fetches) 400s here.
            guid=str(uuid.uuid4()),
            canonical_lib_name=name or _u("lib875"),
            canonical_lib_url=url,
        )
        db.session.add(item)
        db.session.commit()
        made.append(item)
        return item

    yield make
    for item in made:
        db.session.delete(db.session.merge(item))
    db.session.commit()


# ---------------------------------------------------------------------------
# 1. the constraint
# ---------------------------------------------------------------------------
class TestTheConstraint:
    def test_a_second_library_cannot_claim_the_same_url(self, lib_factory):
        url = f"https://example.invalid/{_u('cs')}"
        lib_factory(url=url)
        with pytest.raises(IntegrityError):
            lib_factory(url=url)
        db.session.rollback()

    def test_CONTROL_a_different_url_is_accepted(self, lib_factory):
        """Without this, a model that rejected every insert would pass the
        test above."""
        lib_factory(url=f"https://example.invalid/{_u('a')}")
        lib_factory(url=f"https://example.invalid/{_u('b')}")

    def test_MANY_libraries_may_have_NO_url(self, lib_factory):
        """Nullable AND unique is the design, not an oversight: Postgres (and
        sqlite) permit many NULLs under a UNIQUE. A library without a URL is
        not in conflict with another library without one."""
        lib_factory(url=None)
        lib_factory(url=None)
        lib_factory(url=None)
        assert CanonicalLib.query.filter_by(canonical_lib_url=None).count() >= 3


# ---------------------------------------------------------------------------
# 2. '' is not a URL
# ---------------------------------------------------------------------------
class TestBlankIsNotAUrl:
    @pytest.mark.parametrize("raw", ["", "   ", "\t", None])
    def test_blank_becomes_None(self, raw):
        assert normalise_lib_url(raw) is None

    def test_CONTROL_a_real_value_passes_through_stripped(self):
        assert normalise_lib_url("  https://x.invalid/cs  ") == "https://x.invalid/cs"

    def test_this_is_what_lets_two_blank_libraries_coexist(self, lib_factory):
        """The load-bearing case. Two empty STRINGS collide under a UNIQUE
        where two NULLs do not, so without the normalisation the second
        library saved with a blank URL field would be refused as conflicting
        with the first — wrong, and baffling to whoever hit it."""
        lib_factory(url=normalise_lib_url(""))
        lib_factory(url=normalise_lib_url("   "))
        # no IntegrityError

    def test_url_conflict_treats_blank_as_no_url(self, lib_factory):
        lib_factory(url=None)
        assert url_conflict(None) is None
        assert url_conflict("") is None


# ---------------------------------------------------------------------------
# 3. the write paths
# ---------------------------------------------------------------------------
class TestTheWritePaths:
    def test_api_create_refuses_a_taken_url_with_409(self, client, lib_factory):
        url = f"https://example.invalid/{_u('api-create')}"
        taken = lib_factory(url=url)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/lookup/canonical-libs', json={
            'canonical_lib_name': _u('clash'),
            'canonical_lib_url': url,
        })
        assert resp.status_code == 409, resp.get_json()
        # the message must NAME the holder; "conflict" alone is not actionable
        assert taken.canonical_lib_name in resp.get_json()['error']

    def test_api_update_refuses_a_taken_url_with_409(self, client, lib_factory):
        url = f"https://example.invalid/{_u('api-update')}"
        lib_factory(url=url)
        mine = lib_factory(url=f"https://example.invalid/{_u('mine')}")
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f'/api/v1/lookup/canonical-libs/{mine.guid}',
                          json={'canonical_lib_url': url})
        assert resp.status_code == 409, resp.get_json()

    def test_CONTROL_updating_a_row_to_its_OWN_url_is_not_a_conflict(
            self, client, lib_factory):
        """`exclude_guid` exists for this. Without it every save of an
        unchanged URL would report the row conflicting with itself, and the
        409 above would prove nothing about conflicts."""
        url = f"https://example.invalid/{_u('self')}"
        mine = lib_factory(url=url)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f'/api/v1/lookup/canonical-libs/{mine.guid}',
                          json={'canonical_lib_url': url})
        assert resp.status_code == 200, resp.get_json()

    def test_api_create_normalises_a_blank_url_to_null(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/lookup/canonical-libs', json={
            'canonical_lib_name': _u('blank-url'),
            'canonical_lib_url': '   ',
        })
        assert resp.status_code == 201, resp.get_json()
        assert resp.get_json()['canonical_lib_url'] is None
        client.delete(f"/api/v1/lookup/canonical-libs/{resp.get_json()['guid']}")


# ---------------------------------------------------------------------------
# 4. the resolver
# ---------------------------------------------------------------------------
class TestTheResolver:
    def test_it_is_INJECTIVE_over_every_library_in_the_database(
            self, client, lib_factory):
        """#875 step 4. For every library that has a URL, resolving that URL
        must return THAT library — not merely some library.

        With the constraint in place this is close to tautological, which is
        the point: the property is now structural rather than a thing to hope
        for. Before the constraint it was false in production for two of nine
        rows.

        The rows are seeded HERE rather than read from whatever the database
        happens to hold. The first version did the latter and failed with
        "no library has a URL", because it ran after the fixtures that made
        them had torn down — a test whose outcome depends on execution order
        is not evidence. The shapes mirror production's nine: a termbank URL,
        an external authority, plan itself, and a query-string URL.
        """
        seeded = [
            lib_factory(url=f"https://termbank.pdhc.se/CodeSystem/{_u('t')}"),
            lib_factory(url=f"https://www.whocc.no/{_u('w')}"),
            lib_factory(url=f"https://plan.pdhc.se/{_u('p')}"),
            lib_factory(url=f"https://browser.invalid/?id={_u('q')}&x=1"),
            lib_factory(url=None),          # must not break the sweep
        ]
        assert sum(1 for l in seeded if l.canonical_lib_url) == 4
        libs = [l for l in CanonicalLib.query.all() if l.canonical_lib_url]
        assert libs, "no library has a URL — this test would prove nothing"
        for l in libs:
            got = resolve_canonical_lib(l.canonical_lib_url)
            assert got is not None, f"{l.canonical_lib_name} unresolvable by URL"
            assert got.guid == l.guid, (
                f"resolving {l.canonical_lib_name}'s URL returned "
                f"{got.canonical_lib_name}")

    def test_it_is_injective_by_NAME_too(self, client):
        for l in CanonicalLib.query.all():
            got = resolve_canonical_lib(l.canonical_lib_name)
            assert got is not None and got.guid == l.guid

    def test_an_unknown_system_resolves_to_None_not_to_something(self):
        assert resolve_canonical_lib(f"https://nope.invalid/{uuid.uuid4()}") is None

    def test_empty_resolves_to_None(self):
        assert resolve_canonical_lib("") is None
        assert resolve_canonical_lib(None) is None

    def test_it_RAISES_rather_than_guessing_when_two_rows_match(
            self, client, monkeypatch):
        """Layer 4, and note what this test cannot do.

        The ambiguous state is now unreachable through the database — the
        UNIQUE constraint is exactly what these tests assert above. So the
        two rows are injected at the query boundary instead. That is honest
        about what is being tested: not "can the database hold this" (it
        cannot), but "if the resolver is ever handed it, does it refuse or
        does it pick".

        Picking is the #875 defect. `.first()` picked, silently, and the
        wrong library was then used for a membership check and for a FHIR
        `compose.include[].system`.
        """
        a = CanonicalLib(guid=_u("cl"), canonical_lib_name="zz-dup-a",
                         canonical_lib_url="https://dup.invalid/cs")
        b = CanonicalLib(guid=_u("cl"), canonical_lib_name="zz-dup-b",
                         canonical_lib_url="https://dup.invalid/cs")

        class _Q:
            def filter_by(self, **kw):
                self._kw = kw
                return self

            def all(self):
                if self._kw.get("canonical_lib_url") == "https://dup.invalid/cs":
                    return [a, b]
                return []

        monkeypatch.setattr(CanonicalLib, "query", _Q())
        with pytest.raises(AmbiguousCanonicalLib) as exc:
            resolve_canonical_lib("https://dup.invalid/cs")
        # The message must name BOTH, because the old behaviour named neither
        assert "zz-dup-a" in str(exc.value) and "zz-dup-b" in str(exc.value)
        assert exc.value.field == "canonical_lib_url"

    def test_CONTROL_with_one_row_it_returns_rather_than_raising(
            self, client, monkeypatch):
        """Without this, a resolver that raised unconditionally would pass
        the test above."""
        only = CanonicalLib(guid=_u("cl"), canonical_lib_name="zz-single",
                            canonical_lib_url="https://single.invalid/cs")

        class _Q:
            def filter_by(self, **kw):
                self._kw = kw
                return self

            def all(self):
                if self._kw.get("canonical_lib_url") == "https://single.invalid/cs":
                    return [only]
                return []

        monkeypatch.setattr(CanonicalLib, "query", _Q())
        assert resolve_canonical_lib("https://single.invalid/cs") is only


# ---------------------------------------------------------------------------
# 5. the twin resolver is gone, not fixed twice
# ---------------------------------------------------------------------------
class TestThereIsOnlyOneResolver:
    def test_conceptmap_uses_the_same_function_object(self):
        """`fhir_conceptmap` carried a byte-identical copy whose docstring
        said it "mirrors the lenience of" the original. It mirrored the
        defect too. Asserting identity of the function OBJECT is what makes
        a future re-divergence fail here instead of in production."""
        from app.api import fhir_conceptmap, fhir_valueset
        assert (fhir_conceptmap._resolve_lib_for_input
                is fhir_valueset.resolve_canonical_lib)

    def test_codesystem_uses_it_too(self):
        from app.api import fhir_codesystem, fhir_valueset
        assert (fhir_codesystem.resolve_canonical_lib
                is fhir_valueset.resolve_canonical_lib)


# ---------------------------------------------------------------------------
# 6. the refusal reaches the caller as FHIR, not as a 500
# ---------------------------------------------------------------------------
class TestTheRefusalIsAnswerable:
    def test_the_errorhandler_is_registered_and_returns_409(self, app):
        """A raise nobody handles is a bare 500 with no OperationOutcome,
        which tells a machine caller nothing. Registered on the app rather
        than at each call site, because #875's whole lesson is that the
        resolver existed in two places and one was forgotten."""
        from app.api.fhir_valueset import AmbiguousCanonicalLib as Exc
        handler = app.error_handler_spec[None][None].get(Exc)
        assert handler is not None, (
            "no app-level handler for AmbiguousCanonicalLib — the refusal "
            "would surface as a 500 with no FHIR body")
        with app.test_request_context():
            resp, status = handler(Exc("canonical_lib_url", "u", ["a", "b"]))
        assert status == 409
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'
        assert 'a' in body['issue'][0]['details']['text']
