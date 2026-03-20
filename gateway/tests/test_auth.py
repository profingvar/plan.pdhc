import pytest
from tests.conftest import get_auth_header


class TestAuth:
    def test_login_valid(self, client):
        resp = client.post('/api/v1/auth/login', json={
            'username': 'admin',
            'password': 'admin123',
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == 'admin'

    def test_login_invalid_password(self, client):
        resp = client.post('/api/v1/auth/login', json={
            'username': 'admin',
            'password': 'wrong',
        })
        assert resp.status_code == 401

    def test_login_missing_fields(self, client):
        resp = client.post('/api/v1/auth/login', json={})
        assert resp.status_code == 400

    def test_me_authenticated(self, client):
        headers = get_auth_header(client)
        resp = client.get('/api/v1/auth/me', headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['username'] == 'admin'

    def test_me_unauthenticated(self, client):
        resp = client.get('/api/v1/auth/me')
        assert resp.status_code == 401

    def test_logout(self, client):
        headers = get_auth_header(client)
        resp = client.post('/api/v1/auth/logout', headers=headers)
        assert resp.status_code == 200

    def test_bootstrap_superuser_created(self, app):
        from app.models.user_models import User
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            assert user is not None
            assert user.role == 'admin'
