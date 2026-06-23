"""Characterization tests for /api/v1/form-definitions* — the
authored form-definition layer that produces FHIR Questionnaires.

NOT a functional spec — these tests pin the auth gates and the broad
response shape so refactors of `app/api/form_definitions.py` or the
`form_definition_service` surface regressions in CI. Per ticket #255.
"""
from __future__ import annotations

import pytest
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


UNKNOWN_GUID = '00000000-0000-0000-0000-000000000000'


# ---------------------------------------------------------------------------
# /form-definitions — all routes are auth-gated
# ---------------------------------------------------------------------------
class TestFormDefinitionsAuth:
    """Every route on this blueprint carries @requires_role(...).
    Without an SSO session, writes return 401 and reads return 401 too
    (the listing endpoint requires read_only role at minimum)."""

    def test_list_no_auth_returns_401(self, client):
        resp = client.get('/api/v1/form-definitions')
        assert resp.status_code == 401

    def test_get_no_auth_returns_401(self, client):
        resp = client.get(f'/api/v1/form-definitions/{UNKNOWN_GUID}')
        assert resp.status_code == 401

    def test_create_no_auth_returns_401(self, client):
        resp = client.post('/api/v1/form-definitions', json={})
        assert resp.status_code == 401

    def test_update_no_auth_returns_401(self, client):
        resp = client.put(f'/api/v1/form-definitions/{UNKNOWN_GUID}', json={})
        assert resp.status_code == 401

    def test_delete_no_auth_returns_401(self, client):
        resp = client.delete(f'/api/v1/form-definitions/{UNKNOWN_GUID}')
        assert resp.status_code == 401

    def test_items_no_auth_returns_401(self, client):
        resp = client.get(f'/api/v1/form-definitions/{UNKNOWN_GUID}/items')
        assert resp.status_code == 401

    def test_add_item_no_auth_returns_401(self, client):
        resp = client.post(
            f'/api/v1/form-definitions/{UNKNOWN_GUID}/items', json={},
        )
        assert resp.status_code == 401

    def test_reorder_no_auth_returns_401(self, client):
        resp = client.post(
            f'/api/v1/form-definitions/{UNKNOWN_GUID}/reorder', json={},
        )
        assert resp.status_code == 401

    def test_produce_no_auth_returns_401(self, client):
        resp = client.post(
            f'/api/v1/form-definitions/{UNKNOWN_GUID}/produce', json={},
        )
        assert resp.status_code == 401

    def test_preview_no_auth_returns_401(self, client):
        resp = client.get(f'/api/v1/form-definitions/{UNKNOWN_GUID}/preview')
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# Authenticated path — with SSO, routes resolve (200 or 4xx but not 5xx)
# ---------------------------------------------------------------------------
class TestFormDefinitionsAuthenticated:
    def test_list_with_sso_returns_200(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get('/api/v1/form-definitions')
        assert resp.status_code == 200
        body = resp.get_json()
        # list_form_definitions returns either a list OR a dict with items;
        # both shapes are valid surface conventions in this codebase.
        assert isinstance(body, (list, dict))

    def test_get_unknown_returns_404(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get(f'/api/v1/form-definitions/{UNKNOWN_GUID}')
        assert resp.status_code == 404

    def test_create_empty_body_returns_400(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post(
            '/api/v1/form-definitions',
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_questionnaire_endpoint_resolves(self, client):
        """GET /form-definitions/<guid>/questionnaire is documented as
        'API key or SSO'. With SSO, it resolves to 4xx (unknown guid)
        rather than 5xx."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get(
            f'/api/v1/form-definitions/{UNKNOWN_GUID}/questionnaire',
        )
        assert resp.status_code < 500
