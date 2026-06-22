"""§6.1 + §6.2 — FHIR R5 ValueSet resource, $expand, and scoped $validate-code.

Covers:
- GET  /api/v1/ValueSet/{guid}                — read (§6.1)
- GET  /api/v1/ValueSet                       — searchset Bundle (§6.1)
- GET  /api/v1/ValueSet/{guid}/$expand        — expand by id (§6.1)
- POST /api/v1/ValueSet/$expand               — expand by Parameters body (§6.1)
- GET  /api/v1/ValueSet/{guid}/$validate-code — scoped by id (§6.2)
- GET  /api/v1/ValueSet/$validate-code?url=&… — scoped by url (§6.2)
- POST /api/v1/ValueSet/$validate-code        — scoped by Parameters body (§6.2)
- §2 cdr.pdhc regression                       — global $validate-code unchanged
- D3 url-shape pin / D3.b legacy URL acceptance
- D5 fast-layer validator (fhir.resources R5)
"""
from __future__ import annotations

import pytest
from fhir.resources.bundle import Bundle as FHIRBundle
from fhir.resources.parameters import Parameters as FHIRParameters
from fhir.resources.valueset import ValueSet as FHIRValueSetModel

from app import db as _db
from app.models.concept_models import (
    PLAN_BASE,
    CanonicalLib,
    ValueCatalog,
    ValueSet,
    ValueSetValue,
    fhir_canonical_url,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def yes_no_vs(app):
    """A ValueSet 'YesNo' with two values from a fresh test-only lib."""
    with app.app_context():
        lib_name = 'fhirvstest_yesno_lib'
        lib = CanonicalLib.query.filter_by(canonical_lib_name=lib_name).first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name=lib_name,
                canonical_lib_display_text='YesNo Test Lib',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/fhirvstest-yesno',
                author='test',
            )
            _db.session.add(lib)
            _db.session.flush()

        vs = ValueSet.query.filter_by(valueset_name='FHIRVSTest_YesNo').first()
        if vs is None:
            vs = ValueSet(
                canonical_lib=lib.guid,
                valueset_name='FHIRVSTest_YesNo',
                valueset_display_text='Yes or No',
                valueset_explanation='Two-value test set used by §6.1 tests.',
                author='test',
            )
            _db.session.add(vs)
            _db.session.flush()

            v_yes = ValueCatalog(
                canonical_lib=lib.guid,
                canonical_refnumber='Y',
                value_name='FHIRVSTestYes',
                value_display_text='Yes',
            )
            v_no = ValueCatalog(
                canonical_lib=lib.guid,
                canonical_refnumber='N',
                value_name='FHIRVSTestNo',
                value_display_text='No',
            )
            _db.session.add_all([v_yes, v_no])
            _db.session.flush()

            _db.session.add(ValueSetValue(
                valueset_guid=vs.guid, value_guid=v_yes.guid, sort_order=1,
            ))
            _db.session.add(ValueSetValue(
                valueset_guid=vs.guid, value_guid=v_no.guid, sort_order=2,
            ))
            _db.session.commit()

        yield {
            'vs_guid': vs.guid,
            'lib_url': lib.canonical_lib_url,
        }


@pytest.fixture()
def empty_vs(app):
    """A ValueSet with no values — exercises the empty-compose path."""
    with app.app_context():
        lib = CanonicalLib.query.filter_by(
            canonical_lib_name='fhirvstest_empty_lib',
        ).first()
        if lib is None:
            lib = CanonicalLib(
                canonical_lib_name='fhirvstest_empty_lib',
                canonical_lib_display_text='Empty Test Lib',
                canonical_lib_url='https://termbank.pdhc.se/CodeSystem/fhirvstest-empty',
                author='test',
            )
            _db.session.add(lib)
            _db.session.flush()
        vs = ValueSet.query.filter_by(valueset_name='FHIRVSTest_Empty').first()
        if vs is None:
            vs = ValueSet(
                canonical_lib=lib.guid,
                valueset_name='FHIRVSTest_Empty',
                valueset_display_text='Empty set',
                author='test',
            )
            _db.session.add(vs)
            _db.session.commit()
        yield vs.guid


