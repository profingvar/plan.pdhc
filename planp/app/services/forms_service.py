"""
Forms service — FHIR Questionnaire production, versioning, and retrieval.

Consolidated from forms.pdhc: resolve concepts directly from DB (no HTTP),
build FHIR Questionnaire, validate, version, publish, catalogue, history.
"""
import hashlib
import json

from sqlalchemy import func
from app import db
from app.models.forms_models import Questionnaire, QuestionnaireItem, QuestionnaireResponse
from app.models.concept_models import Concept, ValueSet, ValueSetValue, ValueCatalog
from app.models.fhir_models import PlanDefinition
from app.models.activity_models import PlanDefinitionGoal, PlanDefinitionActivity, Transaction


# ---------------------------------------------------------------------------
# Response type mapping (PlanDef Builder names → internal question types)
# ---------------------------------------------------------------------------

RESPONSE_TYPE_MAP = {
    'single choice': 'single_choice',
    'envalsfråga': 'single_choice',
    'multiple choice': 'multiple_choice',
    'flervalsfråga': 'multiple_choice',
    'quantity': 'numeric',
    'numeric': 'numeric',
    'numerisk': 'numeric',
    'decimal': 'numeric',
    'integer': 'slider',
    'slider': 'slider',
    'text': 'text',
    'string': 'text',
    'fritext': 'text',
    'boolean': 'boolean',
}

# Internal question type → FHIR item type
FHIR_TYPE_MAP = {
    'text': 'string',
    'numeric': 'decimal',
    'slider': 'integer',
    'single_choice': 'choice',
    'multiple_choice': 'choice',
    'boolean': 'boolean',
}

SUPPORTED_TYPES = set(FHIR_TYPE_MAP.keys())

VALID_STATUSES = {'draft', 'active', 'retired', 'unknown'}
VALID_ITEM_TYPES = {'group', 'display', 'boolean', 'decimal', 'integer', 'date',
                    'dateTime', 'time', 'string', 'text', 'url', 'choice',
                    'open-choice', 'attachment', 'reference', 'quantity'}


# ---------------------------------------------------------------------------
# Error classes
# ---------------------------------------------------------------------------

class FormsError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class QuestionServiceError(FormsError):
    pass


class BuildError(FormsError):
    pass


class ValidationError(FormsError):
    def __init__(self, message, status_code=422):
        super().__init__(message, status_code)


class PublishError(FormsError):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)


class ImmutabilityError(FormsError):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)


class DefinitionError(FormsError):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)


class HistoryError(FormsError):
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)


# ===========================================================================
# 1. ResolveQuestionSet — direct DB queries (no HTTP)
# ===========================================================================

def resolve_question_set(source_id, source_type='concept_guids'):
    """Resolve concepts into question items for FHIR Questionnaire building.

    Args:
        source_id: list of concept GUIDs or a PlanDefinition GUID
        source_type: 'concept_guids' or 'plandefinition'
    """
    if source_type == 'plandefinition':
        return _resolve_from_plandefinition(source_id)
    elif source_type == 'concept_guids':
        return _resolve_from_concept_guids(source_id)
    else:
        raise QuestionServiceError(f"Unknown source_type: '{source_type}'")


def _resolve_from_plandefinition(plandef_guid):
    """Resolve all concepts referenced by a PlanDefinition."""
    plandef = PlanDefinition.query.filter_by(guid=plandef_guid).first()
    if not plandef:
        plandef = PlanDefinition.query.filter_by(fhir_id=plandef_guid).first()
    if not plandef:
        raise QuestionServiceError(f"PlanDefinition '{plandef_guid}' not found", 404)

    # Collect concept GUIDs from goals and activity transactions
    concept_guids = []
    seen = set()

    # From activities → transactions
    activity_links = PlanDefinitionActivity.query.filter_by(
        plandefinition_guid=plandef.guid
    ).order_by(PlanDefinitionActivity.sort_order).all()

    for link in activity_links:
        transactions = Transaction.query.filter_by(
            activity_guid=link.activity_guid
        ).order_by(Transaction.sort_order).all()
        for txn in transactions:
            if txn.concept_guid and txn.concept_guid not in seen:
                concept_guids.append(txn.concept_guid)
                seen.add(txn.concept_guid)

    # From goals
    goals = PlanDefinitionGoal.query.filter_by(
        plandefinition_guid=plandef.guid
    ).order_by(PlanDefinitionGoal.sort_order).all()
    for goal in goals:
        if goal.concept_guid and goal.concept_guid not in seen:
            concept_guids.append(goal.concept_guid)
            seen.add(goal.concept_guid)

    if not concept_guids:
        raise QuestionServiceError(
            f"PlanDefinition '{plandef_guid}' has no concept references", 400
        )

    items = _resolve_concepts(concept_guids)

    return {
        'title': plandef.title or '',
        'description': plandef.description or '',
        'source_plandefinition_guid': plandef_guid,
        'items': items,
    }


