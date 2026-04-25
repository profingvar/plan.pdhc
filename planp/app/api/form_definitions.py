"""Form definitions API — CRUD for FormDefinitions, item management, produce, preview."""
from flask import Blueprint, jsonify, request
from app.api.auth import requires_role
from app import limiter
from app.services.form_definitions_service import (
    create_form_definition, update_form_definition, delete_form_definition,
    get_form_definition, list_form_definitions,
    add_item, update_item, remove_item, reorder_items,
    produce, get_resolved_preview,
    get_produced_questionnaire, get_render_ready,
    FormBuilderError, NotFoundError, ConflictError,
)
from app.api.forms import require_api_key_or_role

form_defs_bp = Blueprint('form_defs_api', __name__)
limiter.limit("200/minute")(form_defs_bp)


def _handle_error(e):
    return jsonify(error=type(e).__name__, message=e.message, code=e.status_code), e.status_code


# ---------------------------------------------------------------------------
# FormDefinition CRUD
# ---------------------------------------------------------------------------

@form_defs_bp.route('/form-definitions')
@requires_role('read_only')
def list_definitions():
    status = request.args.get('status')
    search = request.args.get('search')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    return jsonify(list_form_definitions(status=status, search=search, limit=limit, offset=offset))


@form_defs_bp.route('/form-definitions', methods=['POST'])
@requires_role('read_write')
def create_definition():
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400
    try:
        return jsonify(create_form_definition(data)), 201
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>')
@requires_role('read_only')
def get_definition(guid):
    try:
        return jsonify(get_form_definition(guid))
    except NotFoundError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>', methods=['PUT'])
@requires_role('read_write')
def update_definition(guid):
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400
    try:
        return jsonify(update_form_definition(guid, data))
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>', methods=['DELETE'])
@requires_role('read_write')
def delete_definition(guid):
    try:
        return jsonify(delete_form_definition(guid))
    except FormBuilderError as e:
        return _handle_error(e)


# ---------------------------------------------------------------------------
# Item management
# ---------------------------------------------------------------------------

@form_defs_bp.route('/form-definitions/<guid>/items')
@requires_role('read_only')
def list_items(guid):
    try:
        result = get_form_definition(guid)
        return jsonify({'items': result.get('questions', [])})
    except NotFoundError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/items', methods=['POST'])
@requires_role('read_write')
def add_item_endpoint(guid):
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400
    try:
        return jsonify(add_item(guid, data)), 201
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/items/<item_guid>', methods=['PUT'])
@requires_role('read_write')
def update_item_endpoint(guid, item_guid):
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400
    try:
        return jsonify(update_item(item_guid, data))
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/items/<item_guid>', methods=['DELETE'])
@requires_role('read_write')
def remove_item_endpoint(guid, item_guid):
    try:
        return jsonify(remove_item(item_guid))
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/reorder', methods=['POST'])
@requires_role('read_write')
def reorder_endpoint(guid):
    data = request.get_json()
    if not data:
        return jsonify(error="Bad Request", message="JSON body required", code=400), 400
    ordered_guids = data.get('ordered_guids', [])
    try:
        return jsonify(reorder_items(guid, ordered_guids))
    except FormBuilderError as e:
        return _handle_error(e)


# ---------------------------------------------------------------------------
# Produce & Preview
# ---------------------------------------------------------------------------

@form_defs_bp.route('/form-definitions/<guid>/produce', methods=['POST'])
@requires_role('read_write')
def produce_endpoint(guid):
    try:
        result = produce(guid)
        return jsonify(result), 201
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/preview')
@requires_role('read_only')
def preview_endpoint(guid):
    try:
        return jsonify(get_resolved_preview(guid))
    except FormBuilderError as e:
        return _handle_error(e)


# ---------------------------------------------------------------------------
# External access (API key or SSO)
# ---------------------------------------------------------------------------

@form_defs_bp.route('/form-definitions/<guid>/questionnaire')
@require_api_key_or_role
def questionnaire_endpoint(guid):
    version = request.args.get('version', type=int)
    try:
        return jsonify(get_produced_questionnaire(guid, version=version))
    except FormBuilderError as e:
        return _handle_error(e)


@form_defs_bp.route('/form-definitions/<guid>/render-ready')
@require_api_key_or_role
def render_ready_endpoint(guid):
    version = request.args.get('version', type=int)
    try:
        return jsonify(get_render_ready(guid, version=version))
    except FormBuilderError as e:
        return _handle_error(e)
