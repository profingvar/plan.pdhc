import json
from collections import OrderedDict
from datetime import datetime, timezone

from app.models.forms_models import Questionnaire

PLAN_BASE = "https://plan.pdhc.se"


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

        # Action (from stored JSON) — resolve form actions to definitionCanonical
        if plandef.action:
            try:
                actions = json.loads(plandef.action)
                if isinstance(actions, list):
                    fhir_actions = []
                    for act in actions:
                        if act.get('is_form') and act.get('form_guid'):
                            fhir_act = {
                                'title': act.get('title', ''),
                                'type': {
                                    'coding': [{
                                        'system': 'http://terminology.hl7.org/CodeSystem/action-type',
                                        'code': 'collect-information',
                                        'display': 'Collect information',
                                    }]
                                },
                                'definitionCanonical': f'{PLAN_BASE}/api/v1/forms/{act["form_guid"]}',
                            }
                            if act.get('description'):
                                fhir_act['description'] = act['description']
                            # Timing
                            if act.get('timing_type') == 'repeat' and act.get('timing_frequency'):
                                repeat = {
                                    'frequency': act['timing_frequency'],
                                    'period': act.get('timing_period', 1),
                                    'periodUnit': act.get('timing_period_unit', 'd'),
                                }
                                bounds_mode = act.get('timing_bounds_mode')
                                if bounds_mode == 'count' and act.get('timing_bounds_count'):
                                    repeat['count'] = act['timing_bounds_count']
                                elif bounds_mode == 'duration' and act.get('timing_bounds_duration_value'):
                                    unit = act.get('timing_bounds_duration_unit') or 'mo'
                                    repeat['boundsDuration'] = {
                                        'value': act['timing_bounds_duration_value'],
                                        'unit': unit,
                                        'system': 'http://unitsofmeasure.org',
                                        'code': unit,
                                    }
                                fhir_act['timingTiming'] = {'repeat': repeat}
                            fhir_actions.append(fhir_act)
                        else:
                            fhir_actions.append(act)
                    if fhir_actions:
                        resource['action'] = fhir_actions
            except (json.JSONDecodeError, TypeError):
                pass

        return resource
