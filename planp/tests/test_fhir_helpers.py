"""Tests for the §6.5 / §6.6 foundation: URL builder, version helper,
and shared FHIR-shape helpers in ``app/api/fhir_helpers.py``.

Plus the ADR D3 / Risk §9.3 lint: no file other than the URL helper may
hardcode the ``/fhir/`` scheme.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from flask import Flask

from app.api.fhir_helpers import (
    FHIR_CONTENT_TYPE,
    fhir_json_response,
    operation_outcome,
    parameters_response,
    parse_parameters_body,
)
from app.models.concept_models import (
    LOCAL_CODESYSTEM_ID,
    PLAN_BASE,
    fhir_canonical_url,
    fhir_version,
)
# ADR D5 — fast-layer validator. If this import fails, run
# `pip install -r requirements.txt` in the venv.
from fhir.resources.parameters import Parameters as FHIRParameters
from fhir.resources.operationoutcome import OperationOutcome as FHIROperationOutcome


# ---------------------------------------------------------------------------
# §6.6 — URL builder + version helper
# ---------------------------------------------------------------------------
class TestFHIRCanonicalURL:
    def test_form_matches_adr_d3(self):
        assert fhir_canonical_url('ValueSet', 'abc-123') == \
            f'{PLAN_BASE}/fhir/ValueSet/abc-123'

    def test_local_codesystem_id_is_stable(self):
        # ADR D2: id == 'plan-pdhc-local'
        assert LOCAL_CODESYSTEM_ID == 'plan-pdhc-local'
        assert fhir_canonical_url('CodeSystem', LOCAL_CODESYSTEM_ID) == \
            f'{PLAN_BASE}/fhir/CodeSystem/plan-pdhc-local'

    def test_conceptmap_form(self):
        assert fhir_canonical_url('ConceptMap', 'foo') == \
            f'{PLAN_BASE}/fhir/ConceptMap/foo'


class TestFHIRVersion:
    def test_returns_str_of_vers_number(self):
        class Stub:
            vers_number = 7
        assert fhir_version(Stub()) == '7'

    def test_defaults_to_one_when_missing(self):
        class Stub:
            pass
        assert fhir_version(Stub()) == '1'

    def test_defaults_to_one_when_none(self):
        class Stub:
            vers_number = None
        assert fhir_version(Stub()) == '1'


# ---------------------------------------------------------------------------
# §6.5 — shared helpers
# ---------------------------------------------------------------------------
@pytest.fixture()
def helper_app():
    """Minimal Flask app for helpers that touch Flask request context."""
    app = Flask(__name__)
    return app


class TestOperationOutcome:
    def test_shape_and_content_type(self, helper_app):
        with helper_app.test_request_context():
            resp, status = operation_outcome(
                'error', 'required', 'missing param', 400,
            )
        assert status == 400
        assert resp.headers['Content-Type'] == FHIR_CONTENT_TYPE
        body = resp.get_json()
        assert body['resourceType'] == 'OperationOutcome'
        assert body['issue'][0]['severity'] == 'error'
        assert body['issue'][0]['code'] == 'required'
        assert body['issue'][0]['details']['text'] == 'missing param'


class TestD5FastValidator:
    """Confirm the D5 fast-layer (fhir.resources) is wired and validates
    the shapes our helpers emit. Used as the canonical fhir.resources
    smoke test so a missing/broken install fails loud here, not in
    every §6.x test file."""

    def test_parameters_response_validates_against_R5_model(self):
        body = parameters_response(
            result=True, message='ok', system='loinc', code='4548-4',
        )
        # Round-trip through the pydantic model — raises on shape error
        validated = FHIRParameters.model_validate(body)
        assert validated.parameter[0].name == 'result'

    def test_operation_outcome_validates_against_R5_model(self, helper_app):
        with helper_app.test_request_context():
            resp, _ = operation_outcome('error', 'required', 'missing', 400)
        body = resp.get_json()
        validated = FHIROperationOutcome.model_validate(body)
        assert validated.issue[0].severity == 'error'


class TestParametersResponse:
    def test_basic_result_only(self):
        body = parameters_response(result=True)
        assert body['resourceType'] == 'Parameters'
        assert body['parameter'] == [{'name': 'result', 'valueBoolean': True}]

    def test_string_fields_append(self):
        body = parameters_response(result=False, message='nope', code='X')
        names = {p['name']: p for p in body['parameter']}
        assert names['result']['valueBoolean'] is False
        assert names['message']['valueString'] == 'nope'
        assert names['code']['valueString'] == 'X'

    def test_none_fields_omitted(self):
        body = parameters_response(result=True, ref_via='Concept', display=None)
        names = [p['name'] for p in body['parameter']]
        assert 'display' not in names
        assert 'ref_via' in names

    def test_bool_field_becomes_valueBoolean(self):
        body = parameters_response(result=True, extra_flag=False)
        names = {p['name']: p for p in body['parameter']}
        assert 'valueBoolean' in names['extra_flag']
        assert names['extra_flag']['valueBoolean'] is False


class TestFHIRJSONResponse:
    def test_sets_fhir_content_type(self, helper_app):
        with helper_app.test_request_context():
            resp, status = fhir_json_response({'resourceType': 'ValueSet'})
        assert status == 200
        assert resp.headers['Content-Type'] == FHIR_CONTENT_TYPE
        assert resp.get_json() == {'resourceType': 'ValueSet'}


class TestParseParametersBody:
    def test_parses_valid_body(self, helper_app):
        body = {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': 'system', 'valueString': 'loinc'},
                {'name': 'code', 'valueString': '4548-4'},
                {'name': 'result', 'valueBoolean': True},
            ],
        }
        out = parse_parameters_body(body)
        assert out == {'system': 'loinc', 'code': '4548-4', 'result': True}

    def test_ignores_non_parameters_body(self, helper_app):
        out = parse_parameters_body({'resourceType': 'OperationOutcome'})
        assert out == {}

    def test_empty_when_no_body(self, helper_app):
        with helper_app.test_request_context('/', method='POST'):
            out = parse_parameters_body()
        assert out == {}

    def test_accepts_valueCode_and_valueUrl(self, helper_app):
        body = {
            'resourceType': 'Parameters',
            'parameter': [
                {'name': 'code', 'valueCode': 'final'},
                {'name': 'url', 'valueUrl': 'https://x/'},
            ],
        }
        out = parse_parameters_body(body)
        assert out == {'code': 'final', 'url': 'https://x/'}

    def test_skips_anonymous_parameters(self, helper_app):
        body = {
            'resourceType': 'Parameters',
            'parameter': [{'valueString': 'no-name'}, {'name': 'x', 'valueString': 'ok'}],
        }
        out = parse_parameters_body(body)
        assert out == {'x': 'ok'}


# ---------------------------------------------------------------------------
# ADR D3 / Risk §9.3 lint — no file other than the URL helper itself may
# hardcode the **plan.pdhc** ``/fhir/`` canonical-URL scheme. External
# canonical URLs (HL7 StructureDefinitions, other sibling services like
# contract.pdhc) are fine and ignored here.
#
# If this test fails, move the offending string into a call to
# ``fhir_canonical_url()`` in app/models/concept_models.py.
# ---------------------------------------------------------------------------
class TestURLSchemeCentralization:
    """Forbid hardcoded plan.pdhc canonical-URL construction outside the
    helper. The patterns this catches are:
      - 'https://plan.pdhc.se/fhir/...'
      - f'{PLAN_BASE}/fhir/...'
      - 'plan.pdhc.se/fhir/...'  (any scheme)
    HL7's own 'http://hl7.org/fhir/...' URLs are external canonicals and
    are NOT flagged — they reference the HL7 spec, not our identity.
    """

    _BAD_PATTERNS = (
        'plan.pdhc.se/fhir/',
        'PLAN_BASE}/fhir/',
        'PLAN_BASE }/fhir/',
        'PLAN_BASE)/fhir/',
        '{plan_base}/fhir/',
    )

    def test_no_other_file_hardcodes_plan_fhir_url(self):
        app_dir = Path(__file__).parent.parent / 'app'
        url_helper = app_dir / 'models' / 'concept_models.py'
        offenders: list[str] = []
        for py in app_dir.rglob('*.py'):
            if py.resolve() == url_helper.resolve():
                continue
            try:
                src = py.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            for pat in self._BAD_PATTERNS:
                if pat in src:
                    offenders.append(f'{py.relative_to(app_dir)}: '
                                     f'contains {pat!r}')
                    break
        assert offenders == [], (
            'Hardcoded plan.pdhc /fhir/ URL found outside the helper:\n  '
            + '\n  '.join(offenders)
            + '\nImport fhir_canonical_url() from app.models.concept_models.'
        )
