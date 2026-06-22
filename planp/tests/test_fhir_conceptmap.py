"""§6.4 — FHIR R5 ConceptMap resource + $translate.

Covers both directions of translation (local↔canonical), the full
ConceptMap resource projection grouped by target system, error paths,
D3 url-scheme pin, D5 fast-layer validation, and the Risk §9.5
match-is-an-array invariant.
"""
from __future__ import annotations

import pytest
from fhir.resources.bundle import Bundle as FHIRBundle
from fhir.resources.conceptmap import ConceptMap as FHIRConceptMap
from fhir.resources.parameters import Parameters as FHIRParameters

from app import db as _db
from app.api.fhir_conceptmap import LOCAL_CS_URL
from app.models.concept_models import (
    LOCAL_CONCEPTMAP_ID,
    PLAN_BASE,
    CanonicalLib,
    Concept,
    fhir_canonical_url,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def bound_concepts(app):
    """Insert two CanonicalLibs and three Concepts:
       - hba1c → (cmtest_loinc, '4548-4')
       - diabetes → (cmtest_snomed, '44054006')
       - orphan concept with no canonical_refnumber (excluded from map)
    Returns the guids and URLs for assertions."""
    with app.app_context():
        loinc = CanonicalLib.query.filter_by(
            canonical_lib_name='cmtest_loinc',
        ).first()
        if loinc is None:
            loinc = CanonicalLib(
                canonical_lib_name='cmtest_loinc',
                canonical_lib_display_text='Test LOINC',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/cmtest-loinc',
                author='test',
            )
            _db.session.add(loinc)
            _db.session.flush()
        snomed = CanonicalLib.query.filter_by(
            canonical_lib_name='cmtest_snomed',
        ).first()
        if snomed is None:
            snomed = CanonicalLib(
                canonical_lib_name='cmtest_snomed',
                canonical_lib_display_text='Test SNOMED',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/cmtest-snomed',
                author='test',
            )
            _db.session.add(snomed)
            _db.session.flush()

        hba1c = Concept.query.filter_by(
            concept_name='cmtest_hba1c',
        ).first()
        if hba1c is None:
            hba1c = Concept(
                canonical_lib=loinc.guid,
                canonical_refnumber='4548-4',
                concept_name='cmtest_hba1c',
                concept_display_text='HbA1c (test)',
            )
            _db.session.add(hba1c)

        diabetes = Concept.query.filter_by(
            concept_name='cmtest_diabetes',
        ).first()
        if diabetes is None:
            diabetes = Concept(
                canonical_lib=snomed.guid,
                canonical_refnumber='44054006',
                concept_name='cmtest_diabetes',
                concept_display_text='Diabetes mellitus type 2 (test)',
            )
            _db.session.add(diabetes)

        orphan = Concept.query.filter_by(
            concept_name='cmtest_orphan',
        ).first()
        if orphan is None:
            orphan = Concept(
                canonical_lib=loinc.guid,
                canonical_refnumber=None,  # no canonical binding code
                concept_name='cmtest_orphan',
                concept_display_text='Orphan local concept',
            )
            _db.session.add(orphan)

        _db.session.commit()

        yield {
            'loinc_url': loinc.canonical_lib_url,
            'loinc_name': loinc.canonical_lib_name,
            'snomed_url': snomed.canonical_lib_url,
            'snomed_name': snomed.canonical_lib_name,
            'hba1c_guid': hba1c.guid,
            'diabetes_guid': diabetes.guid,
            'orphan_guid': orphan.guid,
        }


# ---------------------------------------------------------------------------
# GET /ConceptMap/{id}
# ---------------------------------------------------------------------------
class TestReadConceptMap:
    def test_resource_shape(self, client, bound_concepts):
        resp = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}')
        assert resp.status_code == 200
        assert resp.headers['Content-Type'].startswith('application/fhir+json')
        body = resp.get_json()
        assert body['resourceType'] == 'ConceptMap'
        assert body['id'] == LOCAL_CONCEPTMAP_ID
        # D3 — canonical url
        assert body['url'] == \
            f'{PLAN_BASE}/fhir/ConceptMap/{LOCAL_CONCEPTMAP_ID}'
        assert body['status'] == 'active'
        assert body['sourceScopeUri'] == LOCAL_CS_URL

    def test_groups_keyed_by_target_system(self, client, bound_concepts):
        body = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}').get_json()
        targets = {g['target'] for g in body['group']}
        # Both libs should appear
        assert bound_concepts['loinc_url'] in targets
        assert bound_concepts['snomed_url'] in targets
        # Every group's source is the local CodeSystem URL
        assert all(g['source'] == LOCAL_CS_URL for g in body['group'])

    def test_local_guid_is_source_code_d1(self, client, bound_concepts):
        body = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}').get_json()
        all_source_codes = {
            e['code'] for g in body['group'] for e in g['element']
        }
        # ADR D1 — local CodeSystem code is Concept.guid
        assert bound_concepts['hba1c_guid'] in all_source_codes
        assert bound_concepts['diabetes_guid'] in all_source_codes

    def test_orphan_concept_excluded(self, client, bound_concepts):
        body = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}').get_json()
        all_source_codes = {
            e['code'] for g in body['group'] for e in g['element']
        }
        assert bound_concepts['orphan_guid'] not in all_source_codes

    def test_target_relationship_is_equivalent(self, client, bound_concepts):
        body = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}').get_json()
        for g in body['group']:
            for e in g['element']:
                for t in e['target']:
                    assert t['relationship'] == 'equivalent'

    def test_unknown_id_404(self, client):
        resp = client.get('/api/v1/ConceptMap/no-such-map')
        assert resp.status_code == 404

    def test_validates_as_R5_conceptmap(self, client, bound_concepts):
        body = client.get(f'/api/v1/ConceptMap/{LOCAL_CONCEPTMAP_ID}').get_json()
        FHIRConceptMap.model_validate(body)


