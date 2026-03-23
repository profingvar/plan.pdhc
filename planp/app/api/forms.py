"""Forms API — FHIR Questionnaire production, read, and management endpoints."""
import functools
from flask import Blueprint, jsonify, request, current_app
from app.api.auth import requires_role
from app.services.forms_service import (
    resolve_question_set, build_fhir_questionnaire, validate_fhir_questionnaire,
    create_or_append_form_version, publish_form_version, enforce_latest_version_immutability,
    get_form_catalogue, get_form_definition, get_form_version_history,
    QuestionServiceError, BuildError, ValidationError, PublishError,
    ImmutabilityError, DefinitionError, HistoryError,
)
from app.models.forms_models import Questionnaire
from app import limiter

forms_bp = Blueprint('forms_api', __name__)
limiter.limit("200/minute")(forms_bp)


def require_api_key_or_role(fn):
    """Accept either a valid X-API-Key header or an SSO session with read_only role."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Check API key first
        api_key = request.headers.get('X-API-Key', '')
        configured_key = current_app.config.get('API_KEY')
        if configured_key and api_key == configured_key:
            return fn(*args, **kwargs)

        # Fall through to SSO role check
        return requires_role('read_only')(fn)(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Builder read endpoints (API key or SSO)
# ---------------------------------------------------------------------------

@forms_bp.route('/forms')
@require_api_key_or_role
def list_forms():
    """GET /api/v1/forms — GetFormCatalogue"""
    status = request.args.get('status', 'active')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    return jsonify(get_form_catalogue(status=status, limit=limit, offset=offset))


@forms_bp.route('/forms/<form_guid>')
@require_api_key_or_role
def get_form(form_guid):
    """GET /api/v1/forms/<form_guid> — GetFormDefinition"""
    version = request.args.get('version', type=int)
    try:
        return jsonify(get_form_definition(form_guid, version=version))
    except DefinitionError as e:
        return jsonify(error="Not Found", message=e.message, code=e.status_code), e.status_code


@forms_bp.route('/forms/<form_guid>/versions')
@require_api_key_or_role
def get_versions(form_guid):
    """GET /api/v1/forms/<form_guid>/versions — GetFormVersionHistory"""
    try:
        return jsonify(get_form_version_history(form_guid))
    except HistoryError as e:
        return jsonify(error="Not Found", message=e.message, code=e.status_code), e.status_code


# ---------------------------------------------------------------------------
# Production endpoints (SSO with read_write role)
# ---------------------------------------------------------------------------

@forms_bp.route('/forms/produce', methods=['POST'])
@requires_role('read_write')
def produce_form():
    """POST /api/v1/forms/produce — full pipeline: resolve → build → validate → persist."""
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400

    form_guid = data.get('form_guid')
    title = data.get('title')
    description = data.get('description', '')
    status = data.get('status', 'draft')
    production_key = data.get('production_key')
    content_fingerprint = data.get('content_fingerprint')

    concept_guids = data.get('concept_guids')
    plandefinition_guid = data.get('plandefinition_guid')
    external_questions = data.get('external_questions')

    if not external_questions and not concept_guids and not plandefinition_guid:
        return jsonify(
            error="Bad Request",
            message="Provide 'concept_guids', 'plandefinition_guid', or 'external_questions'",
            code=400
        ), 400

    try:
        if external_questions:
            pass
        elif plandefinition_guid:
            external_questions = resolve_question_set(
                plandefinition_guid, source_type='plandefinition'
            )
            if not title:
                title = external_questions.get('title', '')
            if not description:
                description = external_questions.get('description', '')
            if not production_key:
                production_key = f'plandef:{plandefinition_guid}'
        elif concept_guids:
            external_questions = resolve_question_set(
                concept_guids, source_type='concept_guids'
            )

        if title:
            external_questions['title'] = title
        if description:
            external_questions['description'] = description

        meta = {
            'title': external_questions.get('title', title or ''),
            'description': external_questions.get('description', description or ''),
        }

        if not form_guid:
            form_guid = Questionnaire.generate_guid()

        fhir_q = build_fhir_questionnaire(
            form_guid=form_guid, version=1, status=status,
            meta=meta, external_questions=external_questions,
        )

        validate_fhir_questionnaire(fhir_q)

        result = create_or_append_form_version(
            form_guid=form_guid, content_fingerprint=content_fingerprint,
            production_key=production_key, meta=meta, status=status,
            fhir_questionnaire=fhir_q,
        )

        return jsonify(result), 201

    except QuestionServiceError as e:
        return jsonify(error="Question Service Error", message=e.message, code=e.status_code), e.status_code
    except BuildError as e:
        return jsonify(error="Build Error", message=e.message, code=e.status_code), e.status_code
    except ValidationError as e:
        return jsonify(error="Validation Error", message=e.message, code=e.status_code), e.status_code


@forms_bp.route('/forms/<form_guid>/publish', methods=['POST'])
@requires_role('read_write')
def publish(form_guid):
    """POST /api/v1/forms/<form_guid>/publish — PublishFormVersion"""
    data = request.get_json() or {}
    version = data.get('version')
    try:
        return jsonify(publish_form_version(form_guid, version=version))
    except PublishError as e:
        return jsonify(error="Not Found", message=e.message, code=e.status_code), e.status_code


@forms_bp.route('/forms/<form_guid>/immutability')
@requires_role('read_write')
def immutability(form_guid):
    """GET /api/v1/forms/<form_guid>/immutability"""
    try:
        return jsonify(enforce_latest_version_immutability(form_guid))
    except ImmutabilityError as e:
        return jsonify(error="Not Found", message=e.message, code=e.status_code), e.status_code
