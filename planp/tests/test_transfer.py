"""#530 — Transfer page + proxy API (plan.pdhc triggers cdr_6's engine #529).

plan.pdhc only proxies; cdr_6's HTTP call is mocked. Auth: read_write
(planning-phase professional or SU); analysis-only is rejected.
"""
import pytest

import app.api.transfer as transfer_api
from tests.conftest import (
    set_sso_session, SAMPLE_ACCESS_BLOB, SAMPLE_READONLY_BLOB,
)


class _FakeResp:
    def __init__(self, status_code=200, body=None):
        self.status_code = status_code
        self._body = body if body is not None else {}

    def json(self):
        return self._body


@pytest.fixture
def configured(app, monkeypatch):
    monkeypatch.setitem(app.config, "CDR6_BASE_URL", "http://cdr6.test")
    monkeypatch.setitem(app.config, "CDR6_SERVICE_KEY", "sim-key")
    monkeypatch.setitem(app.config, "CDR_TRANSFER_TARGETS",
                        ["cdr1", "cdr2", "cdr3", "cdr4", "cdr5"])


@pytest.fixture
def capture(monkeypatch):
    calls = {"posts": []}

    def fake_post(url, json=None, headers=None, timeout=None):
        calls["posts"].append({"url": url, "json": json, "headers": headers})
        # Echo back a plausible cdr_6 summary.
        if json.get("dry_run"):
            return _FakeResp(200, {"mode": "dry-run", "to": json["to"],
                                   "rows": 7, "runs": ["r1", "r2"]})
        return _FakeResp(200, {"mode": "transfer", "to": json["to"], "rows": 7,
                               "accepted": 7, "duplicate": 0, "rejected": 0,
                               "verified": True, "purged": None})

    monkeypatch.setattr(transfer_api.requests, "post", fake_post)
    return calls


# --------------------------------------------------------------------------
# auth gate
# --------------------------------------------------------------------------

def test_targets_requires_auth(client, configured):
    r = client.get("/api/v1/transfer/targets")
    assert r.status_code in (401, 403)


def test_execute_forbidden_for_readonly(client, configured, capture):
    set_sso_session(client, SAMPLE_READONLY_BLOB)  # analysis only, no planning
    r = client.post("/api/v1/transfer/execute", json={"to": "cdr2"})
    assert r.status_code == 403
    assert capture["posts"] == []  # never reached cdr_6


# --------------------------------------------------------------------------
# targets
# --------------------------------------------------------------------------

def test_targets_reports_configured(client, configured):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.get("/api/v1/transfer/targets")
    assert r.status_code == 200
    b = r.get_json()
    assert b["configured"] is True
    assert b["targets"] == ["cdr1", "cdr2", "cdr3", "cdr4", "cdr5"]
    assert "cdr_6" in b["source"]


def test_targets_reports_unconfigured(client, app, monkeypatch):
    monkeypatch.setitem(app.config, "CDR6_BASE_URL", "")
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.get("/api/v1/transfer/targets")
    assert r.get_json()["configured"] is False


# --------------------------------------------------------------------------
# preview
# --------------------------------------------------------------------------

def test_preview_proxies_dry_run(client, configured, capture):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/transfer/preview",
                    json={"to": "cdr2", "sim_run_id": "run-x"})
    assert r.status_code == 200
    assert r.get_json()["rows"] == 7
    sent = capture["posts"][0]
    assert sent["url"] == "http://cdr6.test/api/v1/transfer"
    assert sent["json"] == {"to": "cdr2", "sim_run_id": "run-x", "dry_run": True}
    # cdr_6 is sim-only: we present the sim identity.
    assert sent["headers"]["X-Source-Service"] == "sim.pdhc"
    assert sent["headers"]["X-Service-Key"] == "sim-key"


def test_preview_rejects_unknown_destination(client, configured, capture):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/transfer/preview", json={"to": "cdr9"})
    assert r.status_code == 400
    assert capture["posts"] == []


def test_preview_requires_to(client, configured, capture):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/transfer/preview", json={})
    assert r.status_code == 400


# --------------------------------------------------------------------------
# execute
# --------------------------------------------------------------------------

def test_execute_proxies_real_transfer(client, configured, capture):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/transfer/execute",
                    json={"to": "cdr3", "purge_source": True, "batch_size": 50})
    assert r.status_code == 200
    b = r.get_json()
    assert b["verified"] is True and b["accepted"] == 7
    sent = capture["posts"][0]["json"]
    assert sent["to"] == "cdr3"
    assert sent["dry_run"] is False
    assert sent["purge_source"] is True
    assert sent["batch_size"] == 50


def test_execute_su_admin_allowed(client, configured, capture):
    from tests.conftest import SAMPLE_SU_BLOB
    set_sso_session(client, SAMPLE_SU_BLOB)  # SU bypasses phase check
    r = client.post("/api/v1/transfer/execute", json={"to": "cdr1"})
    assert r.status_code == 200


def test_execute_unconfigured_degrades(client, app, monkeypatch):
    monkeypatch.setitem(app.config, "CDR6_BASE_URL", "")
    monkeypatch.setitem(app.config, "CDR_TRANSFER_TARGETS", ["cdr1", "cdr2"])
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post("/api/v1/transfer/execute", json={"to": "cdr2"})
    assert r.status_code == 503
    assert r.get_json()["error"] == "cdr6_not_configured"


def test_execute_cdr6_unreachable_degrades(client, configured, monkeypatch):
    import requests as _rq
    set_sso_session(client, SAMPLE_ACCESS_BLOB)

    def boom(*a, **k):
        raise _rq.RequestException("connection refused")

    monkeypatch.setattr(transfer_api.requests, "post", boom)
    r = client.post("/api/v1/transfer/execute", json={"to": "cdr2"})
    assert r.status_code == 502
    assert r.get_json()["error"] == "cdr6_unreachable"


# --------------------------------------------------------------------------
# page
# --------------------------------------------------------------------------

def test_transfer_page_renders(client, configured):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.get("/transfer")
    assert r.status_code == 200
    assert b"Transfer synthetic data" in r.data