# ---------------------------------------------------------------------------
# GET /ConceptMap (searchset Bundle)
# ---------------------------------------------------------------------------
class TestSearchConceptMaps:
    def test_returns_bundle(self, client, bound_concepts):
        resp = client.get('/api/v1/ConceptMap')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'Bundle'
        assert body['type'] == 'searchset'
        assert body['total'] == 1
        assert body['entry'][0]['resource']['id'] == LOCAL_CONCEPTMAP_ID
        FHIRBundle.model_validate(body)

    def test_url_filter_match(self, client, bound_concepts):
        canonical = fhir_canonical_url('ConceptMap', LOCAL_CONCEPTMAP_ID)
        resp = client.get(f'/api/v1/ConceptMap?url={canonical}')
        assert resp.get_json()['total'] == 1

    def test_url_filter_no_match(self, client, bound_concepts):
        resp = client.get(
            f'/api/v1/ConceptMap?url={PLAN_BASE}/fhir/ConceptMap/other'
        )
        body = resp.get_json()
        assert body['total'] == 0
        assert body['entry'] == []


# ---------------------------------------------------------------------------
# $translate — local → canonical
# ---------------------------------------------------------------------------
class TestTranslateLocalToCanonical:
    def _flat_matches(self, body):
        """Pull the match parts out of a Parameters body."""
        out = []
        for p in body['parameter']:
            if p.get('name') != 'match':
                continue
            sub = {sub_p['name']: sub_p for sub_p in p.get('part', [])}
            out.append({
                'relationship': sub['relationship']['valueCode'],
                'coding': sub['concept']['valueCoding'],
            })
        return out

    def test_local_to_loinc(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['hba1c_guid'],
            },
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is True
        matches = self._flat_matches(body)
        assert len(matches) == 1
        assert matches[0]['relationship'] == 'equivalent'
        assert matches[0]['coding']['system'] == bound_concepts['loinc_url']
        assert matches[0]['coding']['code'] == '4548-4'

    def test_local_to_canonical_with_targetsystem_match(
        self, client, bound_concepts,
    ):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['hba1c_guid'],
                'targetsystem': bound_concepts['loinc_url'],
            },
        )
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is True

    def test_local_to_canonical_targetsystem_mismatch_returns_false(
        self, client, bound_concepts,
    ):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['hba1c_guid'],
                'targetsystem': bound_concepts['snomed_url'],
            },
        )
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is False

    def test_unknown_local_concept_returns_false(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': '00000000-0000-0000-0000-000000000000',
            },
        )
        assert resp.status_code == 200
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is False
        # Risk §9.5 — match is still expressible (empty here)
        matches = self._flat_matches(body)
        assert matches == []

    def test_orphan_concept_returns_false_with_clear_message(
        self, client, bound_concepts,
    ):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['orphan_guid'],
            },
        )
        body = resp.get_json()
        message = next(
            (p['valueString'] for p in body['parameter']
             if p['name'] == 'message'),
            '',
        )
        assert 'no canonical binding' in message