def _resolve_from_concept_guids(concept_guids):
    """Resolve a list of concept GUIDs into question items."""
    if not concept_guids or not isinstance(concept_guids, list):
        raise QuestionServiceError("concept_guids must be a non-empty list")

    items = _resolve_concepts(concept_guids)
    return {'title': '', 'description': '', 'items': items}


def _resolve_concepts(concept_guids):
    """Fetch concepts from DB and normalize to question items."""
    items = []
    for guid in concept_guids:
        concept = Concept.query.filter_by(guid=guid).first()
        if not concept:
            raise QuestionServiceError(f"Concept '{guid}' not found", 404)
        item = _concept_to_question_item(concept)
        items.append(item)
    return items


def _concept_to_question_item(concept):
    """Map a Concept ORM object to the internal question item schema."""
    display_text = concept.concept_display_text or concept.concept_name

    # Determine question type from response_type relationship
    response_type_name = ''
    if concept.response_type_rel:
        response_type_name = (concept.response_type_rel.response_type_name or
                              concept.response_type_rel.response_type_display_text or '')

    question_type = _map_response_type(response_type_name)

    item = {
        'link_id': concept.guid,
        'text': display_text,
        'type': question_type,
        'required': False,
        'concept_guid': concept.guid,
        'concept_name': concept.concept_name,
    }

    # Canonical code reference
    if concept.canonical_refnumber:
        item['code'] = concept.canonical_refnumber
    if concept.canonical_lib_rel:
        url = concept.canonical_lib_rel.canonical_lib_url
        if url:
            item['code_system'] = url

    # Unit
    if concept.unit_rel:
        unit_text = concept.unit_rel.unit_display_text or concept.unit_rel.unit_name or ''
        if unit_text:
            item['unit'] = unit_text

    # Range
    if concept.range_low is not None:
        item['min_value'] = concept.range_low
    if concept.range_high is not None:
        item['max_value'] = concept.range_high

    # Anchor text
    if concept.anchor_low_text:
        item['anchor_low_text'] = concept.anchor_low_text
    if concept.anchor_high_text:
        item['anchor_high_text'] = concept.anchor_high_text

    # ValueSet values for choice types
    if question_type in ('single_choice', 'multiple_choice') and concept.valueset:
        vsv_entries = (
            ValueSetValue.query
            .filter_by(valueset_guid=concept.valueset)
            .order_by(ValueSetValue.sort_order)
            .all()
        )
        if vsv_entries:
            options = []
            for vsv in vsv_entries:
                val = ValueCatalog.query.filter_by(guid=vsv.value_guid).first()
                if val:
                    options.append({
                        'value': val.guid,
                        'label': val.value_display_text or val.value_name or '',
                        'code': val.canonical_refnumber or '',
                    })
            item['options'] = options

    return item


def _map_response_type(response_type_name):
    """Map response_type name to internal question type."""
    if not response_type_name:
        return 'text'

    normalized = response_type_name.strip().lower()
    mapped = RESPONSE_TYPE_MAP.get(normalized)
    if mapped:
        return mapped

    if 'choice' in normalized or 'val' in normalized:
        if 'multi' in normalized or 'fler' in normalized:
            return 'multiple_choice'
        return 'single_choice'
    if 'quant' in normalized or 'numer' in normalized or 'decimal' in normalized:
        return 'numeric'
    if 'int' in normalized or 'slider' in normalized:
        return 'slider'
    if 'bool' in normalized:
        return 'boolean'

    return 'text'


