import json
from collections import OrderedDict
from datetime import datetime, timezone

from app.models.concept_models import fhir_canonical_url
from app.models.forms_models import Questionnaire
from app.services import continuous_timing, diagnosis_review

PLAN_BASE = "https://plan.pdhc.se"


class FHIRService:
    """Builds FHIR R5 PlanDefinition JSON from a PlanDefinition model instance."""

    HL7_PLAN_DEF_TYPE_SYSTEM = 'http://terminology.hl7.org/CodeSystem/plan-definition-type'

    @staticmethod
    def form_timing_timing(act):
        """timingTiming for a form (or diagnosis-review) action, or None."""
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
            return {'repeat': repeat}
        return None

    #: Timing.repeat.durationUnit is restricted to these (UnitsOfTime).
    UNITS_OF_TIME = ('s', 'min', 'h', 'd', 'wk', 'mo', 'a')

    @staticmethod
    def measurement_timing(act):
        """timingTiming for a measurement action, or None (2026-11-20).

        The repeat part is exactly what a form gets. `duration_value` /
        `duration_unit` is how long ONE occurrence lasts, which is what FHIR's
        `Timing.repeat.duration` means. It is not the length of the plan; that
        is `boundsDuration` or `count`. A `once` activity is `count: 1`.
        """
        timing = FHIRService.form_timing_timing(act)
        if timing is None and act.get('timing_type') == 'once':
            timing = {'repeat': {'count': 1}}
        if timing is None:
            return None
        unit = act.get('duration_unit')
        try:
            value = float(act.get('duration_value'))
        except (TypeError, ValueError):
            value = None
        if value and value > 0 and unit in FHIRService.UNITS_OF_TIME:
            timing['repeat']['duration'] = int(value) if value.is_integer() else value
            timing['repeat']['durationUnit'] = unit
        return timing

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
        # Canonical URL uses the platform-wide form per ADR D3 — same shape
        # as CodeSystem/ValueSet/ConceptMap. Pre-#332 this emitted
        # `https://pdhc.se/PlanDefinition/<id>` (two divergent schemes).
        resource['url'] = fhir_canonical_url('PlanDefinition', fhir_id)
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
                            timing = FHIRService.form_timing_timing(act)
                            if timing:
                                fhir_act['timingTiming'] = timing
                            fhir_actions.append(fhir_act)
                        elif diagnosis_review.is_diagnosis_review(act):
                            # #984: clinician step opening an icd11 diagnosis
                            # session; timing exactly as for forms.
                            fhir_actions.append(diagnosis_review.to_fhir_action(
                                act, FHIRService.form_timing_timing(act)))
                        else:
                            # 2026-11-20: a measurement action carried its
                            # schedule only in plan.pdhc's own fields
                            # (timing_frequency, timing_bounds_count, ...),
                            # so a FHIR reader saw no Timing at all. Those
                            # fields stay for existing readers; timingTiming
                            # is added beside them.
                            fhir_act = dict(act)
                            if continuous_timing.is_continuous(act):
                                # 2026-11-20: ordered once, lasting the active
                                # period; the stream's expected interval is an
                                # extension, never a frequency.
                                timing = continuous_timing.fhir_timing(act)
                                ext = continuous_timing.fhir_extension(act)
                                if ext:
                                    fhir_act['extension'] = (fhir_act.get('extension') or []) + [ext]
                            else:
                                timing = FHIRService.measurement_timing(act)
                            if timing:
                                fhir_act['timingTiming'] = timing
                            fhir_actions.append(fhir_act)
                    if fhir_actions:
                        resource['action'] = fhir_actions
            except (json.JSONDecodeError, TypeError):
                pass

        return resource
