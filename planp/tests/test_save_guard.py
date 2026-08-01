"""GA-5 (#521) — fail-closed enforcement on the save paths + override hatch."""
import pytest

from app import db
from app.models.concept_models import CanonicalLib, ResponseType, Unit
from tests.conftest import set_sso_session, SAMPLE_ACCESS_BLOB, SAMPLE_SU_BLOB


def _goc(model, field, name, **extra):
    row = model.query.filter(getattr(model, field).ilike(name)).first()
    if row:
        return row
    row = model(**{field: name}, **extra)
    db.session.add(row)
    db.session.commit()
    return row


@pytest.fixture
def seed(app):
    with app.app_context():
        return {
            'lib': _goc(CanonicalLib, 'canonical_lib_name', 'LOINC-SG').guid,
            'rt_num': _goc(ResponseType, 'response_type_name', 'numerical').guid,
            'unit': _goc(Unit, 'unit_name', 'mmHg').guid,
        }


def _numeric_no_unit(seed, name):
    return {'concept_name': name, 'canonical_lib': seed['lib'],
            'response_type': seed['rt_num'], 'canonical_refnumber': '8480-6'}  # numeric, NO unit


def test_api_create_blocked_on_error(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/concepts', json=_numeric_no_unit(seed, 'sg-blocked'))
    assert r.status_code == 422
    body = r.get_json()
    assert body['error'] == 'validation_failed'
    assert any(i['code'] == 'E-UNIT-REQUIRED' for i in body['issues'])


def test_api_create_valid_passes(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    payload = _numeric_no_unit(seed, 'sg-valid')
    payload['unit'] = seed['unit']
    r = client.post('/api/v1/concepts', json=payload)
    assert r.status_code == 201


def test_admin_override_forces_save(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_SU_BLOB)  # is_su_admin
    payload = _numeric_no_unit(seed, 'sg-override')
    payload['override_validation'] = True
    r = client.post('/api/v1/concepts', json=payload)
    assert r.status_code == 201


def test_nonadmin_override_still_blocked(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)  # planning, NOT admin
    payload = _numeric_no_unit(seed, 'sg-nonadmin')
    payload['override_validation'] = True
    r = client.post('/api/v1/concepts', json=payload)
    assert r.status_code == 422


def test_killswitch_disables_enforcement(client, app, seed, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', False)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/concepts', json=_numeric_no_unit(seed, 'sg-killswitch'))
    assert r.status_code == 201


def test_warning_only_concept_passes(client, app, seed, monkeypatch):
    # missing terminology code is now a WARNING (#521) -> save allowed
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/concepts', json={
        'concept_name': 'sg-warn-only', 'canonical_lib': seed['lib'],
        'response_type': seed['rt_num'], 'unit': seed['unit'],  # valid quantity, no code
    })
    assert r.status_code == 201


def test_plandef_api_blocked_on_dangling_ref(client, app, monkeypatch):
    monkeypatch.setitem(app.config, 'PLANDEF_VALIDATION_ENFORCED', True)
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = client.post('/api/v1/plandefinitions', json={
        'title': 'sg pd dangling',
        'actions': [{'transactions': [{'concept_guid': 'not-a-real-guid'}]}],
    })
    assert r.status_code == 422
    assert any(i['code'] == 'E-DANGLING-REF' for i in r.get_json()['issues'])