# ===========================================================================
# 2. BuildFhirQuestionnaire
# ===========================================================================

def build_fhir_questionnaire(form_guid, version, status, meta, external_questions):
    """Build a FHIR R5 Questionnaire JSON from resolved concept items."""
    title = meta.get('title', '')
    description = meta.get('description', '')
    items = external_questions.get('items', [])

    fhir_items = [_build_fhir_item(item) for item in items]

    questionnaire = {
        'resourceType': 'Questionnaire',
        'id': form_guid,
        'version': str(version),
        'status': status,
        'title': title,
        'description': description,
        'item': fhir_items,
    }

    source_pd = external_questions.get('source_plandefinition_guid')
    if source_pd:
        questionnaire['derivedFrom'] = [f'PlanDefinition/{source_pd}']

    return questionnaire


def _build_fhir_item(item):
    """Map a resolved concept item to a FHIR Questionnaire.item."""
    ext_type = item.get('type', '')
    if ext_type not in SUPPORTED_TYPES:
        raise BuildError(f"Unsupported question type: '{ext_type}'")

    link_id = item.get('link_id')
    text = item.get('text')
    if not link_id or not text:
        raise BuildError("Item missing required fields: link_id and text")

    fhir_type = FHIR_TYPE_MAP[ext_type]
    fhir_item = {
        'linkId': link_id,
        'text': text,
        'type': fhir_type,
        'required': item.get('required', False),
    }

    # FHIR code binding
    if item.get('code') or item.get('code_system'):
        code_entry = {}
        if item.get('code_system'):
            code_entry['system'] = item['code_system']
        if item.get('code'):
            code_entry['code'] = item['code']
        if item.get('concept_name'):
            code_entry['display'] = item.get('text', '')
        fhir_item['code'] = [code_entry]

    # Choice items
    if ext_type in ('single_choice', 'multiple_choice'):
        options = item.get('options')
        if not options or not isinstance(options, list):
            raise BuildError(f"Choice item '{link_id}' missing 'options' array")
        fhir_item['answerOption'] = [_build_answer_option(opt, item) for opt in options]
        fhir_item['repeats'] = (ext_type == 'multiple_choice')

    # Numeric/slider extensions
    if ext_type in ('numeric', 'slider'):
        extensions = []
        value_key = 'valueDecimal' if ext_type == 'numeric' else 'valueInteger'

        if item.get('min_value') is not None:
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/minValue',
                value_key: item['min_value'],
            })
        if item.get('max_value') is not None:
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/maxValue',
                value_key: item['max_value'],
            })
        if item.get('default_value') is not None:
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/questionnaire-initialValue',
                value_key: item['default_value'],
            })
        if item.get('anchor_low_text'):
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/questionnaire-sliderStepValue',
                'valueString': item['anchor_low_text'],
            })
        if item.get('anchor_high_text'):
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/maxValue',
                'valueString': item['anchor_high_text'],
            })
        if item.get('unit'):
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/questionnaire-unit',
                'valueCoding': {'display': item['unit']},
            })
        # Add questionnaire-itemControl extension for sliders
        if ext_type == 'slider':
            extensions.append({
                'url': 'http://hl7.org/fhir/StructureDefinition/questionnaire-itemControl',
                'valueCodeableConcept': {
                    'coding': [{
                        'system': 'http://hl7.org/fhir/questionnaire-item-control',
                        'code': 'slider',
                        'display': 'Slider',
                    }]
                },
            })

        if extensions:
            fhir_item['extension'] = extensions

    return fhir_item


def _build_answer_option(opt, item):
    """Build a FHIR answerOption from a resolved value."""
    coding = {
        'code': str(opt.get('value', '')),
        'display': opt.get('label', ''),
    }
    if opt.get('code'):
        coding['code'] = opt['code']
    if item.get('code_system'):
        coding['system'] = item['code_system']
    return {'valueCoding': coding}


