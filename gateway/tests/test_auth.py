import pytest
from unittest.mock import patch, MagicMock
from tests.conftest import (
    set_sso_session, SAMPLE_ACCESS_BLOB, SAMPLE_SU_BLOB, SAMPLE_READONLY_BLOB,
)


class TestSSOLogin:
    def test_login_redirects_to_sso(self, client):
        """H1 — /auth/login should redirect to SSO login page."""
        resp = client.get('/api/v1/auth/login')
        assert resp.status_code == 302
        assert 'sso-test:9000/login' in resp.headers['Location']
        assert 'next=' in resp.headers['Location']
        assert 'state=' in resp.headers['Location']

    def test_login_state_stored_in_session(self, client):
        """State parameter should be stored in session for CSRF validation."""
        resp = client.get('/api/v1/auth/login')
        with client.session_transaction() as sess:
            assert 'sso_state' in sess


class TestSSOCallback:
    @patch('app.services.sso_service.requests.get')
    def test_callback_happy_path(self, mock_get, client):
        """H3→H4 — valid token + state → session established, redirect to dashboard."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = SAMPLE_ACCESS_BLOB
        mock_get.return_value = mock_resp

        # Set state in session first (simulating H1)
        with client.session_transaction() as sess:
            sess['sso_state'] = 'test-state-123'

        resp = client.get('/api/v1/auth/callback?token=valid-jwt&state=test-state-123')
        assert resp.status_code == 302  # redirect to dashboard

        with client.session_transaction() as sess:
            assert sess['sso_user'] == SAMPLE_ACCESS_BLOB
            assert sess['sso_token'] == 'valid-jwt'

    def test_callback_state_mismatch(self, client):
        """Tampered state should be rejected with 403."""
        with client.session_transaction() as sess:
            sess['sso_state'] = 'original-state'

        resp = client.get('/api/v1/auth/callback?token=some-jwt&state=tampered-state')
        assert resp.status_code == 403

    def test_callback_missing_token(self, client):
        """Missing token should return 400."""
        with client.session_transaction() as sess:
            sess['sso_state'] = 'test-state'

        resp = client.get('/api/v1/auth/callback?state=test-state')
        assert resp.status_code == 400

    def test_callback_sso_error_response(self, client):
        """SSO error redirect should return 401."""
        with client.session_transaction() as sess:
            sess['sso_state'] = 'test-state'

        resp = client.get(
            '/api/v1/auth/callback?error=authentication_failed'
            '&error_description=Wrong+password&state=test-state'
        )
        assert resp.status_code == 401

    @patch('app.services.sso_service.requests.get')
    def test_callback_token_validation_fails(self, mock_get, client):
        """SSO returns 401 for expired/invalid token."""
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_get.return_value = mock_resp

        with client.session_transaction() as sess:
            sess['sso_state'] = 'test-state'

        resp = client.get('/api/v1/auth/callback?token=expired-jwt&state=test-state')
        assert resp.status_code == 401


class TestSSOMe:
    def test_me_with_session(self, client):
        """Authenticated user should see their access blob."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get('/api/v1/auth/me')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['email'] == 'doctor@hospital.se'

    def test_me_unauthenticated(self, client):
        """No session should return 401."""
        resp = client.get('/api/v1/auth/me')
        assert resp.status_code == 401


class TestSSOLogout:
    def test_logout_clears_session(self, client):
        """Logout should clear SSO data from session."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get('/api/v1/auth/logout')
        assert resp.status_code == 302  # redirect

        with client.session_transaction() as sess:
            assert 'sso_user' not in sess
            assert 'sso_token' not in sess


class TestRoleEnforcement:
    def test_planning_professional_can_write(self, client):
        """Professional with 'planning' phase can access write endpoints."""
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        # POST to a write endpoint (canonical-libs requires read_write)
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'Test Lib',
        })
        # Should not be 401 or 403
        assert resp.status_code not in (401, 403)

    def test_non_planning_professional_cannot_write(self, client):
        """Professional without 'planning' phase gets 403 on write endpoints."""
        set_sso_session(client, SAMPLE_READONLY_BLOB)
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'Test Lib',
        })
        assert resp.status_code == 403

    def test_su_admin_can_write(self, client):
        """SU admin bypasses all checks."""
        set_sso_session(client, SAMPLE_SU_BLOB)
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'Admin Lib',
        })
        assert resp.status_code not in (401, 403)

    def test_unauthenticated_gets_401_on_write(self, client):
        """No session on write endpoint returns 401."""
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'No Auth',
        })
        assert resp.status_code == 401

    def test_read_endpoints_are_public(self, client):
        """GET endpoints should work without authentication."""
        resp = client.get('/api/v1/canonical-libs')
        assert resp.status_code == 200


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200
        assert resp.get_json() == {'status': 'ok'}


class TestBootstrapSuperuser:
    def test_bootstrap_superuser_created(self, app):
        from app.models.user_models import User
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            assert user is not None
            assert user.role == 'admin'
