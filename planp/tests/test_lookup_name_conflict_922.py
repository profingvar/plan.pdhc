"""#922 — renaming a lookup row to a taken name answers 409, not 500.

The defect, measured through the real route before the fix:

    POST /api/v1/lookup/canonical-libs {name: 'a'}   -> 201
    POST /api/v1/lookup/canonical-libs {name: 'b'}   -> 201
    PUT  /api/v1/lookup/canonical-libs/<b> {name:'a'}
      sqlalchemy.exc.IntegrityError: UNIQUE constraint failed

Unhandled, so a bare 500 with no body the caller could act on.

It is #875's shape one field over: a uniqueness guard on CREATE, none on
UPDATE, and a UNIQUE constraint underneath that turns the gap into a 500.
#875 left the asymmetry visible in the same two files — after it,
`canonical_lib_url` was guarded on all four paths and answered 409 while
`canonical_lib_name` was guarded on two and answered 500.

SCOPE, measured rather than assumed. The JSON API is a generic factory
serving SIX models, all with a UNIQUE name column, so one fix covers all
six. The HTML admin has create+edit for FOUR of them. Hence the
parametrisation below: the defect was reported for one model and existed in
ten places.

THE FIX USES THE SERVICE THE REST OF THE CODEBASE ALREADY USES.
`NameUniquenessService.validate_name_for_manual_entry` takes `exclude_guid`
and returns a message — exactly this job — and six other paths call it
(routes/concepts ×2, routes/values, routes/valuesets, api/plandefinitions
×2). `lookup_tables` rolled its own inline check on create and none on
update. So this is not a new helper; it is the exception being brought in
line, which is why the tests assert behaviour and not implementation.
"""
import uuid

import pytest

from app import db
from app.models.concept_models import (CanonicalLib, ConceptType, IntendedUse,
                                       PlanDefType, ResponseType, Unit)
from app.routes.lookup_tables import _refuse_taken_name
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _n(tag):
    """Unique per run: the app fixture is session-scoped over one sqlite file,
    so a fixed name would collide with another test's leftovers rather than
    with the row under test."""
    return f"{tag}-{uuid.uuid4()}"


#: (api path, model, name field) — every model the generic factory serves.
API = [
    ("/api/v1/lookup/canonical-libs", CanonicalLib, "canonical_lib_name"),
    ("/api/v1/lookup/concept-types", ConceptType, "concept_type_name"),
    ("/api/v1/lookup/response-types", ResponseType, "response_type_name"),
    ("/api/v1/lookup/units", Unit, "unit_name"),
    ("/api/v1/lookup/plandef-types", PlanDefType, "plandef_type_name"),
    ("/api/v1/lookup/intended-uses", IntendedUse, "intended_use_name"),
]

#: (web edit path template, model, name field) — the four with HTML admin.
WEB = [
    ("/canonical-libs/{guid}/edit", CanonicalLib, "canonical_lib_name"),
    ("/units/{guid}/edit", Unit, "unit_name"),
    ("/response-types/{guid}/edit", ResponseType, "response_type_name"),
    ("/concept-types/{guid}/edit", ConceptType, "concept_type_name"),
]


@pytest.fixture
def rows(client):
    """Create rows directly and remove them afterwards, so these tests leave
    the shared sqlite file as they found it."""
    made = []

    def make(model, field, name=None):
        item = model(guid=str(uuid.uuid4()), **{field: name or _n("n922")})
        db.session.add(item)
        db.session.commit()
        made.append(item)
        return item

    yield make
    for item in made:
        db.session.delete(db.session.merge(item))
    db.session.commit()


# ---------------------------------------------------------------------------
# The JSON API — all six models
# ---------------------------------------------------------------------------
class TestTheJsonApi:
    @pytest.mark.parametrize("path,model,field", API,
                             ids=[a[0].split('/')[-1] for a in API])
    def test_renaming_to_a_TAKEN_name_is_409(self, client, rows, path, model,
                                             field):
        taken = rows(model, field)
        mine = rows(model, field)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f"{path}/{mine.guid}",
                          json={field: getattr(taken, field)})
        assert resp.status_code != 500, (
            "this was the defect: an unhandled IntegrityError, so the caller "
            "got a bare 500 with nothing to act on")
        assert resp.status_code == 409, resp.get_json()
        assert "error" in resp.get_json()

    @pytest.mark.parametrize("path,model,field", API,
                             ids=[a[0].split('/')[-1] for a in API])
    def test_the_refusal_does_not_change_the_row(self, client, rows, path,
                                                 model, field):
        """A 409 that half-applied the rename would be worse than the 500."""
        taken = rows(model, field)
        mine = rows(model, field)
        was = getattr(mine, field)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        client.put(f"{path}/{mine.guid}", json={field: getattr(taken, field)})
        db.session.expire_all()
        assert getattr(model.query.filter_by(guid=mine.guid).first(), field) == was

    @pytest.mark.parametrize("path,model,field", API,
                             ids=[a[0].split('/')[-1] for a in API])
    def test_CONTROL_a_FREE_name_is_accepted(self, client, rows, path, model,
                                             field):
        """Without this, a route that refused every rename would pass the
        tests above."""
        mine = rows(model, field)
        fresh = _n("free922")
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f"{path}/{mine.guid}", json={field: fresh})
        assert resp.status_code == 200, resp.get_json()
        assert resp.get_json()[field] == fresh

    @pytest.mark.parametrize("path,model,field", API,
                             ids=[a[0].split('/')[-1] for a in API])
    def test_CONTROL_saving_the_SAME_name_is_not_a_self_conflict(
            self, client, rows, path, model, field):
        """The trap `exclude_guid` and the unchanged-name short-circuit both
        exist for: without them, saving a form you did not rename reports the
        row conflicting with itself."""
        mine = rows(model, field)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.put(f"{path}/{mine.guid}",
                          json={field: getattr(mine, field)})
        assert resp.status_code == 200, resp.get_json()


