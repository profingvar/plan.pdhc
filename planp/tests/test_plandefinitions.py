import json
import pytest
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


class TestFHIRPlanDefinitionAPI:
    def test_search_returns_bundle(self, client):
        resp = client.get('/api/v1/PlanDefinition')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['resourceType'] == 'Bundle'
        assert data['type'] == 'searchset'
        assert 'total' in data

    def test_not_found(self, client):
        resp = client.get('/api/v1/PlanDefinition/nonexistent-id')
        assert resp.status_code == 404

    def test_post_returns_501(self, client):
        resp = client.post('/api/v1/PlanDefinition', json={})
        assert resp.status_code == 501

    def test_search_with_filters(self, client):
        resp = client.get('/api/v1/PlanDefinition?status=draft&_count=5&_offset=0')
        assert resp.status_code == 200
