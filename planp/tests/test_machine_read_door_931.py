"""#931 — plan gets a usable machine-auth door for its READ consumers, and a
shadow log of who still reads without one.

Before: KNOWN_SERVICES held sim (key unset) and alert, so no read consumer
could authenticate and plan's reads were open by necessity. Now each consumer
has its own read_only identity; the reads stay open until the shadow log shows
only keyed callers, then they are gated (the #902 shadow-then-enforce pattern).
"""
from __future__ import annotations

import logging

import pytest

from app.api.auth import KNOWN_SERVICES

READERS = ['request.pdhc', 'cdr.pdhc', 'cdr2.pdhc', 'cdr3.pdhc', 'dashboard.pdhc',
           'onboard.pdhc', 'contract.pdhc', 'analyse.pdhc']


@pytest.fixture
def keys(app):
    saved = {}
    for name in READERS:
        var = KNOWN_SERVICES[name][0]
        saved[var] = app.config.get(var)
        app.config[var] = f'key-for-{name}'
    yield
    for var, old in saved.items():
        app.config[var] = old if old is not None else ''


def _h(name, key=None):
    return {'X-Source-Service': name, 'X-Service-Key': key or f'key-for-{name}'}


# ----------------------------------------------------------------- the door

@pytest.mark.parametrize('name', READERS)
def test_each_reader_is_read_only(name):
    assert KNOWN_SERVICES[name][1] == 'read_only'


@pytest.mark.parametrize('name', READERS)
def test_a_reader_with_its_key_passes_a_GATED_read(client, keys, name):
    # /lookup/values is gated (read_only) — 401 without a credential.
    assert client.get('/api/v1/lookup/values').status_code == 401
    assert client.get('/api/v1/lookup/values', headers=_h(name)).status_code == 200


def test_a_reader_cannot_WRITE(client, keys):
    r = client.post('/api/v1/lookup/values', json={'name': 'x'}, headers=_h('request.pdhc'))
    assert r.status_code == 403
    assert r.get_json()['granted_role'] == 'read_only'


def test_one_readers_key_does_not_open_another_identity(client, keys):
    r = client.get('/api/v1/lookup/values', headers=_h('cdr2.pdhc', 'key-for-cdr.pdhc'))
    assert r.status_code == 403


def test_an_UNSET_key_admits_nobody(client):
    # no `keys` fixture: every reader's variable is '' in the test config
    r = client.get('/api/v1/lookup/values', headers=_h('request.pdhc', 'anything'))
    assert r.status_code == 403


# ----------------------------------------------------------------- the shadow log

def _shadow(caplog, fn):
    caplog.clear()
    with caplog.at_level(logging.WARNING, logger='plan.read_shadow'):
        fn()
    return [r.getMessage() for r in caplog.records if r.name == 'plan.read_shadow']


def test_an_unauthenticated_open_read_is_LOGGED_not_blocked(client, caplog):
    out = {}
    lines = _shadow(caplog, lambda: out.setdefault('r', client.get(
        '/api/v1/concepts', headers={'X-Forwarded-For': '203.0.113.7, 10.0.0.1'})))
    assert out['r'].status_code == 200, 'shadow only — nothing is gated yet'
    assert len(lines) == 1
    assert 'outcome=none' in lines[0] and 'path=/api/v1/concepts' in lines[0]
    assert 'remote=203.0.113.7' in lines[0]


def test_a_KEYED_read_is_not_logged(client, keys, caplog):
    assert _shadow(caplog, lambda: client.get('/api/v1/concepts', headers=_h('dashboard.pdhc'))) == []


def test_a_WRONG_key_is_logged_as_invalid_and_names_the_claim(client, keys, caplog):
    lines = _shadow(caplog, lambda: client.get('/api/v1/concepts', headers=_h('dashboard.pdhc', 'nope')))
    assert len(lines) == 1
    assert 'outcome=invalid_key' in lines[0] and 'claimed=dashboard.pdhc' in lines[0]
    assert 'nope' not in lines[0], 'a shadow line must never carry the key'


def test_an_SSO_session_is_not_logged(client, caplog):
    with client.session_transaction() as s:
        s['sso_token'] = 'tok'
    try:
        assert _shadow(caplog, lambda: client.get('/api/v1/concepts')) == []
    finally:
        with client.session_transaction() as s:
            s.pop('sso_token', None)


@pytest.mark.parametrize('path', ['/api/health', '/api/v1/metadata',
                                  '/api/v1/ValueSet/$validate-code?system=s&code=c'])
def test_public_by_decision_is_not_logged(client, caplog, path):
    assert _shadow(caplog, lambda: client.get(path)) == []


def test_a_write_is_not_the_shadow_logs_business(client, caplog):
    assert _shadow(caplog, lambda: client.post('/api/v1/lookup/values', json={})) == []


# ----------------------------------------------------------------- the limiter bypass

def test_a_FORGED_service_name_does_not_lift_the_rate_limit(app, keys):
    from app import _limiter_key, _service_caller
    with app.test_request_context('/api/v1/concepts', headers=_h('request.pdhc', 'forged')):
        assert _service_caller() is False
        assert not _limiter_key().startswith('service:')
    with app.test_request_context('/api/v1/concepts', headers=_h('request.pdhc')):
        assert _service_caller() is True
        assert _limiter_key() == 'service:request.pdhc'
