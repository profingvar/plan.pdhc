"""Characterization tests for plan.pdhc's §2 CapabilityStatement surface
and the cdr.pdhc cross-service ``$validate-code`` contract.

These tests pin existing behaviour so the FHIR R5 terminology profile
work (``plan_pdhc_fhir_terminology_profile_instruction.md`` §6) cannot
silently break either ``capability.py`` or the cdr.pdhc shim.

§6.7 will update the CapabilityStatement to declare the new ValueSet /
CodeSystem / ConceptMap surface — but the field set asserted in
``TestFHIRMetadata`` and ``TestHumanCapability`` must keep working
unchanged across that update.

The CDR contract pin (``TestCDRValidateCodeContract``) reflects the
exact request shape sent by
``cdr.pdhc/cdr_app/app/services/plan_client.py::PlanClient.validate_code``
and the fields its ``_parse_parameters`` reads from the response. If
any of those assertions starts failing, do NOT silently update them —
coordinate with the cdr.pdhc team to update ``PlanClient`` in lockstep.
"""
from __future__ import annotations

import pytest

from app import db as _db
from app.models.concept_models import CanonicalLib, Concept


# ---------------------------------------------------------------------------
# /metadata — FHIR R5 CapabilityStatement
# ---------------------------------------------------------------------------
class TestFHIRMetadata:
    def test_resource_type_and_required_fields(self, client):
        resp = client.get('/api/v1/metadata')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['resourceType'] == 'CapabilityStatement'
        for field in ('id', 'url', 'version', 'name', 'status', 'kind', 'software'):
            assert field in body, f'missing required field: {field}'
        assert body['kind'] == 'instance'


# ---------------------------------------------------------------------------
# /capability-statement — human-readable index
# ---------------------------------------------------------------------------
class TestHumanCapability:
    def test_returns_resources_dict_and_endpoint_count(self, client):
        resp = client.get('/api/v1/capability-statement')
        assert resp.status_code == 200
        body = resp.get_json()
        assert 'resources' in body
        assert isinstance(body['resources'], dict)
        assert body.get('total_endpoints', 0) > 0
        assert body['fhir_version'] == 'R5'


# ---------------------------------------------------------------------------
# /endpoints — operator-friendly route inventory
# ---------------------------------------------------------------------------
class TestEndpointList:
    def test_total_matches_endpoints_length(self, client):
        resp = client.get('/api/v1/endpoints')
        assert resp.status_code == 200
        body = resp.get_json()
        assert isinstance(body.get('endpoints'), list)
        assert body['total'] == len(body['endpoints'])


