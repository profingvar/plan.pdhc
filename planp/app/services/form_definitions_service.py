"""
Form definitions service — CRUD for FormDefinitions, item management,
production pipeline (FormDefinition → FHIR Questionnaire), and preview.
"""
import re
import uuid
from app import db
from app.models.forms_models import (
    FormDefinition, FormDefinitionItem, Questionnaire, QuestionnaireResponse,
)
from app.models.concept_models import Concept
from app.services.forms_service import (
    _concept_to_question_item, build_fhir_questionnaire,
    validate_fhir_questionnaire, create_or_append_form_version,
)


# ---------------------------------------------------------------------------
# Error classes
# ---------------------------------------------------------------------------

class FormBuilderError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(FormBuilderError):
    def __init__(self, message):
        super().__init__(message, 404)


class ConflictError(FormBuilderError):
    def __init__(self, message):
        super().__init__(message, 409)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _slugify(title):
    """Derive a machine name from a title."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.strip().lower()).strip('-')
    return slug or 'untitled'


def _ensure_unique_name(name, exclude_guid=None):
    """Ensure the name is unique among FormDefinitions."""
    query = FormDefinition.query.filter_by(name=name)
    if exclude_guid:
        query = query.filter(FormDefinition.guid != exclude_guid)
    if query.first():
        # Auto-suffix
        base = name
        counter = 2
        while True:
            candidate = f'{base}-{counter}'
            q = FormDefinition.query.filter_by(name=candidate)
            if exclude_guid:
                q = q.filter(FormDefinition.guid != exclude_guid)
            if not q.first():
                return candidate
            counter += 1
    return name


def _get_definition_or_404(guid):
    fd = FormDefinition.query.filter_by(guid=guid).first()
    if not fd:
        raise NotFoundError(f"FormDefinition '{guid}' not found")
    return fd


# ---------------------------------------------------------------------------
# 1. CRUD — FormDefinition
# ---------------------------------------------------------------------------

def create_form_definition(data):
    """Create a new FormDefinition."""
    title = (data.get('title') or '').strip()
    if not title:
        raise FormBuilderError("Title is required")

    name = (data.get('name') or '').strip()
    if not name:
        name = _slugify(title)
    name = _ensure_unique_name(name)

    fd = FormDefinition(
        guid=str(uuid.uuid4()),
        name=name,
        title=title,
        description=(data.get('description') or '').strip() or None,
        status='draft',
        author=(data.get('author') or '').strip() or None,
    )
    db.session.add(fd)
    db.session.commit()
    return fd.to_dict(include_items=True)


def update_form_definition(guid, data):
    """Update FormDefinition metadata. Increments vers_number."""
    fd = _get_definition_or_404(guid)

    if 'title' in data:
        title = (data['title'] or '').strip()
        if not title:
            raise FormBuilderError("Title cannot be empty")
        fd.title = title

    if 'description' in data:
        fd.description = (data['description'] or '').strip() or None

    if 'name' in data:
        name = (data['name'] or '').strip()
        if name:
            name = _ensure_unique_name(name, exclude_guid=guid)
            fd.name = name

    if 'status' in data:
        new_status = data['status']
        if new_status not in ('draft', 'active', 'retired'):
            raise FormBuilderError(f"Invalid status: '{new_status}'")
        fd.status = new_status

    if 'author' in data:
        fd.author = (data['author'] or '').strip() or None

    fd.vers_number += 1
    db.session.commit()
    return fd.to_dict(include_items=True)


def delete_form_definition(guid):
    """Delete a draft FormDefinition. Rejects if active/retired or has produced forms with responses."""
    fd = _get_definition_or_404(guid)

    if fd.status not in ('draft',):
        raise FormBuilderError(
            f"Cannot delete a {fd.status} definition. Retire it first or change to draft.",
            409,
        )

    if fd.produced_form_guid:
        response_count = QuestionnaireResponse.query.filter_by(
            form_guid=fd.produced_form_guid
        ).count()
        if response_count > 0:
            raise FormBuilderError(
                "Cannot delete — the produced form has responses.", 409
            )

    db.session.delete(fd)
    db.session.commit()
    return {'deleted': guid}


def get_form_definition(guid):
    """Return a FormDefinition with all items and resolved concept info."""
    fd = _get_definition_or_404(guid)
    result = fd.to_dict(include_items=False)

    items_with_concepts = []
    for item in fd.items:
        item_dict = item.to_dict()
        concept = Concept.query.filter_by(guid=item.concept_guid).first()
        if concept:
            item_dict['concept_name'] = concept.concept_name
            item_dict['concept_display_text'] = concept.concept_display_text
            item_dict['response_type'] = (
                concept.response_type_rel.response_type_name
                if concept.response_type_rel else None
            )
            item_dict['canonical_refnumber'] = concept.canonical_refnumber
        items_with_concepts.append(item_dict)

    result['questions'] = items_with_concepts
    return result


def list_form_definitions(status=None, search=None, limit=100, offset=0):
    """Paginated list with optional filters."""
    query = FormDefinition.query

    if status:
        query = query.filter(FormDefinition.status == status)
    if search:
        query = query.filter(FormDefinition.title.ilike(f'%{search}%'))

    total = query.count()
    definitions = query.order_by(FormDefinition.title).offset(offset).limit(limit).all()

    return {
        'definitions': [fd.to_summary() for fd in definitions],
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_more': (offset + limit) < total,
    }


# ---------------------------------------------------------------------------
# 2. Item management
# ---------------------------------------------------------------------------

def add_item(form_definition_guid, data):
    """Add a concept to the form definition."""
    fd = _get_definition_or_404(form_definition_guid)
    concept_guid = (data.get('concept_guid') or '').strip()

    if not concept_guid:
        raise FormBuilderError("concept_guid is required")

    concept = Concept.query.filter_by(guid=concept_guid).first()
    if not concept:
        raise NotFoundError(f"Concept '{concept_guid}' not found")

    existing = FormDefinitionItem.query.filter_by(
        form_definition_guid=form_definition_guid, concept_guid=concept_guid
    ).first()
    if existing:
        raise ConflictError(f"Concept '{concept_guid}' already in this form definition")

    max_order = db.session.query(db.func.coalesce(
        db.func.max(FormDefinitionItem.sort_order), -1
    )).filter_by(form_definition_guid=form_definition_guid).scalar()

    item = FormDefinitionItem(
        guid=str(uuid.uuid4()),
        form_definition_guid=form_definition_guid,
        concept_guid=concept_guid,
        sort_order=max_order + 1,
        display_text_override=(data.get('display_text_override') or '').strip() or None,
        required=data.get('required', False),
        enabled=data.get('enabled', True),
        item_type_override=(data.get('item_type_override') or '').strip() or None,
        group_label=(data.get('group_label') or '').strip() or None,
        notes=(data.get('notes') or '').strip() or None,
    )
    db.session.add(item)
    db.session.commit()

    item_dict = item.to_dict()
    item_dict['concept_name'] = concept.concept_name
    return item_dict


def update_item(item_guid, data):
    """Update item settings."""
    item = FormDefinitionItem.query.filter_by(guid=item_guid).first()
    if not item:
        raise NotFoundError(f"FormDefinitionItem '{item_guid}' not found")

    if 'sort_order' in data:
        item.sort_order = data['sort_order']
    if 'display_text_override' in data:
        item.display_text_override = (data['display_text_override'] or '').strip() or None
    if 'required' in data:
        item.required = bool(data['required'])
    if 'enabled' in data:
        item.enabled = bool(data['enabled'])
    if 'item_type_override' in data:
        item.item_type_override = (data['item_type_override'] or '').strip() or None
    if 'group_label' in data:
        item.group_label = (data['group_label'] or '').strip() or None
    if 'notes' in data:
        item.notes = (data['notes'] or '').strip() or None

    db.session.commit()
    return item.to_dict()


def remove_item(item_guid):
    """Remove an item from the form definition."""
    item = FormDefinitionItem.query.filter_by(guid=item_guid).first()
    if not item:
        raise NotFoundError(f"FormDefinitionItem '{item_guid}' not found")

    db.session.delete(item)
    db.session.commit()
    return {'deleted': item_guid}


def reorder_items(form_definition_guid, ordered_guids):
    """Bulk reorder items by accepting an ordered list of item GUIDs."""
    _get_definition_or_404(form_definition_guid)

    if not ordered_guids or not isinstance(ordered_guids, list):
        raise FormBuilderError("ordered_guids must be a non-empty list")

    items = FormDefinitionItem.query.filter_by(
        form_definition_guid=form_definition_guid
    ).all()
    item_map = {item.guid: item for item in items}

    for i, guid in enumerate(ordered_guids):
        if guid in item_map:
            item_map[guid].sort_order = i

    db.session.commit()
    return {'reordered': len(ordered_guids)}


# ---------------------------------------------------------------------------
# 3. Resolve / Preview
# ---------------------------------------------------------------------------

def _resolve_items(fd):
    """Resolve enabled items into the question set format expected by forms_service."""
    items = FormDefinitionItem.query.filter_by(
        form_definition_guid=fd.guid, enabled=True
    ).order_by(FormDefinitionItem.sort_order).all()

    if not items:
        raise FormBuilderError("No enabled items in this form definition")

    resolved = []
    current_group = None

    for fdi in items:
        concept = Concept.query.filter_by(guid=fdi.concept_guid).first()
        if not concept:
            raise FormBuilderError(
                f"Concept '{fdi.concept_guid}' referenced by item '{fdi.guid}' not found"
            )

        question_item = _concept_to_question_item(concept)

        # Apply per-item overrides
        if fdi.display_text_override:
            question_item['text'] = fdi.display_text_override
        question_item['required'] = fdi.required
        if fdi.item_type_override:
            question_item['type'] = fdi.item_type_override

        # Track group for FHIR group items
        if fdi.group_label:
            question_item['_group_label'] = fdi.group_label

        resolved.append(question_item)

    return resolved


def get_resolved_preview(guid):
    """Resolve items without persisting — for live preview."""
    fd = _get_definition_or_404(guid)
    items = _resolve_items(fd)

    return {
        'form_definition_guid': fd.guid,
        'title': fd.title,
        'description': fd.description,
        'item_count': len(items),
        'items': items,
    }


# ---------------------------------------------------------------------------
# 4. Produce — run full pipeline
# ---------------------------------------------------------------------------

def produce(guid):
    """Produce a FHIR Questionnaire from the FormDefinition."""
    fd = _get_definition_or_404(guid)
    resolved_items = _resolve_items(fd)

    # Group items if group_labels are present
    fhir_ready_items = _apply_grouping(resolved_items)

    form_guid = fd.produced_form_guid or Questionnaire.generate_guid()
    production_key = f'builder:{fd.guid}'

    external_questions = {
        'title': fd.title,
        'description': fd.description or '',
        'items': fhir_ready_items,
    }
    meta = {'title': fd.title, 'description': fd.description or ''}

    fhir_q = build_fhir_questionnaire(
        form_guid=form_guid, version=1, status='draft',
        meta=meta, external_questions=external_questions,
    )
    validate_fhir_questionnaire(fhir_q)

    result = create_or_append_form_version(
        form_guid=form_guid, content_fingerprint=None,
        production_key=production_key, meta=meta, status='draft',
        fhir_questionnaire=fhir_q,
    )

    # Link back
    fd.produced_form_guid = result['form_guid']
    fd.production_key = production_key
    db.session.commit()

    return result


def _apply_grouping(items):
    """Strip internal _group_label markers (grouping is handled in FHIR build)."""
    clean = []
    for item in items:
        item.pop('_group_label', None)
        clean.append(item)
    return clean


# ---------------------------------------------------------------------------
# 5. External access helpers
# ---------------------------------------------------------------------------

def get_produced_questionnaire(guid, version=None):
    """Return the FHIR Questionnaire JSON for a FormDefinition's produced form."""
    fd = _get_definition_or_404(guid)
    if not fd.produced_form_guid:
        raise NotFoundError(
            f"FormDefinition '{guid}' has not been produced yet. "
            "Use the produce endpoint first."
        )

    if version is not None:
        q = Questionnaire.query.filter_by(
            form_guid=fd.produced_form_guid, version=version
        ).first()
    else:
        q = Questionnaire.query.filter_by(
            form_guid=fd.produced_form_guid
        ).order_by(Questionnaire.version.desc()).first()

    if not q:
        raise NotFoundError(f"Questionnaire version not found for form '{fd.produced_form_guid}'")

    return q.to_dict()


