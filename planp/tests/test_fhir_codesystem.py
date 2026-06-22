"""§6.3 — FHIR R5 CodeSystem resource + $lookup with termbank delegation.

Covers:
- GET  /api/v1/CodeSystem                — searchset Bundle
- GET  /api/v1/CodeSystem/{id}           — read
- GET  /api/v1/CodeSystem/$lookup        — by query params
- POST /api/v1/CodeSystem/$lookup        — by Parameters body
- ADR D1                                 — code = Concept.guid
- ADR D2                                 — single local CodeSystem
- Termbank delegation                    — when system is a CanonicalLib,
                                            $lookup goes through
                                            TermbankClient (not 404)
- D5 fast-layer validator                — outputs validate as R5
                                            CodeSystem / Bundle / Parameters
"""
from __future__ import annotations

from unittest.mock import patch

import pytest
from fhir.resources.bundle import Bundle as FHIRBundle
from fhir.resources.codesystem import CodeSystem as FHIRCodeSystem
from fhir.resources.parameters import Parameters as FHIRParameters

from app import db as _db
from app.api.fhir_codesystem import LOCAL_CS_NAME, LOCAL_CS_URL
from app.models.concept_models import (
    LOCAL_CODESYSTEM_ID,
    PLAN_BASE,
    CanonicalLib,
    Concept,
    fhir_canonical_url,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def cs_concept(app):
    """Insert a local Concept bound to a CanonicalLib (cstest_loinc, 1234).
    The Concept guid is the local code (per D1)."""
    with app.app_context():
        lib = CanonicalLib.query.filter_by(
            canonical_lib_name='cstest_loinc',
        ).first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name='cstest_loinc',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/cstest-loinc',
                author='test',
            )
            _db.session.add(lib)
            _db.session.flush()
        c = Concept.query.filter_by(concept_name='cs_test_concept').first()
        if c is None:
            c = Concept(
                canonical_lib=lib.guid,
                canonical_refnumber='1234',
                concept_name='cs_test_concept',
                concept_display_text='CS Test Concept',
                concept_explain='Test concept used by the §6.3 CodeSystem tests.',
            )
            _db.session.add(c)
            _db.session.commit()
        yield {
            'guid': c.guid,
            'display': c.concept_display_text,
            'lib_url': lib.canonical_lib_url,
            'lib_name': lib.canonical_lib_name,
        }


# ---------------------------------------------------------------------------
# GET /CodeSystem/{id}
# ---------------------------------------------------------------------------
class TestReadCodeSystem:
    def test_shape_and_fields(self, client, cs_concept):
        resp = client.get(f'/api/v1/CodeSystem/{LOCAL_CODESYSTEM_ID}')
        assert resp.status_code == 200
        assert resp.headers['Content-Type'].startswith('application/fhir+json')
        body = resp.get_json()
        assert body['resourceType'] == 'CodeSystem'
        assert body['id'] == LOCAL_CODESYSTEM_ID
        # ADR D3 — canonical url
        assert body['url'] == LOCAL_CS_URL
        assert body['status'] == 'active'
        assert body['content'] == 'complete'
        assert body['caseSensitive'] is True
        assert body['count'] >= 1
        FHIRCodeSystem.model_validate(body)

    def test_concept_uses_guid_as_code_d1(self, client, cs_concept):
        body = client.get(f'/api/v1/CodeSystem/{LOCAL_CODESYSTEM_ID}').get_json()
        codes = {e['code'] for e in body['concept']}
        # ADR D1
        assert cs_concept['guid'] in codes

    def test_concept_display_is_concept_display_text(
        self, client, cs_concept,
    ):
        body = client.get(f'/api/v1/CodeSystem/{LOCAL_CODESYSTEM_ID}').get_json()
        match = next(e for e in body['concept'] if e['code'] == cs_concept['guid'])
        assert match['display'] == cs_concept['display']
        assert 'definition' in match

    def test_concept_carries_canonical_property(self, client, cs_concept):
        body = client.get(f'/api/v1/CodeSystem/{LOCAL_CODESYSTEM_ID}').get_json()
        match = next(e for e in body['concept'] if e['code'] == cs_concept['guid'])
        props = {p['code']: p['valueString'] for p in match.get('property', [])}
        assert props.get('canonical-lib') == cs_concept['lib_name']
        assert props.get('canonical-ref') == '1234'

    def test_unknown_id_404(self, client):
        resp = client.get('/api/v1/CodeSystem/wrong-id')
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /CodeSystem (searchset Bundle)
# ---------------------------------------------------------------------------
class TestSearchCodeSystems:
    def test_returns_bundle_with_local_cs(self, client, cs_concept):
        resp = client.get('/api/v1/CodeSystem')
        body = resp.get_json()
        assert body['resourceType'] == 'Bundle'
        assert body['type'] == 'searchset'
        assert body['total'] == 1
        assert body['entry'][0]['resource']['id'] == LOCAL_CODESYSTEM_ID
        FHIRBundle.model_validate(body)

    def test_url_filter_match(self, client, cs_concept):
        resp = client.get(f'/api/v1/CodeSystem?url={LOCAL_CS_URL}')
        assert resp.get_json()['total'] == 1

    def test_url_filter_no_match(self, client, cs_concept):
        resp = client.get(f'/api/v1/CodeSystem?url={PLAN_BASE}/fhir/CodeSystem/other')
        assert resp.get_json()['total'] == 0