# ---------------------------------------------------------------------------
# The HTML admin — the four with edit routes
# ---------------------------------------------------------------------------
class TestTheHtmlAdmin:
    @pytest.mark.parametrize("tmpl,model,field", WEB,
                             ids=[w[0].split('/')[1] for w in WEB])
    def test_renaming_to_a_TAKEN_name_refuses_and_keeps_the_row(
            self, client, rows, tmpl, model, field):
        taken = rows(model, field)
        mine = rows(model, field)
        was = getattr(mine, field)
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(tmpl.format(guid=mine.guid),
                           data={field: getattr(taken, field)})
        assert resp.status_code != 500
        assert resp.status_code == 302, "it should redirect back to the form"
        db.session.expire_all()
        assert getattr(model.query.filter_by(guid=mine.guid).first(), field) == was, (
            "the rename was applied despite the refusal")

    @pytest.mark.parametrize("tmpl,model,field", WEB,
                             ids=[w[0].split('/')[1] for w in WEB])
    def test_CONTROL_a_FREE_name_goes_through(self, client, rows, tmpl, model,
                                              field):
        mine = rows(model, field)
        fresh = _n("webfree922")
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(tmpl.format(guid=mine.guid), data={field: fresh})
        assert resp.status_code == 302
        db.session.expire_all()
        assert getattr(model.query.filter_by(guid=mine.guid).first(), field) == fresh


# ---------------------------------------------------------------------------
# The shared helper
# ---------------------------------------------------------------------------
class TestTheHelper:
    def test_an_unchanged_name_short_circuits(self, client, rows):
        """It returns None WITHOUT consulting the database. Asserted by
        breaking the query: if the short-circuit is removed this raises
        instead of returning None, which is a sharper signal than a bool."""
        item = rows(CanonicalLib, "canonical_lib_name")

        class _Boom:
            def filter(self, *a, **k):
                raise AssertionError("queried the database for an unchanged name")

        assert _refuse_taken_name(
            item.canonical_lib_name, type("M", (), {"query": _Boom()}),
            "canonical_lib_name", item, "lookup_web.edit_canonical_lib") is None

    def test_a_free_name_returns_None(self, client, rows):
        item = rows(CanonicalLib, "canonical_lib_name")
        assert _refuse_taken_name(_n("helperfree"), CanonicalLib,
                                  "canonical_lib_name", item,
                                  "lookup_web.edit_canonical_lib") is None

    def test_a_taken_name_returns_a_redirect(self, app, client, rows):
        """Needs a request context: the refusal path calls `flash()`, which
        writes to the session. Calling the helper bare raises "Working
        outside of request context" — which is the test being wrong, not the
        helper, and is why the two passing cases above return before the
        flash."""
        taken = rows(CanonicalLib, "canonical_lib_name")
        item = rows(CanonicalLib, "canonical_lib_name")
        with app.test_request_context():
            got = _refuse_taken_name(taken.canonical_lib_name, CanonicalLib,
                                     "canonical_lib_name", item,
                                     "lookup_web.edit_canonical_lib")
        assert got is not None
        assert got.status_code == 302


# ---------------------------------------------------------------------------
# The asymmetry #922 was filed about
# ---------------------------------------------------------------------------
class TestTheAsymmetryIsGone:
    def test_name_and_url_both_answer_409_on_the_same_route(self, client,
                                                            rows):
        """After #875, `canonical_lib_url` was guarded on all four paths and
        answered 409 while `canonical_lib_name` was guarded on two and
        answered 500. A reader of lookup_tables.py saw the URL check beside
        an unguarded name assignment and would reasonably assume the name was
        handled elsewhere. Both now answer the same way, on the same route."""
        a = rows(CanonicalLib, "canonical_lib_name")
        a.canonical_lib_url = f"https://example.invalid/{_n('u')}"
        db.session.commit()
        mine = rows(CanonicalLib, "canonical_lib_name")
        set_sso_session(client, SAMPLE_ACCESS_BLOB)

        by_name = client.put(f"/api/v1/lookup/canonical-libs/{mine.guid}",
                             json={"canonical_lib_name": a.canonical_lib_name})
        by_url = client.put(f"/api/v1/lookup/canonical-libs/{mine.guid}",
                            json={"canonical_lib_url": a.canonical_lib_url})
        assert (by_name.status_code, by_url.status_code) == (409, 409), (
            f"name={by_name.status_code} url={by_url.status_code}")
