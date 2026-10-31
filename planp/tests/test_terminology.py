"""Phase 0.2 — terminology API + termbank client tests.

Covers:
  - $validate-code endpoint (Concept ref / ValueCatalog ref / no ref / unknown system)
  - termbank-concept proxy (success / miss / unreachable)
  - termbank-search proxy
  - TermbankClient direct unit tests (cache, error paths)
"""
from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest
import requests

from app import db as _db
from app.models.concept_models import (
    CanonicalLib,
    Concept,
    ConceptType,
    ResponseType,
    Unit,
    ValueCatalog,
)
from app.services.termbank_client import TermbankClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def seeded_libs(app):
    """Insert the 5 canonical_libs that the production migration would seed."""
    with app.app_context():
        names = [
            ("loinc", "LOINC", "https://termbank.pdhc.se/CodeSystem/loinc"),
            ("socialstyrelsen", "Socialstyrelsens termbank",
             "https://termbank.pdhc.se/CodeSystem/socialstyrelsen"),
            ("icd10", "ICD-10-SE",
             "https://termbank.pdhc.se/CodeSystem/icd10"),
            ("atc", "ATC",
             "https://termbank.pdhc.se/CodeSystem/atc"),
            ("snomed", "SNOMED CT (SE)",
             "https://termbank.pdhc.se/CodeSystem/snomed"),
        ]
        out = {}
        for name, display, url in names:
            existing = CanonicalLib.query.filter_by(
                canonical_lib_name=name
            ).first()
            if existing is None:
                lib = CanonicalLib(
                    canonical_lib_name=name,
                    canonical_lib_display_text=display,
                    canonical_lib_url=url,
                    author="termbank.pdhc",
                )
                _db.session.add(lib)
                _db.session.flush()
                out[name] = lib.guid
            else:
                out[name] = existing.guid
        _db.session.commit()
        yield out


@pytest.fixture()
def hba1c_concept(app, seeded_libs):
    """Insert a Concept(loinc, 4548-4) for $validate-code positive tests."""
    with app.app_context():
        # ConceptType + ResponseType + Unit may not exist by default in test DB;
        # only canonical_lib is NOT NULL on Concept.
        c = Concept(
            canonical_lib=seeded_libs["loinc"],
            canonical_refnumber="4548-4",
            concept_name="HbA1c",
            concept_display_text="Hemoglobin A1c/Hemoglobin.total in Blood",
        )
        _db.session.add(c)
        _db.session.commit()
        yield c.guid


@pytest.fixture()
def diabetes_value(app, seeded_libs):
    """Insert a ValueCatalog row referencing SNOMED 44054006 (Diabetes type 2)."""
    with app.app_context():
        v = ValueCatalog(
            canonical_lib=seeded_libs["snomed"],
            canonical_refnumber="44054006",
            value_name="Diabetes mellitus type 2",
            value_display_text="diabetes mellitus typ 2",
        )
        _db.session.add(v)
        _db.session.commit()
        yield v.guid


@pytest.fixture()
def icd11_lib(app):
    """A CLASSIFICATION library: answer space is the whole code system."""
    with app.app_context():
        lib = CanonicalLib.query.filter_by(
            canonical_lib_name="icd11-mms").first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name="icd11-mms",
                canonical_lib_display_text="ICD-11 MMS (WHO)",
                canonical_lib_url="https://termbank.pdhc.se/CodeSystem/icd11-mms",
                author="termbank.pdhc",
                whole_system_answer_space=True,
            )
            _db.session.add(lib)
        else:
            lib.whole_system_answer_space = True
        _db.session.commit()
        yield lib.guid


