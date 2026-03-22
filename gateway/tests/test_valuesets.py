import pytest
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _create_canonical_lib(client, name='TestLib'):
    resp = client.post('/api/v1/canonical-libs', json={
        'canonical_lib_name': name,
    })
    return resp.get_json()['guid']


class TestValues:
    def test_crud_cycle(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _create_canonical_lib(client, 'ValuesLib')

        # Create
        resp = client.post('/api/v1/values', json={
            'value_name': 'Yes',
            'canonical_lib': lib_guid,
            'value_display_text': 'Yes',
        })
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
        })
        assert resp.status_code == 200

        # Delete
        resp = client.delete(f'/api/v1/values/{guid}')
        assert resp.status_code == 200

    def test_requires_canonical_lib(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        resp = client.post('/api/v1/values', json={
            'value_name': 'Missing',
        })
        assert resp.status_code == 400


class TestValueSets:
    def test_crud_cycle(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _create_canonical_lib(client, 'VSLib')

        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': 'YesNo',
            'canonical_lib': lib_guid,
        })
        assert resp.status_code == 201
        vs_guid = resp.get_json()['guid']

        resp = client.get(f'/api/v1/valuesets/{vs_guid}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'values' in data
        assert isinstance(data['values'], list)

        resp = client.get('/api/v1/valuesets')
        assert resp.status_code == 200

        resp = client.delete(f'/api/v1/valuesets/{vs_guid}')
        assert resp.status_code == 200

    def test_create_with_values(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _create_canonical_lib(client, 'VSValLib')

        # Create values first
        resp = client.post('/api/v1/values', json={
            'value_name': 'Yes', 'canonical_lib': lib_guid,
        })
        val1 = resp.get_json()['guid']
        resp = client.post('/api/v1/values', json={
            'value_name': 'No', 'canonical_lib': lib_guid,
        })
        val2 = resp.get_json()['guid']

        # Create valueset with values and sort orders
        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': 'YesNoSet',
            'canonical_lib': lib_guid,
            'values': [
                {'value_guid': val1, 'sort_order': 1},
                {'value_guid': val2, 'sort_order': 2},
            ],
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert len(data['values']) == 2
        assert data['values'][0]['value_name'] == 'Yes'
        assert data['values'][0]['sort_order'] == 1
        assert data['values'][1]['value_name'] == 'No'
        assert data['values'][1]['sort_order'] == 2

        # GET should also return full value references
        resp = client.get(f'/api/v1/valuesets/{data["guid"]}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data['values']) == 2
        assert data['values'][0]['guid'] == val1


class TestValueSetMembership:
    def test_add_remove_values(self, client):
        set_sso_session(client, SAMPLE_ACCESS_BLOB)
        lib_guid = _create_canonical_lib(client, 'MemberLib')

        # Create valueset
        resp = client.post('/api/v1/valuesets', json={
            'valueset_name': 'Severity',
            'canonical_lib': lib_guid,
        })
        vs_guid = resp.get_json()['guid']

        # Create values
        resp = client.post('/api/v1/values', json={
            'value_name': 'Mild',
            'canonical_lib': lib_guid,
        })
        val1_guid = resp.get_json()['guid']

        resp = client.post('/api/v1/values', json={
            'value_name': 'Severe',
            'canonical_lib': lib_guid,
        })
        val2_guid = resp.get_json()['guid']

        # Add to valueset
        resp = client.post(f'/api/v1/valuesets/{vs_guid}/values', json={
            'value_guid': val1_guid,
            'sort_order': 1,
        })
        assert resp.status_code == 201

        resp = client.post(f'/api/v1/valuesets/{vs_guid}/values', json={
            'value_guid': val2_guid,
            'sort_order': 2,
        })
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
        })
        assert resp.status_code == 409

        # Remove
        resp = client.delete(f'/api/v1/valuesets/{vs_guid}/values/{val1_guid}')
        assert resp.status_code == 200

        resp = client.get(f'/api/v1/valuesets/{vs_guid}/values')
        assert len(resp.get_json()) == 1
