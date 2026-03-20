"""Tests for FHIR service serialization."""
import pytest
from app.models.fhir_models import PlanDefinition
from app.services.fhir_service import FHIRService


class TestFHIRService:
    def test_basic_serialization(self, app):
        with app.app_context():
            pd = PlanDefinition(
                title='Test Plan',
                name='test_plan',
                status='draft',
                version='1.0.0',
            )
            resource = FHIRService.create_fhir_plandefinition(pd)

            assert resource['resourceType'] == 'PlanDefinition'
            assert resource['title'] == 'Test Plan'
            assert resource['name'] == 'test_plan'
            assert resource['status'] == 'draft'
            assert resource['version'] == '1.0.0'

    def test_defaults(self, app):
        with app.app_context():
            pd = PlanDefinition(title='Defaults Test')
            resource = FHIRService.create_fhir_plandefinition(pd)

            assert resource['type']['coding'][0]['code'] == 'clinical-protocol'
            assert resource['subjectCodeableConcept']['coding'][0]['code'] == 'Patient'
            assert resource['version'] == '1.0.0'

    def test_goals_and_actions_included(self, app):
        with app.app_context():
            pd = PlanDefinition(
                title='With Content',
                goal='[{"description": "test goal"}]',
                action='[{"title": "test action"}]',
            )
            resource = FHIRService.create_fhir_plandefinition(pd)

            assert 'goal' in resource
            assert len(resource['goal']) == 1
            assert 'action' in resource
            assert len(resource['action']) == 1

    def test_identifier_and_url(self, app):
        with app.app_context():
            pd = PlanDefinition(title='ID Test', name='id_test')
            resource = FHIRService.create_fhir_plandefinition(pd)

            assert resource['identifier'][0]['system'] == 'https://pdhc.se/plan-definitions'
            assert 'url' in resource

    def test_optional_fields_omitted_when_empty(self, app):
        with app.app_context():
            pd = PlanDefinition(title='Minimal')
            resource = FHIRService.create_fhir_plandefinition(pd)

            assert 'publisher' not in resource
            assert 'description' not in resource
            assert 'effectivePeriod' not in resource