def get_render_ready(guid, version=None):
    """Return a simplified, render-ready JSON optimized for frontend rendering."""
    fd = _get_definition_or_404(guid)

    # If produced, use the stored questionnaire items; otherwise resolve live
    if fd.produced_form_guid:
        q_result = get_produced_questionnaire(guid, version)
        fhir_json = q_result.get('fhir_json', {})
        form_version = q_result.get('version', 1)
        status = q_result.get('status', 'draft')
    else:
        # Resolve live from definition
        preview = get_resolved_preview(guid)
        fhir_json = None
        form_version = 0
        status = fd.status

    # Build render-ready from definition items
    items_out = []
    fdi_items = FormDefinitionItem.query.filter_by(
        form_definition_guid=fd.guid, enabled=True
    ).order_by(FormDefinitionItem.sort_order).all()

    for fdi in fdi_items:
        concept = Concept.query.filter_by(guid=fdi.concept_guid).first()
        if not concept:
            continue

        question_item = _concept_to_question_item(concept)
        if fdi.display_text_override:
            question_item['text'] = fdi.display_text_override
        question_item['required'] = fdi.required
        if fdi.item_type_override:
            question_item['type'] = fdi.item_type_override

        render_item = {
            'link_id': question_item.get('link_id'),
            'text': question_item.get('text'),
            'type': question_item.get('type'),
            'required': question_item.get('required', False),
        }

        if question_item.get('unit'):
            render_item['unit'] = question_item['unit']
        if question_item.get('min_value') is not None:
            render_item['min_value'] = question_item['min_value']
        if question_item.get('max_value') is not None:
            render_item['max_value'] = question_item['max_value']
        if question_item.get('options'):
            render_item['options'] = question_item['options']
        if fdi.group_label:
            render_item['group'] = fdi.group_label

        items_out.append(render_item)

    return {
        'form_guid': fd.produced_form_guid or fd.guid,
        'form_definition_guid': fd.guid,
        'title': fd.title,
        'description': fd.description,
        'version': form_version,
        'status': status,
        'items': items_out,
    }