# ---------------------------------------------------------------------------
# GET /ValueSet/{guid}
# ---------------------------------------------------------------------------
class TestReadValueSet:
    def test_resource_shape(self, client, yes_no_vs):
        resp = client.get(f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}")
        assert resp.status_code == 200
        assert resp.headers['Content-Type'].startswith('application/fhir+json')
        body = resp.get_json()
        assert body['resourceType'] == 'ValueSet'
        assert body['id'] == yes_no_vs['vs_guid']
        # ADR D3 — canonical url emitted in /fhir/ form
        assert body['url'] == \
            f'{PLAN_BASE}/fhir/ValueSet/{yes_no_vs["vs_guid"]}'
        assert body['status'] == 'active'
        assert body['name'] == 'FHIRVSTest_YesNo'
        assert body['title'] == 'Yes or No'
        # version per ADR D4
        assert body['version'] == '1'

    def test_compose_groups_by_system(self, client, yes_no_vs):
        resp = client.get(f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}")
        body = resp.get_json()
        assert 'compose' in body
        includes = body['compose']['include']
        assert len(includes) == 1
        system_block = includes[0]
        assert system_block['system'] == yes_no_vs['lib_url']
        codes = {c['code']: c['display'] for c in system_block['concept']}
        assert codes == {'Y': 'Yes', 'N': 'No'}

    def test_read_404_unknown_guid(self, client):
        resp = client.get('/api/v1/ValueSet/00000000-0000-0000-0000-000000000000')
        assert resp.status_code == 404
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'

    def test_read_400_invalid_guid(self, client):
        resp = client.get('/api/v1/ValueSet/not-a-uuid')
        assert resp.status_code == 400
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'

    def test_validates_as_R5_valueset(self, client, yes_no_vs):
        # D5 fast layer — round-trip via the pydantic R5 model
        resp = client.get(f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}")
        FHIRValueSetModel.model_validate(resp.get_json())


