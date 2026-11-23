"""#1011 (stage 3 of #931) — plan's open API reads are gated, one group at a time.

#931 gave every READ consumer a read_only key and left the reads open behind a
shadow log (`plan.read_shadow`). Two days of that log, 2026-11-21..23, showed
one more keyless consumer — provider1.pdhc, whose `plan_client` is fail-soft —
and crawlers. Everything else arrived keyed or with a session.

This module carries the proof for each gated group, and grows by one group per
commit so each commit is deployable on its own:

  * a bare GET is refused with 401;
  * provider1.pdhc's read_only key gets 200 (the consumer the log found);
  * a read_only SSO session gets 200 (plan's own pages and any logged-in user);
  * a forged key is 403, and neither a bare nor a forged request is granted
    the rate-limit bypass, which only a VERIFIED key earns (#931).
"""
from __future__ import annotations

import uuid

import pytest

from app import db
from app.api.auth import KNOWN_SERVICES
from tests.conftest import SAMPLE_READONLY_BLOB, set_sso_session

PROVIDER1 = 'provider1.pdhc'
KEY = 'k-provider1-test'


@pytest.fixture
def provider1_key(app):
    var = KNOWN_SERVICES[PROVIDER1][0]
    old = app.config.get(var)
    app.config[var] = KEY
    yield
    app.config[var] = old if old is not None else ''


def _keyed(key=KEY):
    return {'X-Source-Service': PROVIDER1, 'X-Service-Key': key}


# --------------------------------------------------------------- the identity

def test_provider1_is_a_read_only_identity():
    assert KNOWN_SERVICES[PROVIDER1] == ('PROVIDER1_PDHC_SERVICE_KEY', 'read_only')


def test_provider1_key_reaches_app_config(app):
    # KNOWN_SERVICES naming a variable is not enough: auth.py resolves it via
    # current_app.config, so config.py must map it (the alert.pdhc lesson).
    assert 'PROVIDER1_PDHC_SERVICE_KEY' in app.config


def test_provider1_passes_an_already_gated_read(client, provider1_key):
    # concept-types has been gated since #925 — the read the operator script
    # uses to prove the key from inside provider1's container.
    assert client.get('/api/v1/lookup/concept-types').status_code == 401
    r = client.get('/api/v1/lookup/concept-types', headers=_keyed())
    assert r.status_code == 200


def test_provider1_cannot_write(client, provider1_key):
    r = client.post('/api/v1/lookup/units', json={'unit_name': 'x1011'}, headers=_keyed())
    assert r.status_code == 403
    assert r.get_json()['granted_role'] == 'read_only'


def test_an_unset_provider1_key_admits_nobody(client):
    r = client.get('/api/v1/lookup/concept-types', headers=_keyed('anything'))
    assert r.status_code == 403


# --------------------------------------------------------------- the groups
#
# Each group is a list of GET paths. `{name}` placeholders are filled from the
# `seeded` fixture so a keyed read can answer 200, not merely "not 401".

GROUPS: dict[str, list[str]] = {}


@pytest.fixture(scope='module')
def seeded(app):
    """One row of everything a gated read can return, created once."""
    from app.models.concept_models import (CanonicalLib, Concept, PlanDefType,
                                           ResponseType, Unit, ValueCatalog,
                                           ValueSet, ValueSetValue)
    from app.models.fhir_models import PlanDefinition
    from app.models.forms_models import Questionnaire
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        lib = CanonicalLib(canonical_lib_name=f'g1011-{tag}',
                           canonical_lib_url=f'https://example.org/g1011/{tag}')
        rt = ResponseType(response_type_name=f'g1011-rt-{tag}')
        unit = Unit(unit_name=f'g1011-u-{tag}')
        pdt = PlanDefType(plandef_type_name=f'g1011-pdt-{tag}')
        db.session.add_all([lib, rt, unit, pdt])
        db.session.flush()
        val = ValueCatalog(canonical_lib=lib.guid, value_name=f'g1011-v-{tag}',
                           canonical_refnumber=f'C{tag}')
        vs = ValueSet(canonical_lib=lib.guid, valueset_name=f'g1011-vs-{tag}')
        db.session.add_all([val, vs])
        db.session.flush()
        db.session.add(ValueSetValue(valueset_guid=vs.guid, value_guid=val.guid))
        concept = Concept(canonical_lib=lib.guid, concept_name=f'g1011-c-{tag}')
        pd = PlanDefinition(title=f'g1011 plan {tag}')
        form_guid = str(uuid.uuid4())
        db.session.add_all([concept, pd, Questionnaire(
            form_guid=form_guid, version=1, title=f'g1011 form {tag}',
            status='active', fhir_json={'resourceType': 'Questionnaire'})])
        db.session.commit()
        return {
            'lib': lib.guid, 'rt': rt.guid, 'unit': unit.guid, 'pdt': pdt.guid,
            'value': val.guid, 'vs': vs.guid, 'concept': concept.guid,
            'pd': pd.guid, 'pd_fhir': pd.fhir_id, 'form': form_guid,
        }


def _all_paths():
    return [(g, p) for g, paths in GROUPS.items() for p in paths]


def _ids():
    return [f'{g}:{p}' for g, p in _all_paths()]


@pytest.mark.parametrize('group,path', _all_paths(), ids=_ids())
def test_a_bare_read_is_refused(client, seeded, group, path):
    r = client.get(path.format(**seeded))
    assert r.status_code == 401, r.get_data(as_text=True)[:200]


@pytest.mark.parametrize('group,path', _all_paths(), ids=_ids())
def test_a_crawler_user_agent_changes_nothing(client, seeded, group, path):
    ua = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)'}
    assert client.get(path.format(**seeded), headers=ua).status_code == 401


@pytest.mark.parametrize('group,path', _all_paths(), ids=_ids())
def test_provider1_key_reads(client, seeded, provider1_key, group, path):
    r = client.get(path.format(**seeded), headers=_keyed())
    assert r.status_code == 200, r.get_data(as_text=True)[:300]


@pytest.mark.parametrize('group,path', _all_paths(), ids=_ids())
def test_a_read_only_session_reads(client, seeded, group, path):
    # The plan UI's own browser fetches ride on this session cookie.
    set_sso_session(client, SAMPLE_READONLY_BLOB)
    r = client.get(path.format(**seeded))
    assert r.status_code == 200, r.get_data(as_text=True)[:300]


@pytest.mark.parametrize('group,path', _all_paths(), ids=_ids())
def test_a_forged_key_is_403_and_earns_no_rate_limit_bypass(
        app, client, seeded, provider1_key, group, path):
    url = path.format(**seeded)
    assert client.get(url, headers=_keyed('wrong')).status_code == 403
    from app import _service_caller
    with app.test_request_context(url, headers=_keyed('wrong')):
        assert _service_caller() is False
    with app.test_request_context(url):
        assert _service_caller() is False
    # CONTROL: the bypass is reachable at all, so the two Falses mean something.
    with app.test_request_context(url, headers=_keyed()):
        assert _service_caller() is True
