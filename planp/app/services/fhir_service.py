import json
from collections import OrderedDict
from datetime import datetime, timezone

from app.models.forms_models import Questionnaire


class FHIRService:
    """Builds FHIR R5 PlanDefinition JSON from a PlanDefinition model instance."""

    HL7_PLAN_DEF_TYPE_SYSTEM = 'http://terminology.hl7.org/CodeSystem/plan-definition-type'

    @staticmethod
    def create_fhir_plandefinition(plandef):
        now = datetime.now(timezone.utc).isoformat()
        fhir_id = plandef.fhir_id

        resource = OrderedDict()
        resource['resourceType'] = 'PlanDefinition'
        resource['id'] = fhir_id
        resource['meta'] = {
            'versionId': str(plandef.vers_number if hasattr(plandef, 'vers_number') else 1),
            'lastUpdated': now,
        }
        resource['identifier'] = [{
            'system': 'https://pdhc.se/plan-definitions',
            'value': plandef.name or fhir_id,
        }]
        resource['url'] = f'https://pdhc.se/PlanDefinition/{fhir_id}'
        resource['version'] = plandef.version or '1.0.0'
        resource['name'] = plandef.name
        resource['title'] = plandef.title
        resource['status'] = plandef.status or 'draft'

        # Type
        type_code = plandef.type or 'clinical-protocol'
        resource['type'] = {
            'coding': [{
                'system': FHIRService.HL7_PLAN_DEF_TYPE_SYSTEM,
                'code': type_code,
            }]
        }

        # Subject
        subject = plandef.subject_type or 'Patient'
        resource['subjectCodeableConcept'] = {
            'coding': [{
                'system': 'http://hl7.org/fhir/resource-types',
                'code': subject,
            }]
        }

        # Optional descriptive fields
        if plandef.publisher:
            resource['publisher'] = plandef.publisher
        if plandef.description:
            resource['description'] = plandef.description
        if plandef.purpose:
            resource['purpose'] = plandef.purpose
        if plandef.usage:
            resource['usage'] = plandef.usage
        if plandef.copyright:
            resource['copyright'] = plandef.copyright

        # Dates
        if plandef.approval_date:
            resource['approvalDate'] = plandef.approval_date.isoformat()
        if plandef.last_review_date:
            resource['lastReviewDate'] = plandef.last_review_date.isoformat()
        if plandef.effective_period_start or plandef.effective_period_end:
            ep = {}
            if plandef.effective_period_start:
                ep['start'] = plandef.effective_period_start.isoformat()
            if plandef.effective_period_end:
                ep['end'] = plandef.effective_period_end.isoformat()
            resource['effectivePeriod'] = ep

        # Contributors
        for role in ('author', 'editor', 'reviewer', 'endorser'):
            val = getattr(plandef, role, None)
            if val:
                resource[role] = [{'name': val}]

        # Related artifact
        if plandef.related_artifact:
            try:
                ra = json.loads(plandef.related_artifact)
                resource['relatedArtifact'] = ra if isinstance(ra, list) else [ra]
            except (json.JSONDecodeError, TypeError):
                pass

        # Library
        if plandef.library:
            resource['library'] = [plandef.library]

        # Goal (from stored JSON)
        if plandef.goal:
            try:
                goals = json.loads(plandef.goal)
                if isinstance(goals, list):
                    resource['goal'] = goals
            except (json.JSONDecodeError, TypeError):
                pass

        # Action (from stored JSON)
        if plandef.action:
            try:
                actions = json.loads(plandef.action)
                if isinstance(actions, list):
                    resource['action'] = actions
            except (json.JSONDecodeError, TypeError):
                pass

        # Questionnaire references — add collect-information actions for
        # any Questionnaires produced from this PlanDefinition.
        produced = Questionnaire.query.filter(
            Questionnaire.production_key == f'plandef:{plandef.guid}',
            Questionnaire.status == 'active',
        ).order_by(Questionnaire.form_guid, Questionnaire.version.desc()).all()

        # Deduplicate to latest version per form_guid
        seen_forms = set()
        for q in produced:
            if q.form_guid in seen_forms:
                continue
            seen_forms.add(q.form_guid)
            action_entry = {
                'title': q.title,
                'type': {
                    'coding': [{
                        'system': 'http://terminology.hl7.org/CodeSystem/action-type',
                        'code': 'collect-information',
                        'display': 'Collect information',
                    }]
                },
                'definitionCanonical': f'Questionnaire/{q.form_guid}',
            }
            resource.setdefault('action', []).append(action_entry)

        return resource