# ===========================================================================
# CDR cross-service contract pin
# ===========================================================================
class TestCDRValidateCodeContract:
    """Source of contract:

      - URL:   ``cdr.pdhc/cdr_app/app/services/plan_client.py``
               ``PlanClient.validate_code()`` builds
               ``GET {base}/api/v1/ValueSet/$validate-code?system=&code=``
      - Body:  ``PlanClient._parse_parameters()`` reads ``result``
               (Boolean) plus any ``valueString`` fields by ``name``
               from ``body['parameter'][*]``.
    """

    @pytest.fixture()
    def loinc_concept(self, app):
        """Insert a (loinc, 4548-4) Concept. Tolerates rows seeded by
        a prior test in the same session — checks before insert."""
        with app.app_context():
            lib = CanonicalLib.query.filter_by(
                canonical_lib_name='loinc',
            ).first()
            if lib is None:
                lib = CanonicalLib(
                    canonical_lib_name='loinc',
                    canonical_lib_display_text='LOINC',
                    canonical_lib_url='https://termbank.pdhc.se/CodeSystem/loinc',
                    author='termbank.pdhc',
                )
                _db.session.add(lib)
                _db.session.flush()
            c = Concept.query.filter_by(
                canonical_lib=lib.guid,
                canonical_refnumber='4548-4',
            ).first()
            if c is None:
                c = Concept(
                    canonical_lib=lib.guid,
                    canonical_refnumber='4548-4',
                    concept_name='HbA1c-contract-pin',
                    concept_display_text='Hemoglobin A1c',
                )
                _db.session.add(c)
                _db.session.commit()
            yield

    def test_url_shape_used_by_cdr(self, client, loinc_concept):
        """The exact URL ``PlanClient.validate_code`` constructs must work."""
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'system': 'loinc', 'code': '4548-4'},
        )
        assert resp.status_code == 200

    def test_parameters_shape_parseable_by_cdr(self, client, loinc_concept):
        """Mirror ``PlanClient._parse_parameters`` — assert the same
        fields it relies on are present and shaped correctly."""
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'system': 'loinc', 'code': '4548-4'},
        )
        body = resp.get_json()
        assert body['resourceType'] == 'Parameters'
        assert isinstance(body['parameter'], list)

        flat = {}
        for p in body['parameter']:
            name = p.get('name')
            if 'valueBoolean' in p:
                flat[name] = p['valueBoolean']
            elif 'valueString' in p:
                flat[name] = p['valueString']

        assert flat.get('result') is True, 'cdr.pdhc requires Boolean result'
        assert isinstance(flat.get('display'), str), \
            'cdr.pdhc logs display field on the validate-code response'

    def test_negative_result_is_http_200_not_4xx(self, client):
        """``PlanClient.validate_code`` treats non-200 as transient
        (caches a ``_status`` and returns ``result: False``) — but a
        legitimate ``not adopted`` answer MUST come back as HTTP 200
        with ``result: False`` in the body, so cdr.pdhc reaches a
        terminal plan_miss verdict rather than retrying."""
        resp = client.get(
            '/api/v1/ValueSet/$validate-code',
            query_string={'system': 'fake-lib-no-one-will-name-this', 'code': 'x'},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        flat = {
            p['name']: p.get('valueBoolean', p.get('valueString'))
            for p in body['parameter']
        }
        assert flat['result'] is False


# ===========================================================================
# §6.7 — CapabilityStatement truth-up: new ValueSet/CodeSystem/ConceptMap
# surface is declared accurately; explicitly-unsupported ops are documented.
# ===========================================================================
class TestCapability67Declares:
    def _by_type(self, body):
        rest = body['rest'][0]
        return {r['type']: r for r in rest['resource']}

    def _op_names(self, resource_entry):
        return {op['name'] for op in resource_entry.get('operation', [])}

    def test_valueset_declares_expand_and_validate_code(self, client):
        body = client.get('/api/v1/metadata').get_json()
        vs = self._by_type(body).get('ValueSet')
        assert vs is not None
        ops = self._op_names(vs)
        assert 'expand' in ops
        assert 'validate-code' in ops
        # Should mention both the global cdr.pdhc shim AND the scoped
        # FHIR semantics so a future maintainer sees the dual contract.
        doc = next(
            op['documentation'] for op in vs['operation']
            if op['name'] == 'validate-code'
        )
        assert 'cdr.pdhc' in doc
        assert 'scoped' in doc

    def test_codesystem_declares_lookup_with_termbank_delegation(self, client):
        body = client.get('/api/v1/metadata').get_json()
        cs = self._by_type(body).get('CodeSystem')
        assert cs is not None
        assert 'lookup' in self._op_names(cs)
        doc = next(op['documentation'] for op in cs['operation']
                   if op['name'] == 'lookup')
        assert 'termbank' in doc.lower()
        # Documentation should call out the local-id rule (Concept.guid)
        assert 'plan-pdhc-local' in cs['documentation']

    def test_conceptmap_exists_with_translate(self, client):
        body = client.get('/api/v1/metadata').get_json()
        cm = self._by_type(body).get('ConceptMap')
        assert cm is not None
        assert 'translate' in self._op_names(cm)
        # Documentation should call out the id and bidirectionality.
        assert 'plan-pdhc-canonical-bindings' in cm['documentation']
        assert 'bidirectional' in cm['documentation'].lower()

    def test_unsupported_operations_explicitly_documented(self, client):
        """Per spec §7 / ADR DoD: $subsumes, is-a filters, and
        hierarchical properties must be declared as deliberately
        excluded (a CapabilityStatement that claims them and fails
        is worse than one that honestly excludes them)."""
        body = client.get('/api/v1/metadata').get_json()
        # Search across every resource entry's documentation for the
        # explicit-non-goals block.
        all_docs = '\n\n'.join(
            r.get('documentation', '') for r in body['rest'][0]['resource']
        )
        assert 'EXPLICITLY UNSUPPORTED' in all_docs.upper() \
            or 'subsumes' in all_docs.lower()
        for marker in ('subsumes', 'is-a', 'hierarch'):
            assert marker in all_docs.lower(), \
                f'§7 non-goal {marker!r} not declared in CapabilityStatement'


class TestCapability67EndpointsList:
    def test_new_fhir_routes_appear_in_endpoints(self, client):
        body = client.get('/api/v1/endpoints').get_json()
        paths = {f"{ep['method']} {ep['path']}" for ep in body['endpoints']}
        # Spot-check one per new resource family
        assert any('/ValueSet/<guid>/$expand' in p for p in paths)
        assert any('/CodeSystem/$lookup' in p for p in paths)
        assert any('/ConceptMap/$translate' in p for p in paths)
        assert any('/ConceptMap/<id>' in p for p in paths)

    def test_planDefinition_expand_documents_NOT_terminology(self, client):
        body = client.get('/api/v1/endpoints').get_json()
        pd_expand = next(
            ep for ep in body['endpoints']
            if ep['path'].endswith('/PlanDefinition/<fhir_id>/$expand')
        )
        # The §6 work added a callout that PlanDefinition $expand isn't
        # the terminology $expand. Future readers shouldn't confuse them.
        assert 'NOT the FHIR ValueSet $expand' in pd_expand['description']
