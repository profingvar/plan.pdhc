"""#872 — the adoption rule must be READABLE, and ICD-10 is decided.

Two gaps, both found by measuring rather than reading the plan document.

**The rule was not discoverable.** The semantics of
``whole_system_answer_space`` are tested in test_terminology.py and the
response has carried a ``whole_system`` boolean and an explanatory message
since #857. But measured 2026-11-01: **nothing outside this service read
that boolean** — zero readers across the whole workspace, and cdr's own
parser carried the key into a dict no code inspected. A contract nobody can
discover is a contract nobody follows, so the CapabilityStatement now states
it and these tests keep it stated.

**ICD-10 was deferred on a premise that turned out to be empty.** Migration
c3d4e5f6a7b8 left ``icd10`` FALSE because it "is also used for non-diagnosis
purposes in existing plans". Measured against production 2026-11-01: icd10
has **0 concepts and 0 values_catalog rows**. Migration d4e5f6a7b8c9 flips
it; these tests fix the semantics that flip relies on.

The migration itself cannot be tested here — this suite runs on SQLite with
``create_all`` and never applies migrations. It was applied against real
Postgres separately; see progress.md.
"""
import pytest

from app import db as _db
from app.models.concept_models import CanonicalLib, Concept


def _params(resp):
    return {p["name"]: p for p in resp.get_json()["parameter"]}


def _icd10_with_flag(app, flag: bool):
    """Set icd10's flag, yield, then put it back exactly as it was.

    The restore is not politeness. The app fixture's SQLite database is
    shared across the whole session, so a fixture that leaves the flag
    flipped changes the answer other test FILES get — which is how this was
    found: two tests in test_terminology.py went red depending on file
    order, and the leak looked like a code defect."""
    with app.app_context():
        lib = CanonicalLib.query.filter_by(canonical_lib_name="icd10").first()
        created = lib is None
        if created:
            lib = CanonicalLib(
                canonical_lib_name="icd10",
                canonical_lib_display_text="ICD-10-SE",
                canonical_lib_url="https://termbank.pdhc.se/CodeSystem/icd10",
                author="termbank.pdhc",
                whole_system_answer_space=flag,
            )
            _db.session.add(lib)
            _db.session.commit()
            before = None
        else:
            before = bool(lib.whole_system_answer_space)
            lib.whole_system_answer_space = flag
            _db.session.commit()
        guid = lib.guid
    try:
        yield guid
    finally:
        with app.app_context():
            lib = CanonicalLib.query.filter_by(canonical_lib_name="icd10").first()
            if lib is not None:
                if before is None:
                    _db.session.delete(lib)
                else:
                    lib.whole_system_answer_space = before
                _db.session.commit()


@pytest.fixture()
def icd10_lib(app):
    """ICD-10 as a CLASSIFICATION — the #872 decision."""
    yield from _icd10_with_flag(app, True)


@pytest.fixture()
def icd10_per_code(app):
    """ICD-10 as it was BEFORE #872: per-code adoption. The control."""
    yield from _icd10_with_flag(app, False)


# ---------------------------------------------------------------------------
# The decision: ICD-10-SE is a classification too
# ---------------------------------------------------------------------------

