"""Characterization tests for /api/v1/forms* — the FHIR Questionnaire
catalogue + produce/publish endpoints.

NOT a functional spec — these tests pin the auth gates and the broad
response shape so refactors of `app/api/forms.py` or the
`forms_service` modules surface regressions in CI. Per ticket #255.
"""
from __future__ import annotations

import pytest
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


# ---------------------------------------------------------------------------
# /forms — public catalogue and read
# ---------------------------------------------------------------------------
class TestFormsCatalogue:
    def test_list_forms_is_public(self, client):
        """No auth required — drives the form-picker on builder UIs."""
        resp = client.get('/api/v1/forms')
        assert resp.status_code == 200
        body = resp.get_json()
        # get_form_catalogue() returns a dict; the exact field set is
        # an implementation detail. Pin the type.
        assert isinstance(body, dict)

    def test_list_forms_accepts_filters(self, client):
        """The 'status', 'limit', 'offset', 'include_archived' params
        are explicitly handled — pin that the route accepts them."""
        resp = client.get(
            '/api/v1/forms?status=active&limit=10&offset=0&include_archived=1',
        )
        assert resp.status_code == 200

    def test_get_unknown_form_returns_4xx(self, client):
        """get_form_definition() raises DefinitionError for unknown ids
        and the route translates to a 4xx with an 'error' message."""
        resp = client.get(
            '/api/v1/forms/00000000-0000-0000-0000-000000000000',
        )
        assert 400 <= resp.status_code < 500
        body = resp.get_json()
        # Error body uses the conventional {error, message} shape.
        assert 'error' in body or 'message' in body


# ---------------------------------------------------------------------------
# /forms/<guid>/versions — public version-history read
# ---------------------------------------------------------------------------
class TestFormVersions:
    def test_versions_endpoint_exists(self, client):
        resp = client.get(
            '/api/v1/forms/00000000-0000-0000-0000-000000000000/versions',
        )
        # Unknown form -> 4xx; the route resolves and doesn't 5xx.
        assert resp.status_code != 404 or resp.is_json
        assert resp.status_code < 500


# ---------------------------------------------------------------------------
# /forms/produce, /forms/<guid>/publish — require auth
# ---------------------------------------------------------------------------
class TestFormsWriteAuth:
    def test_produce_no_auth_returns_401_or_403(self, client):
        resp = client.post('/api/v1/forms/produce', json={})
        assert resp.status_code in (401, 403)

    def test_publish_no_auth_returns_401_or_403(self, client):
        resp = client.post(
            '/api/v1/forms/00000000-0000-0000-0000-000000000000/publish',
            json={},
        )
        assert resp.status_code in (401, 403)


# ---------------------------------------------------------------------------
# /forms/<guid>/immutability — auth-gated metadata
# ---------------------------------------------------------------------------
class TestFormImmutability:
    def test_immutability_no_auth_returns_401_or_403(self, client):
        resp = client.get(
            '/api/v1/forms/00000000-0000-0000-0000-000000000000/immutability',
        )
        assert resp.status_code in (401, 403)

    def test_immutability_with_auth_resolves(self, client):
        """With SSO, the endpoint should at least RESPOND (200 or 404)
        rather than 5xx — pins that the route exists and the auth path
        works."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get(
            '/api/v1/forms/00000000-0000-0000-0000-000000000000/immutability',
        )
        assert resp.status_code != 500
        assert resp.status_code < 500