# ---------------------------------------------------------------------------
# $translate — canonical → local
# ---------------------------------------------------------------------------
class TestTranslateCanonicalToLocal:
    def _flat_matches(self, body):
        out = []
        for p in body['parameter']:
            if p.get('name') != 'match':
                continue
            sub = {sub_p['name']: sub_p for sub_p in p.get('part', [])}
            out.append({
                'relationship': sub['relationship']['valueCode'],
                'coding': sub['concept']['valueCoding'],
            })
        return out

    def test_canonical_url_to_local(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': bound_concepts['loinc_url'],
                'code': '4548-4',
            },
        )
        body = resp.get_json()
        matches = self._flat_matches(body)
        assert len(matches) == 1
        assert matches[0]['coding']['system'] == LOCAL_CS_URL
        assert matches[0]['coding']['code'] == bound_concepts['hba1c_guid']

    def test_canonical_name_to_local_cdr_friendly(self, client, bound_concepts):
        # cdr.pdhc-style: pass lib NAME, not URL.
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': bound_concepts['loinc_name'],
                'code': '4548-4',
            },
        )
        body = resp.get_json()
        matches = self._flat_matches(body)
        assert len(matches) == 1
        assert matches[0]['coding']['code'] == bound_concepts['hba1c_guid']

    def test_unknown_canonical_code_returns_false(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': bound_concepts['loinc_url'],
                'code': 'NOPE',
            },
        )
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is False

    def test_unknown_system_returns_false_not_404(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': 'totally-fake-canonical-lib',
                'code': '4548-4',
            },
        )
        assert resp.status_code == 200
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is False
        msg = next(p['valueString'] for p in body['parameter']
                   if p['name'] == 'message')
        assert 'not registered' in msg

    def test_canonical_with_wrong_targetsystem_returns_false(
        self, client, bound_concepts,
    ):
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': bound_concepts['loinc_url'],
                'code': '4548-4',
                'targetsystem': bound_concepts['snomed_url'],
            },
        )
        body = resp.get_json()
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is False


# ---------------------------------------------------------------------------
# POST /ConceptMap/$translate
# ---------------------------------------------------------------------------
class TestTranslatePost:
    def _params(self, **kv):
        return {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': k, 'valueString': v} for k, v in kv.items()
            ],
        }

    def test_post_local_to_canonical(self, client, bound_concepts):
        resp = client.post(
            '/api/v1/ConceptMap/$translate',
            json=self._params(
                system=LOCAL_CS_URL,
                code=bound_concepts['hba1c_guid'],
            ),
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        flat = {p['name']: p.get('valueBoolean') for p in body['parameter']
                if 'valueBoolean' in p}
        assert flat['result'] is True

    def test_post_missing_system_400(self, client):
        resp = client.post(
            '/api/v1/ConceptMap/$translate',
            json=self._params(code='4548-4'),
        )
        assert resp.status_code == 400
        assert resp.get_json()['issue'][0]['code'] == 'required'

    def test_post_missing_code_400(self, client):
        resp = client.post(
            '/api/v1/ConceptMap/$translate',
            json=self._params(system=LOCAL_CS_URL),
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Operation contract / error handling
# ---------------------------------------------------------------------------
class TestTranslateGetErrorPaths:
    def test_missing_required_400(self, client):
        resp = client.get('/api/v1/ConceptMap/$translate')
        assert resp.status_code == 400
        assert resp.get_json()['issue'][0]['code'] == 'required'

    def test_escaped_dollar_sign(self, client, bound_concepts):
        resp = client.get(
            '/api/v1/ConceptMap/%24translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['hba1c_guid'],
            },
        )
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Risk §9.5 — match is always an array-shaped parameter
# ---------------------------------------------------------------------------
class TestMatchArrayInvariant:
    def test_zero_matches_does_not_collapse_response(
        self, client, bound_concepts,
    ):
        """When result=false, the body should still validate as
        Parameters and never invent a singleton object for ``match``.
        FHIR's Parameters repetition shape preserves array-ness."""
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': '00000000-0000-0000-0000-000000000000',
            },
        )
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        # No 'match' parameters at all (not a single dict with name='match'
        # and an empty 'part' — which would imply 1 match with no data).
        assert not any(p.get('name') == 'match' for p in body['parameter'])

    def test_single_match_is_one_parameter_part_not_a_list(
        self, client, bound_concepts,
    ):
        """A single match emits ONE parameter with name='match'. Future
        N matches will emit N parameters with name='match' — the
        repetition is at the Parameters level, not under a single
        'match' key."""
        resp = client.get(
            '/api/v1/ConceptMap/$translate',
            query_string={
                'system': LOCAL_CS_URL,
                'code': bound_concepts['hba1c_guid'],
            },
        )
        body = resp.get_json()
        match_params = [p for p in body['parameter']
                        if p.get('name') == 'match']
        assert len(match_params) == 1
        assert isinstance(match_params[0]['part'], list)
