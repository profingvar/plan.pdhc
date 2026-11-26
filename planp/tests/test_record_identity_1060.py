"""#1060: record.pdhc is a read_only identity, for ConceptMap/$translate.

record.pdhc's EEHRxF laboratory-report export (stage 7) must name each result
with a standard code (LOINC / NPU). A result in cdr1 carries only
`urn:pdhc:concept|<guid>`; the binding lives here, behind the #1011 gate. So
record reads `$translate` with its own key, and nothing else.
"""
from __future__ import annotations

import pytest

from app.api.auth import KNOWN_SERVICES

RECORD = 'record.pdhc'
KEY = 'k-record-test-1060'


@pytest.fixture
def record_key(app):
    var = KNOWN_SERVICES[RECORD][0]
    old = app.config.get(var)
    app.config[var] = KEY
    yield
    app.config[var] = old if old is not None else ''


def _keyed(key=KEY):
    return {'X-Source-Service': RECORD, 'X-Service-Key': key}


TRANSLATE = ('/api/v1/ConceptMap/$translate'
             '?system=https://plan.pdhc.se/fhir/CodeSystem/plan-pdhc-local'
             '&code=00000000-0000-4000-8000-000000001060')


def test_record_is_a_read_only_identity():
    assert KNOWN_SERVICES[RECORD] == ('RECORD_PDHC_SERVICE_KEY', 'read_only')


def test_record_key_reaches_app_config(app):
    assert 'RECORD_PDHC_SERVICE_KEY' in app.config


def test_translate_is_gated_and_the_record_key_opens_it(client, record_key):
    assert client.get(TRANSLATE).status_code == 401
    r = client.get(TRANSLATE, headers=_keyed())
    assert r.status_code == 200, r.get_data(as_text=True)[:300]
    assert r.get_json()['resourceType'] == 'Parameters'


def test_record_cannot_write(client, record_key):
    r = client.post('/api/v1/lookup/units', json={'unit_name': 'x1060'}, headers=_keyed())
    assert r.status_code == 403
    assert r.get_json()['granted_role'] == 'read_only'


def test_a_wrong_or_unset_record_key_admits_nobody(client, record_key):
    assert client.get(TRANSLATE, headers=_keyed('wrong')).status_code == 403


def test_an_unset_record_key_admits_nobody(client):
    assert client.get(TRANSLATE, headers=_keyed('anything')).status_code == 403
