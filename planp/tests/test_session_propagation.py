"""X2 operator-session propagation (#423) — plan.pdhc adoption.

plan forwards the operator's X-Operator-Session-Id on its onward calls to
termbank.pdhc (concept lookup / search) and to contract.pdhc (dispatch match).
Self-contained (a bare Flask app for the request context) so it needs no DB.
"""
from unittest.mock import patch

from flask import Flask, session

from app.services.session_headers import (
    current_session_id,
    outbound_session_headers,
)
from app.services import termbank_client

SID = "sess-plan-1"


def _ctx_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test"
    return app


def test_helper_resolves_and_gates():
    app = _ctx_app()
    with app.test_request_context("/", headers={"X-Operator-Session-Id": SID}):
        assert current_session_id() == SID
        assert outbound_session_headers() == {"X-Operator-Session-Id": SID}
    with app.test_request_context("/"):
        assert outbound_session_headers() == {}


def test_from_session_blob_sid():
    app = _ctx_app()
    with app.test_request_context("/"):
        session["access_blob"] = {"session_id": SID}
        assert outbound_session_headers() == {"X-Operator-Session-Id": SID}


class _Resp:
    status_code = 404
    def json(self):
        return {}


def test_termbank_lookup_forwards_operator_session():
    """A concept lookup while serving an operator request carries the header."""
    tc = termbank_client.TermbankClient(base_url="http://termbank")
    seen = {}
    app = _ctx_app()
    with app.test_request_context("/", headers={"X-Operator-Session-Id": SID}):
        with patch.object(termbank_client.requests, "get",
                          side_effect=lambda *a, **kw: (seen.update(kw.get("headers") or {}), _Resp())[1]):
            tc.lookup("loinc", "4548-4")
    assert seen.get("X-Operator-Session-Id") == SID
