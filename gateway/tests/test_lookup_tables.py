import pytest
from tests.conftest import get_auth_header


class TestCanonicalLibs:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)

        # Create
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'SNOMED CT',
            'canonical_lib_display_text': 'SNOMED Clinical Terms',
            'canonical_lib_url': 'http://snomed.info/sct',
        }, headers=headers)
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        # Read
        resp = client.get(f'/api/v1/canonical-libs/{guid}')
        assert resp.status_code == 200
        assert resp.get_json()['canonical_lib_name'] == 'SNOMED CT'

        # List
        resp = client.get('/api/v1/canonical-libs')
        assert resp.status_code == 200
        assert len(resp.get_json()) >= 1

        # Update
        resp = client.put(f'/api/v1/canonical-libs/{guid}', json={
            'canonical_lib_display_text': 'Updated display',
        }, headers=headers)
        assert resp.status_code == 200
        assert resp.get_json()['vers_number'] == 2

        # Delete
        resp = client.delete(f'/api/v1/canonical-libs/{guid}', headers=headers)
        assert resp.status_code == 200

        # Verify gone
        resp = client.get(f'/api/v1/canonical-libs/{guid}')
        assert resp.status_code == 404

    def test_duplicate_name(self, client):
        headers = get_auth_header(client)
        client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'LOINC',
        }, headers=headers)
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'LOINC',
        }, headers=headers)
        assert resp.status_code == 409

    def test_invalid_uuid(self, client):
        resp = client.get('/api/v1/canonical-libs/not-a-uuid')
        assert resp.status_code == 400

    def test_auth_required_for_create(self, client):
        resp = client.post('/api/v1/canonical-libs', json={
            'canonical_lib_name': 'ICD-10',
        })
        assert resp.status_code == 401


class TestConceptTypes:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)
        resp = client.post('/api/v1/concept-types', json={
            'concept_type_name': 'observation',
        }, headers=headers)
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        resp = client.get(f'/api/v1/concept-types/{guid}')
        assert resp.status_code == 200

        resp = client.delete(f'/api/v1/concept-types/{guid}', headers=headers)
        assert resp.status_code == 200


class TestResponseTypes:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)
        resp = client.post('/api/v1/response-types', json={
            'response_type_name': 'quantity',
        }, headers=headers)
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        resp = client.delete(f'/api/v1/response-types/{guid}', headers=headers)
        assert resp.status_code == 200


class TestUnits:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)
        resp = client.post('/api/v1/units', json={
            'unit_name': 'mmHg',
        }, headers=headers)
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        resp = client.delete(f'/api/v1/units/{guid}', headers=headers)
        assert resp.status_code == 200
