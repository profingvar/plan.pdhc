import pytest
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _setup_concept_deps(client):
    """Create canonical lib and return its GUID."""
    resp = client.post('/api/v1/canonical-libs', json={
        'canonical_lib_name': f'ConceptTestLib_{id(client)}',
    })
    return resp.get_json()['guid']


class TestConceptCRUD:
    def test_create_and_read(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'blood_pressure',
            'canonical_lib': lib_guid,
            'concept_display_text': 'Blood Pressure',
        })
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        resp = client.get(f'/api/v1/concepts/{guid}')
        assert resp.status_code == 200
        assert resp.get_json()['concept_name'] == 'blood_pressure'

    def test_list_with_pagination(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.get('/api/v1/concepts?page=1&per_page=10')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'items' in data
        assert 'total' in data

    def test_update(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'heart_rate',
            'canonical_lib': lib_guid,
        })
        guid = resp.get_json()['guid']

        resp = client.put(f'/api/v1/concepts/{guid}', json={
            'concept_display_text': 'Heart Rate Updated',
        })
        assert resp.status_code == 200
        assert resp.get_json()['vers_number'] == 2

    def test_delete(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'to_delete',
            'canonical_lib': lib_guid,
        })
        guid = resp.get_json()['guid']

        resp = client.delete(f'/api/v1/concepts/{guid}')
        assert resp.status_code == 200

        resp = client.get(f'/api/v1/concepts/{guid}')
        assert resp.status_code == 404

    def test_auth_required(self, client):
        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'no_auth',
            'canonical_lib': 'fake-guid',
        })
        assert resp.status_code == 401

    def test_invalid_uuid_rejected(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'bad_uuid',
            'canonical_lib': 'not-a-uuid',
        })
        assert resp.status_code == 400

    def test_name_uniqueness_auto_rename(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        client.post('/api/v1/concepts', json={
            'concept_name': 'duplicate_test',
            'canonical_lib': lib_guid,
        })

        resp = client.post('/api/v1/concepts', json={
            'concept_name': 'duplicate_test',
            'canonical_lib': lib_guid,
        })
        assert resp.status_code == 201
        assert resp.get_json()['concept_name'] == 'duplicate_test_1'


class TestConceptValues:
    def test_concept_values_through_valueset(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        # Create valueset
        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': f'ConceptVS_{id(client)}',
            'canonical_lib': lib_guid,
        })
        vs_guid = resp.get_json()['guid']

        # Create value
        resp = client.post('/api/v1/values', json={
            'value_name': f'ConceptVal_{id(client)}',
            'canonical_lib': lib_guid,
        })
        val_guid = resp.get_json()['guid']

        # Create concept bound to valueset
        resp = client.post('/api/v1/concepts', json={
            'concept_name': f'categorical_concept_{id(client)}',
            'canonical_lib': lib_guid,
            'valueset': vs_guid,
        })
        concept_guid = resp.get_json()['guid']

        # Add value through concept
        resp = client.post(f'/api/v1/concepts/{concept_guid}/values', json={
            'value_guid': val_guid,
        })
        assert resp.status_code == 201

        # List values
        resp = client.get(f'/api/v1/concepts/{concept_guid}/values')
        assert resp.status_code == 200
        assert len(resp.get_json()) == 1

        # Remove value
        resp = client.delete(
            f'/api/v1/concepts/{concept_guid}/values/{val_guid}',
        )
        assert resp.status_code == 200

    def test_no_valueset_error(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _setup_concept_deps(client)

        resp = client.post('/api/v1/concepts', json={
            'concept_name': f'no_vs_concept_{id(client)}',
            'canonical_lib': lib_guid,
        })
        concept_guid = resp.get_json()['guid']

        resp = client.post(f'/api/v1/concepts/{concept_guid}/values', json={
            'value_guid': '00000000-0000-0000-0000-000000000000',
        })
        assert resp.status_code == 400
        assert 'does not have a valueset' in resp.get_json()['error']
