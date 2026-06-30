"""#332 — PlanDefinition canonical URL uses fhir_canonical_url() like
the terminology resources.

Pre-#332 the URL was `https://pdhc.se/PlanDefinition/<id>` while
CodeSystem / ValueSet / ConceptMap used
`{PLAN_BASE}/fhir/{Resource}/{id}` (per ADR D3). Hard cutover: the new
URL is `https://plan.pdhc.se/fhir/PlanDefinition/<id>`. No back-compat
shim. If an external consumer depends on the old form, they must
update — there is no transitional redirect.
"""
from __future__ import annotations

import pytest

from app import db as _db
from app.models.concept_models import PLAN_BASE, fhir_canonical_url
from app.models.fhir_models import PlanDefinition
from app.services.fhir_service import FHIRService


@pytest.fixture
def saved_plandef(app):
    with app.app_context():
        pd = PlanDefinition(title='Canonical URL Test', name='cu_test')
        _db.session.add(pd)
        _db.session.commit()
        # Touch fhir_id (the @property triggers generation/persistence) by
        # using the model's serializer instead of accessing it directly.
        yield pd
        _db.session.delete(pd)
        _db.session.commit()


class TestPlanDefinitionURLMatchesTerminologyShape:
    def test_create_emits_plan_pdhc_se_fhir_form(self, app, saved_plandef):
        with app.app_context():
            pd = PlanDefinition.query.get(saved_plandef.id)
            resource = FHIRService.create_fhir_plandefinition(pd)
            expected = fhir_canonical_url('PlanDefinition', pd.fhir_id)
            assert resource['url'] == expected, (
                f'PlanDefinition.url should match fhir_canonical_url() shape; '
                f'got {resource["url"]!r}'
            )

    def test_url_starts_with_plan_base_fhir(self, app, saved_plandef):
        with app.app_context():
            pd = PlanDefinition.query.get(saved_plandef.id)
            resource = FHIRService.create_fhir_plandefinition(pd)
            assert resource['url'].startswith(f'{PLAN_BASE}/fhir/PlanDefinition/'), (
                'PlanDefinition canonical URL must align with the terminology '
                'resources (PLAN_BASE + /fhir/{Resource}/{id}).'
            )

    def test_legacy_pdhc_se_shape_no_longer_emitted(self, app, saved_plandef):
        with app.app_context():
            pd = PlanDefinition.query.get(saved_plandef.id)
            resource = FHIRService.create_fhir_plandefinition(pd)
            # Hard cutover: no plain `https://pdhc.se/PlanDefinition/` form.
            assert not resource['url'].startswith('https://pdhc.se/PlanDefinition/')