# ===========================================================================
# 3. ValidateFhirQuestionnaire
# ===========================================================================

def validate_fhir_questionnaire(fhir_questionnaire):
    """Validate a FHIR Questionnaire dict for structural correctness."""
    if not isinstance(fhir_questionnaire, dict):
        raise ValidationError("Questionnaire must be a JSON object")
    if fhir_questionnaire.get('resourceType') != 'Questionnaire':
        raise ValidationError("resourceType must be 'Questionnaire'")
    if not fhir_questionnaire.get('status'):
        raise ValidationError("Questionnaire must include 'status'")
    if fhir_questionnaire['status'] not in VALID_STATUSES:
        raise ValidationError(
            f"Invalid status '{fhir_questionnaire['status']}'. "
            f"Must be one of: {', '.join(VALID_STATUSES)}"
        )

    items = fhir_questionnaire.get('item', [])
    if not isinstance(items, list):
        raise ValidationError("'item' must be an array")

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"Item at index {i} must be a JSON object")
        if not item.get('linkId'):
            raise ValidationError(f"Item at index {i} missing required 'linkId'")
        if not item.get('text'):
            raise ValidationError(f"Item at index {i} missing required 'text'")
        if not item.get('type'):
            raise ValidationError(f"Item at index {i} missing required 'type'")
        if item['type'] not in VALID_ITEM_TYPES:
            raise ValidationError(f"Item '{item['linkId']}' has invalid type '{item['type']}'")
        if item['type'] == 'choice' and not item.get('answerOption'):
            raise ValidationError(f"Choice item '{item['linkId']}' must have 'answerOption'")

    return True


# ===========================================================================
# 4. CreateOrAppendFormVersion
# ===========================================================================

def create_or_append_form_version(form_guid, content_fingerprint, production_key,
                                   meta, status, fhir_questionnaire):
    """Persist a form version with idempotency and monotonic versioning."""
    if not form_guid:
        form_guid = Questionnaire.generate_guid()

    if not content_fingerprint:
        content_fingerprint = _compute_fingerprint(fhir_questionnaire)

    # Idempotent match
    existing = Questionnaire.query.filter_by(
        form_guid=form_guid, content_fingerprint=content_fingerprint
    ).first()
    if existing:
        return existing.to_dict()

    # Next version
    latest = Questionnaire.query.filter_by(form_guid=form_guid).order_by(
        Questionnaire.version.desc()
    ).first()
    next_version = (latest.version + 1) if latest else 1

    fhir_questionnaire['id'] = form_guid
    fhir_questionnaire['version'] = str(next_version)

    title = meta.get('title', fhir_questionnaire.get('title', ''))
    description = meta.get('description', fhir_questionnaire.get('description', ''))

    questionnaire = Questionnaire(
        form_guid=form_guid,
        version=next_version,
        title=title,
        description=description,
        status=status,
        fhir_json=fhir_questionnaire,
        content_fingerprint=content_fingerprint,
        production_key=production_key,
    )
    db.session.add(questionnaire)
    db.session.flush()

    for item_data in fhir_questionnaire.get('item', []):
        qi = QuestionnaireItem(
            questionnaire_id=questionnaire.id,
            form_guid=form_guid,
            form_version=next_version,
            link_id=item_data.get('linkId', ''),
            text=item_data.get('text', ''),
            type=item_data.get('type', ''),
            required=item_data.get('required', False),
            options=[opt.get('valueCoding', {}) for opt in item_data.get('answerOption', [])]
            if item_data.get('answerOption') else None,
            min_value=_extract_extension_value(item_data, 'minValue'),
            max_value=_extract_extension_value(item_data, 'maxValue'),
            default_value=_extract_extension_value(item_data, 'questionnaire-initialValue'),
        )
        db.session.add(qi)

    db.session.commit()
    return questionnaire.to_dict()