# ---------------------------------------------------------------------------
# GET /CodeSystem/$lookup — LOCAL system
# ---------------------------------------------------------------------------
class TestLookupLocal:
    def _flat(self, body):
        out = {}
        for p in body['parameter']:
            if 'valueString' in p:
                out[p['name']] = p['valueString']
            elif 'valueBoolean' in p:
                out[p['name']] = p['valueBoolean']
        return out

    def test_lookup_by_guid_returns_concept(self, client, cs_concept):
        resp = client.get(
            '/api/v1/CodeSystem/$lookup',
            query_string={'system': LOCAL_CS_URL, 'code': cs_concept['guid']},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        flat = self._flat(body)
        assert flat['name'] == LOCAL_CS_NAME
        assert flat['display'] == cs_concept['display']

    def test_lookup_includes_canonical_lib_property(self, client, cs_concept):
        resp = client.get(
            '/api/v1/CodeSystem/$lookup',
            query_string={'system': LOCAL_CS_URL, 'code': cs_concept['guid']},
        )
        body = resp.get_json()
        # Find the canonical-lib property part
        props = [
            p for p in body['parameter'] if p['name'] == 'property'
        ]
        property_codes = []
        for p in props:
            for sub in p['part']:
                if sub['name'] == 'code':
                    property_codes.append(sub['valueCode'])
        assert 'canonical-lib' in property_codes
        assert 'canonical-ref' in property_codes

    def test_lookup_unknown_guid_404(self, client):
        resp = client.get(
            '/api/v1/CodeSystem/$lookup',
            query_string={
                'system': LOCAL_CS_URL,
                'code': '00000000-0000-0000-0000-000000000000',
            },
        )
        assert resp.status_code == 404
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'

    def test_missing_params_400(self, client):
        resp = client.get('/api/v1/CodeSystem/$lookup')
        assert resp.status_code == 400
        assert resp.get_json()['issue'][0]['code'] == 'required'

    def test_escaped_dollar_sign(self, client, cs_concept):
        resp = client.get(
            '/api/v1/CodeSystem/%24lookup',
            query_string={'system': LOCAL_CS_URL, 'code': cs_concept['guid']},
        )
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# $lookup — EXTERNAL system delegates to TermbankClient
# ---------------------------------------------------------------------------
class TestLookupExternalDelegatesToTermbank:
    """Spec §6.3 delegation rule. The TermbankClient is the existing
    in-process TTL cache that already powers /api/v1/termbank/concept/.
    Mocking ``client.lookup`` lets us verify the wiring without touching
    the live termbank service."""

    def test_external_system_by_url_delegates(self, client, app, cs_concept):
        fake = {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': 'name', 'valueString': 'LOINC'},
                {'name': 'display', 'valueString': 'Hemoglobin A1c'},
            ],
        }
        with patch.object(
            app.termbank_client, 'lookup', return_value=fake,
        ) as m:
            resp = client.get(
                '/api/v1/CodeSystem/$lookup',
                query_string={
                    'system': cs_concept['lib_url'],
                    'code': '4548-4',
                },
            )
        assert resp.status_code == 200
        assert resp.get_json() == fake
        # The delegation call uses the CanonicalLib NAME, not URL,
        # matching what termbank itself expects.
        m.assert_called_once_with(cs_concept['lib_name'], '4548-4')

    def test_external_system_by_name_delegates(self, client, app, cs_concept):
        fake = {'resourceType': 'Parameters', 'parameter': []}
        with patch.object(
            app.termbank_client, 'lookup', return_value=fake,
        ) as m:
            resp = client.get(
                '/api/v1/CodeSystem/$lookup',
                query_string={
                    'system': cs_concept['lib_name'],
                    'code': '4548-4',
                },
            )
        assert resp.status_code == 200
        m.assert_called_once_with(cs_concept['lib_name'], '4548-4')

    def test_termbank_miss_returns_404_operationoutcome(
        self, client, app, cs_concept,
    ):
        with patch.object(app.termbank_client, 'lookup', return_value=None):
            resp = client.get(
                '/api/v1/CodeSystem/$lookup',
                query_string={
                    'system': cs_concept['lib_url'],
                    'code': 'NOPE',
                },
            )
        assert resp.status_code == 404
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'
        # Hint that it could be unreachability, not just a real miss.
        assert 'unreachable' in body['issue'][0]['details']['text']

    def test_unregistered_external_system_404(self, client):
        resp = client.get(
            '/api/v1/CodeSystem/$lookup',
            query_string={
                'system': 'totally-fake-canonical-lib',
                'code': '1234',
            },
        )
        assert resp.status_code == 404
        body = resp.get_json()
        # Should be a clear 'not a registered CanonicalLib' message —
        # we should NOT have called termbank in this case.
        assert 'not a registered CanonicalLib' in \
            body['issue'][0]['details']['text']


# ---------------------------------------------------------------------------
# POST /CodeSystem/$lookup
# ---------------------------------------------------------------------------
class TestLookupPost:
    def _params(self, **kv):
        return {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': k, 'valueString': v} for k, v in kv.items()
            ],
        }

    def test_post_local(self, client, cs_concept):
        resp = client.post(
            '/api/v1/CodeSystem/$lookup',
            json=self._params(
                system=LOCAL_CS_URL,
                code=cs_concept['guid'],
            ),
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)

    def test_post_external_delegates(self, client, app, cs_concept):
        fake = {'resourceType': 'Parameters', 'parameter': []}
        with patch.object(
            app.termbank_client, 'lookup', return_value=fake,
        ) as m:
            resp = client.post(
                '/api/v1/CodeSystem/$lookup',
                json=self._params(
                    system=cs_concept['lib_url'],
                    code='4548-4',
                ),
            )
        assert resp.status_code == 200
        m.assert_called_once()

    def test_post_missing_400(self, client):
        resp = client.post(
            '/api/v1/CodeSystem/$lookup',
            json=self._params(system=LOCAL_CS_URL),
        )
        assert resp.status_code == 400