class TestIcd10IsAClassification:
    def test_an_arbitrary_ICD10_code_is_adopted(self, client, icd10_lib):
        params = _params(client.get(
            "/api/v1/ValueSet/$validate-code?system=icd10&code=E11.9"))
        assert params["result"]["valueBoolean"] is True
        assert params["ref_via"]["valueString"] == "CanonicalLib"
        assert params["whole_system"]["valueBoolean"] is True

    def test_the_SAME_code_is_refused_without_the_flag(self, client, icd10_per_code):
        """THE CONTROL. Identical request, flag off, clean no. Without this
        the test above would pass even if plan answered true for everything."""
        params = _params(client.get(
            "/api/v1/ValueSet/$validate-code?system=icd10&code=E11.9"))
        assert params["result"]["valueBoolean"] is False
        assert "not adopted" in params["message"]["valueString"]

    def test_a_registered_ICD10_concept_still_answers_PER_CODE(self, app, client,
                                                               icd10_lib):
        """Order matters and must keep mattering: Concept, then ValueCatalog,
        then the whole-system branch. A code that HAS a row still answers with
        its display and ref_guid, which is strictly more than "adopted" — so
        flipping the flag cannot degrade an existing answer."""
        with app.app_context():
            lib = CanonicalLib.query.filter_by(canonical_lib_name="icd10").one()
            concept = Concept(
                canonical_lib=lib.guid,
                canonical_refnumber="E11.9",
                concept_name="Diabetes mellitus typ 2 utan komplikationer",
            )
            _db.session.add(concept)
            _db.session.commit()
            guid = concept.guid
        try:
            params = _params(client.get(
                "/api/v1/ValueSet/$validate-code?system=icd10&code=E11.9"))
            assert params["result"]["valueBoolean"] is True
            assert params["ref_via"]["valueString"] == "Concept"
            assert "whole_system" not in params
        finally:
            # The row must go, and not only for tidiness: the fixture may
            # delete the icd10 library on teardown, and SQLite leaves foreign
            # keys unenforced by default — so an orphan Concept would survive
            # into other tests instead of failing loudly here.
            with app.app_context():
                row = Concept.query.filter_by(guid=guid).first()
                if row is not None:
                    _db.session.delete(row)
                    _db.session.commit()

    def test_an_unknown_library_is_STILL_refused(self, client, icd10_lib):
        """The flag widens one library. It does not make plan say yes to
        anything — the same guard the icd11 flip was held to."""
        params = _params(client.get(
            "/api/v1/ValueSet/$validate-code?system=icd10x&code=E11.9"))
        assert params["result"]["valueBoolean"] is False
        assert "not registered" in params["message"]["valueString"]


# ---------------------------------------------------------------------------
# Discoverability: a caller must be able to READ the rule
# ---------------------------------------------------------------------------

class TestTheRuleIsAdvertised:
    """Both surfaces, because they have different readers.

    ``/api/v1/metadata`` is the FHIR CapabilityStatement — what a FHIR
    client (cdr.pdhc included) parses. ``/api/v1/capability-statement`` is
    the human-readable index. Documenting only one leaves the other
    advertising a contract that is no longer the whole truth, which is the
    §3-of-CLAUDE.md failure mode: a stale line read as an instruction.
    """

    def _fhir_doc(self, client):
        body = client.get("/api/v1/metadata").get_json()
        resources = {r["type"]: r for r in body["rest"][0]["resource"]}
        vs = resources["ValueSet"]
        return next(op["documentation"] for op in vs["operation"]
                    if op["name"] == "validate-code")

    def _index_desc(self, client):
        body = client.get("/api/v1/capability-statement").get_json()
        hits = [e for e in body["resources"]["ValueSet"]
                if e["path"].endswith("/ValueSet/$validate-code")
                and e["method"] == "GET"]
        assert len(hits) == 1, f"expected one GET $validate-code entry, got {len(hits)}"
        return hits[0]["description"]

    def _validate_code_entry(self, client):
        """Both texts joined — a rule stated in either surface counts as
        stated, but the per-surface tests below require it in each."""
        return self._fhir_doc(client) + " || " + self._index_desc(client)

    def test_the_FHIR_capability_statement_states_it(self, client):
        doc = self._fhir_doc(client)
        assert "whole_system" in doc
        assert "ADOPTION" in doc
        assert "NOT a membership test" in doc

    def test_the_READABLE_index_states_it_too(self, client):
        desc = self._index_desc(client)
        assert "whole_system" in desc
        assert "ADOPTION" in desc

    def test_the_capability_statement_states_the_granularity(self, client):
        desc = self._validate_code_entry(client)
        assert "whole_system" in desc
        assert "ADOPTION" in desc
        assert "NOT a membership test" in desc

    def test_it_names_the_reason_not_just_the_rule(self, client):
        """A rule without its reason gets 'simplified' away by the next
        reader. The 85 000-code constraint is why the rule exists."""
        desc = self._validate_code_entry(client)
        assert "85" in desc            # ~85 000 codes
        assert "#872" in desc

    def test_it_tells_a_caller_what_to_DO(self, client):
        """The whole finding was that the boolean was on the wire and nobody
        read it. The advertisement has to say to read it."""
        desc = self._validate_code_entry(client)
        assert "Read whole_system" in desc