def _compute_fingerprint(fhir_json):
    canonical = json.dumps(fhir_json, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _extract_extension_value(item_data, keyword):
    for ext in item_data.get('extension', []):
        if keyword in ext.get('url', ''):
            for key in ('valueDecimal', 'valueInteger'):
                if key in ext:
                    return ext[key]
    return None


# ===========================================================================
# 5. EnforceLatestVersionImmutability
# ===========================================================================

def enforce_latest_version_immutability(form_guid):
    """Check whether the latest version can be edited (no responses)."""
    latest = Questionnaire.query.filter_by(form_guid=form_guid).order_by(
        Questionnaire.version.desc()
    ).first()
    if not latest:
        raise ImmutabilityError(f"Form '{form_guid}' not found")

    response_count = QuestionnaireResponse.query.filter_by(
        form_guid=form_guid, form_version=latest.version
    ).count()
    can_edit = response_count == 0

    return {
        'form_guid': form_guid,
        'latest_version': latest.version,
        'response_count': response_count,
        'can_edit_latest': can_edit,
        'recommended_action': 'allow_replace_latest' if can_edit else 'create_new_version',
    }


# ===========================================================================
# 6. PublishFormVersion
# ===========================================================================

def publish_form_version(form_guid, version=None):
    """Set status=active for a form version. Does not mutate fhir_json."""
    if version:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid, version=version
        ).first()
    else:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid
        ).order_by(Questionnaire.version.desc()).first()

    if not questionnaire:
        raise PublishError(f"Form version ({form_guid}, v{version}) not found")

    questionnaire.status = 'active'
    db.session.commit()
    return questionnaire.to_dict()


# ===========================================================================
# 7. GetFormCatalogue
# ===========================================================================

def get_form_catalogue(status='active', limit=100, offset=0):
    """Return paginated list of forms (latest version per form_guid)."""
    latest_version = (
        Questionnaire.query
        .with_entities(
            Questionnaire.form_guid,
            func.max(Questionnaire.version).label('max_version')
        )
        .group_by(Questionnaire.form_guid)
        .subquery()
    )

    query = (
        Questionnaire.query
        .join(latest_version,
              (Questionnaire.form_guid == latest_version.c.form_guid) &
              (Questionnaire.version == latest_version.c.max_version))
    )

    if status:
        query = query.filter(Questionnaire.status == status)

    total = query.count()
    forms = query.order_by(Questionnaire.title).offset(offset).limit(limit).all()

    return {
        'forms': [f.to_summary() for f in forms],
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_more': (offset + limit) < total,
    }


# ===========================================================================
# 8. GetFormDefinition
# ===========================================================================

def get_form_definition(form_guid, version=None):
    """Return a specific form version or the latest."""
    if version is not None:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid, version=version
        ).first()
    else:
        questionnaire = Questionnaire.query.filter_by(
            form_guid=form_guid
        ).order_by(Questionnaire.version.desc()).first()

    if not questionnaire:
        raise DefinitionError(f"Form '{form_guid}' version {version or 'latest'} not found")

    return questionnaire.to_dict()


# ===========================================================================
# 9. GetFormVersionHistory
# ===========================================================================

def get_form_version_history(form_guid):
    """Return all versions for a form with response counts and can_edit flag."""
    versions = Questionnaire.query.filter_by(
        form_guid=form_guid
    ).order_by(Questionnaire.version.desc()).all()

    if not versions:
        raise HistoryError(f"Form '{form_guid}' not found")

    response_counts = dict(
        db.session.query(
            QuestionnaireResponse.form_version,
            func.count(QuestionnaireResponse.id)
        ).filter_by(form_guid=form_guid)
        .group_by(QuestionnaireResponse.form_version)
        .all()
    )

    latest = versions[0]
    latest_response_count = response_counts.get(latest.version, 0)

    version_list = [{
        'version': v.version,
        'title': v.title,
        'status': v.status,
        'created_at': v.created_at.isoformat() if v.created_at else None,
        'response_count': response_counts.get(v.version, 0),
    } for v in versions]

    return {
        'form_guid': form_guid,
        'total_versions': len(versions),
        'latest_version': latest.version,
        'latest_status': latest.status,
        'can_edit': latest_response_count == 0,
        'versions': version_list,
    }