# ---------------------------------------------------------------------------
# $validate-code
# ---------------------------------------------------------------------------
class TestValidateCode:
    def test_true_when_concept_references(self, client, hba1c_concept):
        resp = client.get("/api/v1/ValueSet/$validate-code?system=loinc&code=4548-4")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["resourceType"] == "Parameters"
        params = {p["name"]: p for p in body["parameter"]}
        assert params["result"]["valueBoolean"] is True
        assert params["ref_via"]["valueString"] == "Concept"
        assert params["display"]["valueString"] == "HbA1c"

    def test_true_when_only_value_references(self, client, diabetes_value):
        resp = client.get("/api/v1/ValueSet/$validate-code?system=snomed&code=44054006")
        assert resp.status_code == 200
        params = {p["name"]: p for p in resp.get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True
        assert params["ref_via"]["valueString"] == "ValueCatalog"

    def test_false_when_no_reference(self, client, seeded_libs):
        # System exists, but no Concept/ValueCatalog references this code.
        resp = client.get("/api/v1/ValueSet/$validate-code?system=loinc&code=NOPE-1")
        assert resp.status_code == 200
        params = {p["name"]: p for p in resp.get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is False
        assert "not adopted" in params["message"]["valueString"]

    def test_false_when_unknown_system(self, client):
        resp = client.get("/api/v1/ValueSet/$validate-code?system=fakelib&code=x")
        assert resp.status_code == 200
        params = {p["name"]: p for p in resp.get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is False
        assert "not registered" in params["message"]["valueString"]

    # -- a CLASSIFICATION declares adoption at system granularity -----------
    # Measured 2026-10-21 from icd11.pdhc's first live Condition projection:
    # an ICD-11 diagnosis is chosen from ~85 000 codes at the point of care, so
    # no per-code row can be pre-populated and cdr.pdhc rejected every
    # projected Condition with plan_miss.
    def test_true_for_ANY_code_in_a_whole_system_library(self, client, icd11_lib):
        resp = client.get(
            "/api/v1/ValueSet/$validate-code?system=icd11-mms&code=1A00")
        assert resp.status_code == 200
        params = {p["name"]: p for p in resp.get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True
        assert params["ref_via"]["valueString"] == "CanonicalLib"
        assert params["whole_system"]["valueBoolean"] is True

    def test_a_code_never_seen_before_is_still_adopted(self, client, icd11_lib):
        # The actual requirement. A clinician may record a code nobody has
        # registered anywhere, and that must not be a write rejection.
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code"
            "?system=icd11-mms&code=ZZ99.ZZ").get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True

    def test_a_postcoordinated_cluster_code_is_adopted(self, client, icd11_lib):
        # cdr splits the termbank canonical, so the code it sends can be a stem
        # or a cluster expression. Neither can be enumerated in advance.
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code"
            "?system=icd11-mms&code=1A00%26XN62R").get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True

    def test_an_UNKNOWN_library_is_still_refused(self, client, icd11_lib):
        # The guard that keeps this from being a loosening of the gate: the
        # flag widens one library, it does not make plan answer yes to anything.
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code?system=notalib&code=1A00"
        ).get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is False
        assert "not registered" in params["message"]["valueString"]

    def test_per_code_libraries_are_UNCHANGED(self, client, icd11_lib, seeded_libs):
        # loinc has no whole_system flag, so an unreferenced code is still a
        # clean "no". Every existing library must behave exactly as before.
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code?system=loinc&code=NOPE-1"
        ).get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is False
        assert "not adopted" in params["message"]["valueString"]

    def test_a_real_Concept_still_WINS_over_the_system_answer(
            self, client, app, icd11_lib):
        # Ordering matters: a per-code row carries a display and a ref_guid,
        # which is strictly more information than "the system is adopted". The
        # whole-system branch is the fallback, not the first answer.
        with app.app_context():
            _db.session.add(Concept(
                canonical_lib=icd11_lib,
                canonical_refnumber="5A11",
                concept_name="Diabetes mellitus typ 2",
            ))
            _db.session.commit()
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code?system=icd11-mms&code=5A11"
        ).get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True
        assert params["ref_via"]["valueString"] == "Concept"
        assert params["display"]["valueString"] == "Diabetes mellitus typ 2"
        assert "whole_system" not in params

    # -- #857: the answer is ADOPTION, and must not read as existence --------

    def test_the_message_says_it_is_NOT_a_membership_test(self, client, icd11_lib):
        """The compensating control, since there is no technical one.

        A whole_system TRUE answer is correct and was ratified, but it MOVES
        the per-code existence check onto icd11.pdhc's WHO validation at entry
        rather than removing it. Nothing downstream enforces that: cdr's
        KNOWN_FHIR_SERVICES gates FHIR writes as well as reads (#760), so a
        caller beside the designed path could POST a Condition with a
        fabricated icd11-mms code and plan would assent.

        Until #857 option (a) lands, the message IS the control — so it is
        pinned here rather than left to survive the next edit on goodwill.
        """
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code"
            "?system=icd11-mms&code=ZZ-nonsense").get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True
        msg = params["message"]["valueString"]
        assert "NOT a membership test" in msg
        assert "does not assert" in msg
        assert "icd11.pdhc" in msg          # who DOES check existence
        assert "#857" in msg                # where to read why

    def test_a_MEASUREMENT_library_message_is_unchanged(self, client, seeded_libs):
        """The control. The new wording must not leak onto the per-code path,
        where a False answer really is a membership result."""
        params = {p["name"]: p for p in client.get(
            "/api/v1/ValueSet/$validate-code"
            "?system=icd10&code=A00.9").get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is False
        assert "membership" not in params["message"]["valueString"]

    def test_icd10_is_deliberately_NOT_whole_system(self, client, seeded_libs):
        # An ICD-10-SE *diagnosis* has the same mismatch, but icd10 is also used
        # for non-diagnosis purposes in existing plans, so flipping it is a
        # separate editorial decision. Pinned so it cannot drift silently.
        with_lib = CanonicalLib.query.filter_by(canonical_lib_name="icd10").first()
        assert bool(with_lib.whole_system_answer_space) is False

    def test_missing_params_400(self, client):
        resp = client.get("/api/v1/ValueSet/$validate-code")
        assert resp.status_code == 400
        body = resp.get_json()
        assert body["resourceType"] == "OperationOutcome"
        assert body["issue"][0]["code"] == "required"

    def test_only_code_missing_400(self, client):
        resp = client.get("/api/v1/ValueSet/$validate-code?system=loinc")
        assert resp.status_code == 400

    def test_escaped_dollar_sign(self, client, hba1c_concept):
        resp = client.get("/api/v1/ValueSet/%24validate-code?system=loinc&code=4548-4")
        assert resp.status_code == 200
        params = {p["name"]: p for p in resp.get_json()["parameter"]}
        assert params["result"]["valueBoolean"] is True


# ---------------------------------------------------------------------------
# /termbank/concept/<system>/<code> proxy
# ---------------------------------------------------------------------------
class TestTermbankConceptProxy:
    def test_success_returns_termbank_payload(self, client, app):
        fake_body = {
            "resourceType": "Parameters",
            "parameter": [{"name": "display", "valueString": "HbA1c"}],
        }
        with patch.object(app.termbank_client, "lookup", return_value=fake_body):
            resp = client.get("/api/v1/termbank/concept/loinc/4548-4")
        assert resp.status_code == 200
        assert resp.get_json() == fake_body

    def test_404_on_miss(self, client, app):
        with patch.object(app.termbank_client, "lookup", return_value=None):
            resp = client.get("/api/v1/termbank/concept/loinc/NOPE")
        assert resp.status_code == 404
        body = resp.get_json()
        assert body["resourceType"] == "OperationOutcome"

    def test_handles_dotted_codes(self, client, app):
        """ICD codes like E11.0A include a dot — <path:> converter must accept it."""
        with patch.object(
            app.termbank_client, "lookup", return_value={"resourceType": "Parameters"}
        ):
            resp = client.get("/api/v1/termbank/concept/icd10/E11.0A")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# /termbank/search proxy
# ---------------------------------------------------------------------------
class TestTermbankSearchProxy:
    def test_success_passes_through(self, client, app):
        fake = {
            "query": "metformin",
            "system": None,
            "count": 2,
            "results": [
                {"canonical_uri": "...A10BA02", "code": "A10BA02",
                 "display": "Metformin", "system": "atc", "status": "active",
                 "version": "sensl-v2"},
                {"canonical_uri": "...QA10BA02", "code": "QA10BA02",
                 "display": "Metformin", "system": "atc", "status": "active",
                 "version": "sensl-v2"},
            ],
        }
        with patch.object(app.termbank_client, "search", return_value=fake) as m:
            resp = client.get("/api/v1/termbank/search?q=metformin&limit=5")
        assert resp.status_code == 200
        assert resp.get_json() == fake
        m.assert_called_once_with("metformin", system=None, limit=5)

    def test_filters_by_system(self, client, app):
        with patch.object(
            app.termbank_client, "search", return_value={"results": []}
        ) as m:
            resp = client.get("/api/v1/termbank/search?q=diabetes&system=snomed&limit=3")
        assert resp.status_code == 200
        m.assert_called_once_with("diabetes", system="snomed", limit=3)

    def test_clamps_limit(self, client, app):
        with patch.object(
            app.termbank_client, "search", return_value={"results": []}
        ) as m:
            client.get("/api/v1/termbank/search?q=x&limit=99999")
        # Implementation caps to 200
        assert m.call_args.kwargs["limit"] == 200

    def test_invalid_limit_falls_back(self, client, app):
        with patch.object(
            app.termbank_client, "search", return_value={"results": []}
        ) as m:
            client.get("/api/v1/termbank/search?q=x&limit=garbage")
        assert m.call_args.kwargs["limit"] == 20


# ---------------------------------------------------------------------------
# TermbankClient direct unit tests
# ---------------------------------------------------------------------------
class TestTermbankClientUnit:
    def test_lookup_caches_within_ttl(self):
        c = TermbankClient(base_url="https://t.example", cache_ttl=60)
        body = {"resourceType": "Parameters", "parameter": []}
        with patch("requests.get") as gm:
            gm.return_value = MagicMock(status_code=200, json=lambda: body)
            r1 = c.lookup("loinc", "4548-4")
            r2 = c.lookup("loinc", "4548-4")
        assert r1 == r2 == body
        assert gm.call_count == 1  # second call hit the cache

    def test_lookup_404_returns_none_and_caches_miss(self):
        c = TermbankClient(base_url="https://t.example", cache_ttl=60)
        with patch("requests.get") as gm:
            gm.return_value = MagicMock(status_code=404)
            r1 = c.lookup("loinc", "NOPE")
            r2 = c.lookup("loinc", "NOPE")
        assert r1 is None and r2 is None
        # The miss is also cached (one HTTP call total)
        assert gm.call_count == 1

    def test_lookup_unreachable_returns_none(self):
        c = TermbankClient(base_url="https://t.example")
        with patch("requests.get", side_effect=requests.RequestException("boom")):
            r = c.lookup("loinc", "4548-4")
        assert r is None

    def test_search_unreachable_returns_error_dict(self):
        c = TermbankClient(base_url="https://t.example")
        with patch("requests.get", side_effect=requests.ConnectionError("boom")):
            r = c.search("metformin")
        assert r["error"] == "unreachable"
        assert r["results"] == []

    def test_search_timeout_returns_timeout_error_dict(self):
        c = TermbankClient(base_url="https://t.example")
        with patch("requests.get", side_effect=requests.Timeout("too slow")):
            r = c.search("metformin")
        assert r["error"] == "timeout"
        assert r["results"] == []

    def test_search_other_request_error_returns_request_error(self):
        c = TermbankClient(base_url="https://t.example")
        # Bare RequestException — not Timeout, not ConnectionError; catches
        # SSL errors, chunked-encoding errors, malformed URLs in flight, etc.
        with patch("requests.get", side_effect=requests.RequestException("?")):
            r = c.search("metformin")
        assert r["error"] == "request_error"
        assert r["results"] == []

    def test_search_empty_query_short_circuits(self):
        c = TermbankClient(base_url="https://t.example")
        with patch("requests.get") as gm:
            r = c.search("   ")
        assert r["count"] == 0
        assert r["results"] == []
        gm.assert_not_called()

    def test_search_non_200_returns_error(self):
        c = TermbankClient(base_url="https://t.example")
        with patch("requests.get") as gm:
            gm.return_value = MagicMock(status_code=503)
            r = c.search("x")
        assert r["error"] == "http_503"
        assert r["results"] == []

    def test_clear_cache_drops_entries(self):
        c = TermbankClient(base_url="https://t.example", cache_ttl=60)
        body = {"x": 1}
        with patch("requests.get") as gm:
            gm.return_value = MagicMock(status_code=200, json=lambda: body)
            c.lookup("loinc", "X")
            c.clear_cache()
            c.lookup("loinc", "X")
        assert gm.call_count == 2
