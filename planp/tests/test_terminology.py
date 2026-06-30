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
