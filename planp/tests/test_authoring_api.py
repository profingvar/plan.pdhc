"""GA-3 — opt-in /api/v1/authoring surface (epic #516)."""
import pytest

from app import db
from app.models.concept_models import CanonicalLib, ResponseType, Unit
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB


def _goc(model, name_field, name, **extra):
    row = model.query.filter(getattr(model, name_field).ilike(name)).first()
    if row:
        return row
    row = model(**{name_field: name}, **extra)
    db.session.add(row)
    db.session.commit()
    return row


@pytest.fixture
def seed(app):
    with app.app_context():
        return {
            'rt_qty': _goc(ResponseType, 'response_type_name', 'Quantity').guid,
            'lib': _goc(CanonicalLib, 'canonical_lib_name', 'LOINC-GA').guid,
        }


def test_models_endpoint_reports_disabled_by_default(client):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)  # planning phase -> read_write
    r = client.get('/api/v1/authoring/models')
    assert r.status_code == 200
    assert r.get_json()['enabled'] is False


def test_models_endpoint_when_enabled(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_MODELS', ['claude-sonnet-5'])
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.get('/api/v1/authoring/models')
    body = r.get_json()
    assert body['enabled'] is True
    assert 'claude-sonnet-5' in body['models']


def test_validate_endpoint_flags_quantity_without_unit(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/validate', json={
        'kind': 'concept',
        'payload': {
            'response_type': seed['rt_qty'],
            'canonical_lib': seed['lib'],
            'canonical_refnumber': '8480-6',
        },
    })
    assert r.status_code == 200
    body = r.get_json()
    assert body['ok'] is False
    assert any(i['code'] == 'E-UNIT-REQUIRED' for i in body['issues'])


def test_validate_endpoint_disabled_returns_flag(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', False)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/validate', json={'kind': 'concept', 'payload': {}})
    assert r.status_code == 200
    assert r.get_json()['enabled'] is False


def test_assist_requires_intent(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/assist', json={'intent': ''})
    assert r.status_code == 400


def test_authoring_requires_auth(client, app, monkeypatch):
    # No SSO session set -> read_write decorator must reject.
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    with client.session_transaction() as sess:
        sess.clear()
    r = client.get('/api/v1/authoring/models')
    assert r.status_code in (401, 403)


# ---- openEHR-realisability proxy (#523) --------------------------------
class _FakeR:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._p = payload
    def json(self):
        return self._p


def test_openehr_realisable_disabled(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', False)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/openehr-realisable', json={'concept_guids': []})
    assert r.status_code == 200 and r.get_json()['enabled'] is False


def test_openehr_realisable_not_configured(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    monkeypatch.setitem(app.config, 'ROSETTA_BASE_URL', '')
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/openehr-realisable', json={'concept_guids': []})
    body = r.get_json()
    assert body['available'] is False and body['reason'] == 'rosetta_not_configured'


def test_openehr_realisable_forwards_to_rosetta(client, app, monkeypatch):
    import app.api.authoring as authoring
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    monkeypatch.setitem(app.config, 'ROSETTA_BASE_URL', 'http://rosetta.test')
    monkeypatch.setitem(app.config, 'ROSETTA_SERVICE_KEY', 'k')
    captured = {}
    def fake_post(url, json=None, headers=None, timeout=None):
        captured['url'] = url; captured['json'] = json; captured['headers'] = headers
        return _FakeR(200, {'total': 1, 'realisable_count': 1, 'all_realisable': True,
                            'templates': ['pdhc_vitals.v1'], 'concepts': [], 'pending': [], 'unmapped': []})
    monkeypatch.setattr(authoring.requests, 'post', fake_post)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/openehr-realisable',
                    json={'transactions': [{'concept_guid': 'g1'}]})
    body = r.get_json()
    assert body['available'] is True and body['all_realisable'] is True
    assert captured['url'] == 'http://rosetta.test/api/v1/openehr/realisable'
    assert captured['headers']['X-Service-Key'] == 'k'


def test_openehr_realisable_unreachable_degrades(client, app, monkeypatch):
    import app.api.authoring as authoring
    import requests as _rq
    monkeypatch.setitem(app.config, 'AUTHORING_ASSISTANT_ENABLED', True)
    monkeypatch.setitem(app.config, 'ROSETTA_BASE_URL', 'http://rosetta.test')
    def boom(*a, **k):
        raise _rq.ConnectionError('nope')
    monkeypatch.setattr(authoring.requests, 'post', boom)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/authoring/openehr-realisable', json={'concept_guids': ['g']})
    assert r.get_json()['reason'] == 'rosetta_unreachable'
