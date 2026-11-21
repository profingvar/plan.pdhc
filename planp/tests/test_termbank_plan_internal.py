"""2026-11-20 — termbank is reachable ONLY from inside plan.pdhc.

plan's two termbank proxies were open, and Googlebot crawled
/api/v1/termbank/concept/<system>/<code> straight through them. They now need
a logged-in plan session, and a service key is refused even when valid.
"""
from unittest.mock import patch

import pytest

from tests.conftest import SAMPLE_READONLY_BLOB, set_sso_session

ROUTES = ("/api/v1/termbank/concept/snomed/447033006", "/api/v1/termbank/search?q=x")


@pytest.fixture()
def stubbed(app):
    with patch.object(app.termbank_client, "lookup", return_value={"ok": 1}), \
         patch.object(app.termbank_client, "search", return_value={"results": []}), \
         patch.object(type(app.termbank_client), "configured", new=True, create=True):
        yield


@pytest.mark.parametrize("path", ROUTES)
def test_anonymous_is_refused(client, stubbed, path):
    assert client.get(path).status_code == 401


@pytest.mark.parametrize("path", ROUTES)
def test_a_crawler_user_agent_changes_nothing(client, stubbed, path):
    ua = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}
    assert client.get(path, headers=ua).status_code == 401


@pytest.mark.parametrize("path", ROUTES)
def test_a_valid_service_key_is_still_refused(client, app, stubbed, path):
    from app.api.auth import KNOWN_SERVICES
    src, (cfg_var, _role) = next(iter(KNOWN_SERVICES.items()))
    app.config[cfg_var] = "k-test"
    r = client.get(path, headers={"X-Source-Service": src, "X-Service-Key": "k-test"})
    assert r.status_code == 403 and "inside plan.pdhc" in r.get_json()["error"]


@pytest.mark.parametrize("path", ROUTES)
def test_a_plan_session_gets_through(client, stubbed, path):
    set_sso_session(client, SAMPLE_READONLY_BLOB)
    assert client.get(path).status_code == 200


def test_capability_statement_no_longer_says_open(client):
    from app.api.capability import ENDPOINTS
    rows = [e for e in ENDPOINTS if "/termbank/" in e["path"]]
    assert len(rows) == 2 and all(e["auth_required"] is True for e in rows)


# --- CodeSystem/$lookup: its termbank branch was the second open door --------

@pytest.fixture()
def external_lib(app):
    from app import db
    from app.models.concept_models import CanonicalLib
    lib = CanonicalLib.query.filter_by(canonical_lib_name="snomed").first()
    if lib is None:
        lib = CanonicalLib(canonical_lib_name="snomed")
        db.session.add(lib); db.session.commit()
    return lib.canonical_lib_name


def _lookup(client, system, **kw):
    return client.get("/api/v1/CodeSystem/$lookup",
                      query_string={"system": system, "code": "447033006"}, **kw)


def test_lookup_into_termbank_is_refused_anonymously(client, app, stubbed, external_lib):
    assert _lookup(client, external_lib).status_code == 401


def test_lookup_into_termbank_refuses_a_valid_service_key(client, app, stubbed, external_lib):
    from app.api.auth import KNOWN_SERVICES
    src, (cfg_var, _role) = next(iter(KNOWN_SERVICES.items()))
    app.config[cfg_var] = "k-test"
    r = _lookup(client, external_lib, headers={"X-Source-Service": src, "X-Service-Key": "k-test"})
    assert r.status_code == 403


def test_lookup_into_termbank_works_with_a_plan_session(client, app, stubbed, external_lib):
    set_sso_session(client, SAMPLE_READONLY_BLOB)
    assert _lookup(client, external_lib).status_code == 200


def test_local_lookup_is_not_gated(client, app):
    # cdr and analyse resolve plan's OWN concept names this way, keyed or not
    # (#1011 decides plan's own reads); it never reaches termbank.
    from app.api.fhir_codesystem import LOCAL_CS_URL
    r = client.get("/api/v1/CodeSystem/$lookup",
                   query_string={"system": LOCAL_CS_URL, "code": "no-such-guid"})
    assert r.status_code == 404          # not 401: the gate did not run
