import pytest
from tests.conftest import get_auth_header


def _create_canonical_lib(client, headers, name='TestLib'):
    resp = client.post('/api/v1/canonical-libs', json={
        'canonical_lib_name': name,
    }, headers=headers)
    return resp.get_json()['guid']


class TestValues:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)
        lib_guid = _create_canonical_lib(client, headers, 'ValuesLib')

        # Create
        resp = client.post('/api/v1/values', json={
            'value_name': 'Yes',
            'canonical_lib': lib_guid,
            'value_display_text': 'Yes',
        }, headers=headers)
        assert resp.status_code == 201
        guid = resp.get_json()['guid']

        # Read
        resp = client.get(f'/api/v1/values/{guid}')
        assert resp.status_code == 200

        # List
        resp = client.get('/api/v1/values')
        assert resp.status_code == 200
        assert len(resp.get_json()) >= 1

        # Update
        resp = client.put(f'/api/v1/values/{guid}', json={
            'value_display_text': 'Updated',
        }, headers=headers)
        assert resp.status_code == 200

        # Delete
        resp = client.delete(f'/api/v1/values/{guid}', headers=headers)
        assert resp.status_code == 200

    def test_requires_canonical_lib(self, client):
        headers = get_auth_header(client)
        resp = client.post('/api/v1/values', json={
            'value_name': 'Missing',
        }, headers=headers)
        assert resp.status_code == 400


class TestValueSets:
    def test_crud_cycle(self, client):
        headers = get_auth_header(client)
        lib_guid = _create_canonical_lib(client, headers, 'VSLib')

        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': 'YesNo',
            'canonical_lib': lib_guid,
        }, headers=headers)
        assert resp.status_code == 201
        vs_guid = resp.get_json()['guid']

        resp = client.get(f'/api/v1/valuesets/{vs_guid}')
        assert resp.status_code == 200

        resp = client.get('/api/v1/valuesets')
        assert resp.status_code == 200

        resp = client.delete(f'/api/v1/valuesets/{vs_guid}', headers=headers)
        assert resp.status_code == 200


class TestValueSetMembership:
    def test_add_remove_values(self, client):
        headers = get_auth_header(client)
        lib_guid = _create_canonical_lib(client, headers, 'MemberLib')

        # Create valueset
        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': 'Severity',
            'canonical_lib': lib_guid,
        }, headers=headers)
        vs_guid = resp.get_json()['guid']

        # Create values
        resp = client.post('/api/v1/values', json={
            'value_name': 'Mild',
            'canonical_lib': lib_guid,
        }, headers=headers)
        val1_guid = resp.get_json()['guid']

        resp = client.post('/api/v1/values', json={
            'value_name': 'Severe',
            'canonical_lib': lib_guid,
        }, headers=headers)
        val2_guid = resp.get_json()['guid']

        # Add to valueset
        resp = client.post(f'/api/v1/valuesets/{vs_guid}/values', json={
            'value_guid': val1_guid,
            'sort_order': 1,
        }, headers=headers)
        assert resp.status_code == 201

        resp = client.post(f'/api/v1/valuesets/{vs_guid}/values', json={
            'value_guid': val2_guid,
            'sort_order': 2,
        }, headers=headers)
        assert resp.status_code == 201

        # List values in set
        resp = client.get(f'/api/v1/valuesets/{vs_guid}/values')
        assert resp.status_code == 200
        vals = resp.get_json()
        assert len(vals) == 2
        assert vals[0]['value_name'] == 'Mild'

        # Duplicate prevention
        resp = client.post(f'/api/v1/valuesets/{vs_guid}/values', json={
            'value_guid': val1_guid,
        }, headers=headers)
        assert resp.status_code == 409

        # Remove
        resp = client.delete(f'/api/v1/valuesets/{vs_guid}/values/{val1_guid}', headers=headers)
        assert resp.status_code == 200

        resp = client.get(f'/api/v1/valuesets/{vs_guid}/values')
        assert len(resp.get_json()) == 1