# ---------------------------------------------------------------------------
# GET /ValueSet — searchset Bundle
# ---------------------------------------------------------------------------
class TestSearchValueSets:
    def test_returns_searchset_bundle(self, client, yes_no_vs):
        resp = client.get('/api/v1/ValueSet')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'Bundle'
        assert body['type'] == 'searchset'
        assert isinstance(body['entry'], list)
        # Bundle validates against the R5 pydantic model
        FHIRBundle.model_validate(body)

    def test_url_filter_canonical_form(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.get(f'/api/v1/ValueSet?url={canonical}')
        body = resp.get_json()
        assert body['total'] == 1
        assert body['entry'][0]['resource']['id'] == yes_no_vs['vs_guid']

    def test_url_filter_legacy_form_d3b(self, client, yes_no_vs):
        # D3.b — legacy {PLAN_BASE}/api/v1/valuesets/{guid} accepted
        legacy = f'{PLAN_BASE}/api/v1/valuesets/{yes_no_vs["vs_guid"]}'
        resp = client.get(f'/api/v1/ValueSet?url={legacy}')
        body = resp.get_json()
        assert body['total'] == 1

    def test_url_filter_lookup_form_d3b(self, client, yes_no_vs):
        # D3.b — also the actual route form /api/v1/lookup/valuesets/{guid}
        lookup = f'{PLAN_BASE}/api/v1/lookup/valuesets/{yes_no_vs["vs_guid"]}'
        resp = client.get(f'/api/v1/ValueSet?url={lookup}')
        body = resp.get_json()
        assert body['total'] == 1

    def test_url_filter_unknown_returns_empty(self, client, yes_no_vs):
        resp = client.get(
            f'/api/v1/ValueSet?url={PLAN_BASE}/fhir/ValueSet/'
            '00000000-0000-0000-0000-000000000000'
        )
        body = resp.get_json()
        assert body['total'] == 0
        assert body['entry'] == []

    def test_paging_count_offset(self, client, yes_no_vs, empty_vs):
        resp = client.get('/api/v1/ValueSet?_count=1&_offset=0')
        body = resp.get_json()
        assert len(body['entry']) == 1
        assert body['total'] >= 2  # at least the two fixtures
        resp2 = client.get('/api/v1/ValueSet?_count=1&_offset=1')
        body2 = resp2.get_json()
        assert len(body2['entry']) == 1
        # Different ValueSet at next offset
        assert body2['entry'][0]['resource']['id'] != \
            body['entry'][0]['resource']['id']


# ---------------------------------------------------------------------------
# GET /ValueSet/{guid}/$expand
# ---------------------------------------------------------------------------
class TestExpandByGet:
    def test_expansion_contains_resolves_system_code_display(
        self, client, yes_no_vs,
    ):
        resp = client.get(f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$expand")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'ValueSet'
        assert 'expansion' in body
        contains = body['expansion']['contains']
        assert body['expansion']['total'] == 2
        codes = {c['code']: c for c in contains}
        assert set(codes.keys()) == {'Y', 'N'}
        for entry in contains:
            assert entry['system'] == yes_no_vs['lib_url']
            assert entry['display'] in ('Yes', 'No')
        # D5 — expansion-bearing ValueSet still validates as R5
        FHIRValueSetModel.model_validate(body)

    def test_expand_empty_valueset_returns_total_zero(self, client, empty_vs):
        resp = client.get(f'/api/v1/ValueSet/{empty_vs}/$expand')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['expansion']['total'] == 0
        assert body['expansion']['contains'] == []
        FHIRValueSetModel.model_validate(body)

    def test_expand_404_unknown(self, client):
        resp = client.get(
            '/api/v1/ValueSet/00000000-0000-0000-0000-000000000000/$expand'
        )
        assert resp.status_code == 404

    def test_expand_400_invalid_guid(self, client):
        resp = client.get('/api/v1/ValueSet/not-a-uuid/$expand')
        assert resp.status_code == 400

    def test_escaped_dollar_sign(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/%24expand"
        )
        assert resp.status_code == 200
        assert resp.get_json()['expansion']['total'] == 2


# ---------------------------------------------------------------------------
# POST /ValueSet/$expand — Parameters body
# ---------------------------------------------------------------------------
class TestExpandByPost:
    def _params_body(self, **kv):
        return {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': k, 'valueString': v} for k, v in kv.items()
            ],
        }

    def test_expand_by_url_parameter(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.post(
            '/api/v1/ValueSet/$expand',
            json=self._params_body(url=canonical),
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'ValueSet'
        assert body['expansion']['total'] == 2

    def test_expand_by_valueSet_parameter_fallback(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.post(
            '/api/v1/ValueSet/$expand',
            json=self._params_body(valueSet=canonical),
        )
        assert resp.status_code == 200
        assert resp.get_json()['expansion']['total'] == 2

    def test_expand_by_legacy_url_d3b(self, client, yes_no_vs):
        legacy = f'{PLAN_BASE}/api/v1/valuesets/{yes_no_vs["vs_guid"]}'
        resp = client.post(
            '/api/v1/ValueSet/$expand',
            json=self._params_body(url=legacy),
        )
        assert resp.status_code == 200

    def test_400_when_no_identifier(self, client):
        resp = client.post(
            '/api/v1/ValueSet/$expand',
            json={'resourceType': 'Parameters', 'parameter': []},
        )
        assert resp.status_code == 400
        assert resp.get_json()['issue'][0]['code'] == 'required'

    def test_400_when_url_unparseable(self, client):
        resp = client.post(
            '/api/v1/ValueSet/$expand',
            json=self._params_body(url='https://x/garbage'),
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# §2 regression — legacy CRUD JSON is untouched by the new FHIR surface
# ---------------------------------------------------------------------------
class TestLegacyCRUDRegression:
    def test_lookup_valuesets_route_still_returns_legacy_json(
        self, client, yes_no_vs,
    ):
        """The existing lookup CRUD (/api/v1/lookup/valuesets/<guid>) keeps
        its non-FHIR shape — separate route, separate blueprint."""
        resp = client.get(
            f"/api/v1/lookup/valuesets/{yes_no_vs['vs_guid']}",
        )
        assert resp.status_code == 200
        body = resp.get_json()
        # The legacy shape uses 'valueset_name', NOT 'resourceType'
        assert body['valueset_name'] == 'FHIRVSTest_YesNo'
        assert 'resourceType' not in body
        # Legacy 'values' member format
        assert 'values' in body


# ===========================================================================
# §6.2 — scoped $validate-code (keeping the global cdr.pdhc contract intact)
# ===========================================================================
class TestScopedValidateCodeByGuid:
    """GET /api/v1/ValueSet/{guid}/$validate-code?system=&code="""

    def _flat(self, body):
        return {
            p['name']: p.get('valueBoolean', p.get('valueString'))
            for p in body['parameter']
        }

    def test_member_returns_true(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code"
            f"?system={yes_no_vs['lib_url']}&code=Y"
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        flat = self._flat(body)
        assert flat['result'] is True
        assert flat['display'] == 'Yes'

    def test_non_member_returns_false(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code"
            f"?system={yes_no_vs['lib_url']}&code=NOPE"
        )
        assert resp.status_code == 200
        flat = self._flat(resp.get_json())
        assert flat['result'] is False
        assert 'not in ValueSet' in flat['message']

    def test_system_by_name_works(self, client, yes_no_vs):
        # cdr.pdhc/global form passes lib NAME as system; the scoped
        # handler must accept either name or url.
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code"
            '?system=fhirvstest_yesno_lib&code=Y'
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True

    def test_system_omitted_matches_by_code_alone(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code?code=Y"
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True

    def test_unknown_system_returns_false_not_404(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code"
            '?system=fake-system-not-registered&code=Y'
        )
        assert resp.status_code == 200
        flat = self._flat(resp.get_json())
        assert flat['result'] is False
        assert 'not registered' in flat['message']

    def test_missing_code_400(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/$validate-code"
        )
        assert resp.status_code == 400
        assert resp.get_json()['issue'][0]['code'] == 'required'

    def test_unknown_valueset_404(self, client):
        resp = client.get(
            '/api/v1/ValueSet/00000000-0000-0000-0000-000000000000'
            '/$validate-code?system=x&code=Y'
        )
        assert resp.status_code == 404

    def test_escaped_dollar_sign(self, client, yes_no_vs):
        resp = client.get(
            f"/api/v1/ValueSet/{yes_no_vs['vs_guid']}/%24validate-code"
            f"?system={yes_no_vs['lib_url']}&code=Y"
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True


class TestScopedValidateCodeByUrl:
    """GET /api/v1/ValueSet/$validate-code?url=...&code=..."""

    def _flat(self, body):
        return {
            p['name']: p.get('valueBoolean', p.get('valueString'))
            for p in body['parameter']
        }

    def test_url_canonical_form(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'url': canonical, 'code': 'Y'},
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True

    def test_url_legacy_form_d3b(self, client, yes_no_vs):
        legacy = f"{PLAN_BASE}/api/v1/valuesets/{yes_no_vs['vs_guid']}"
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'url': legacy, 'code': 'Y'},
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True

    def test_url_with_valueSet_alias(self, client, yes_no_vs):
        # FHIR spec accepts either 'url' or 'valueSet' query param.
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'valueSet': canonical, 'code': 'Y'},
        )
        assert resp.status_code == 200
        assert self._flat(resp.get_json())['result'] is True

    def test_url_unparseable_400(self, client):
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'url': 'not a url', 'code': 'Y'},
        )
        assert resp.status_code == 400

    def test_url_unknown_404(self, client):
        bad = f'{PLAN_BASE}/fhir/ValueSet/00000000-0000-0000-0000-000000000000'
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'url': bad, 'code': 'Y'},
        )
        assert resp.status_code == 404


class TestScopedValidateCodeByPost:
    """POST /api/v1/ValueSet/$validate-code with Parameters body."""

    def _params(self, **kv):
        return {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': k, 'valueString': v} for k, v in kv.items()
            ],
        }

    def test_post_url_code_returns_true(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.post(
            '/api/v1/ValueSet/$validate-code',
            json=self._params(url=canonical, code='Y'),
        )
        assert resp.status_code == 200
        body = resp.get_json()
        FHIRParameters.model_validate(body)
        flat = {
            p['name']: p.get('valueBoolean', p.get('valueString'))
            for p in body['parameter']
        }
        assert flat['result'] is True
        assert flat['display'] == 'Yes'

    def test_post_missing_url_400(self, client):
        resp = client.post(
            '/api/v1/ValueSet/$validate-code',
            json=self._params(code='Y'),
        )
        assert resp.status_code == 400

    def test_post_missing_code_400(self, client, yes_no_vs):
        canonical = fhir_canonical_url('ValueSet', yes_no_vs['vs_guid'])
        resp = client.post(
            '/api/v1/ValueSet/$validate-code',
            json=self._params(url=canonical),
        )
        assert resp.status_code == 400


class TestCDRGlobalContractAfter62:
    """§6.2 must NOT touch the cdr.pdhc global path. Re-pin the contract
    here so any future change that breaks the cdr shim fails loudly in
    this file, not just in test_capability.py."""

    @pytest.fixture()
    def cdr_loinc(self, app):
        with app.app_context():
            lib = CanonicalLib.query.filter_by(
                canonical_lib_name='loinc',
            ).first()
            if lib is None:
                lib = CanonicalLib(
                    canonical_lib_name='loinc',
                    canonical_lib_url='https://termbank.pdhc.se/CodeSystem/loinc',
                    author='termbank.pdhc',
                )
                _db.session.add(lib)
                _db.session.flush()
            existing_val = ValueCatalog.query.filter_by(
                canonical_lib=lib.guid,
                canonical_refnumber='4548-4',
            ).first()
            if existing_val is None:
                _db.session.add(ValueCatalog(
                    canonical_lib=lib.guid,
                    canonical_refnumber='4548-4',
                    value_name='HbA1c-cdr-pin-62',
                    value_display_text='HbA1c',
                ))
                _db.session.commit()
            yield

    def test_global_no_url_still_works(self, client, cdr_loinc):
        """Exact shape cdr.pdhc plan_client sends."""
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'system': 'loinc', 'code': '4548-4'},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'Parameters'
        flat = {
            p['name']: p.get('valueBoolean', p.get('valueString'))
            for p in body['parameter']
        }
        assert flat['result'] is True

    def test_global_missing_system_still_400(self, client):
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'code': '4548-4'},
        )
        # Global path keeps the original "both required" rule (§4.2 pin).
        assert resp.status_code == 400
