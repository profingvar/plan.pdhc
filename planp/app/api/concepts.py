import io
import os
import uuid as uuid_mod
from datetime import datetime, timezone
import bleach
from flask import Blueprint, request, jsonify, g
from sqlalchemy import or_
from app import db  # limiter exemption handled globally via request_filter in app/__init__.py
from app.api.auth import requires_role
from app.models.concept_models import (
    Concept, CanonicalLib, ValueSet, ValueSetValue, ValueCatalog,
)
from app.services.name_uniqueness import make_unique_concept_name
from app.services.concept_importer import (
    parse_xlsx, parse_csv, validate_and_import, compute_sha256, ImportError_,
)

concepts_bp = Blueprint('concepts', __name__)
# Rate limiting via global RATELIMIT_DEFAULT in app/__init__.py.
# Service-key callers (sim.pdhc / loader.pdhc / cdr.pdhc canonicaliser)
# are exempted via the global request_filter registered there — the
# burst-warmup of the canonicaliser cache used to push parallel writers
# past the limit and trigger 6/400 4xx during the first seed
# (post_seed_followups Block A).


def _is_valid_uuid(val):
    try:
        uuid_mod.UUID(str(val))
        return True
    except (ValueError, AttributeError):
        return False


def _sanitize(val):
    if val is None:
        return None
    return bleach.clean(str(val).strip())


# ---------------------------------------------------------------------------
# Concept CRUD
# ---------------------------------------------------------------------------

@concepts_bp.route('/concepts', methods=['GET'])
def list_concepts():
    query = Concept.query

    # Text search
    search = request.args.get('search', '').strip()
    if search:
        like = f'%{search}%'
        query = query.filter(or_(
            Concept.concept_name.ilike(like),
            Concept.concept_display_text.ilike(like),
            Concept.concept_explain.ilike(like),
        ))

    # Filters
    for filt, field in [
        ('concept_type', Concept.concept_type),
        ('response_type', Concept.response_type),
        ('canonical_lib', Concept.canonical_lib),
    ]:
        val = request.args.get(filt)
        if val:
            query = query.filter(field == val)

    if request.args.get('has_values') == 'true':
        query = query.filter(Concept.no_of_values_connected > 0)

    # Deterministic sort
    query = query.order_by(Concept.concept_name, Concept.guid)

    # Pagination
    page = max(1, request.args.get('page', 1, type=int))
    per_page = max(1, min(200, request.args.get('per_page', 50, type=int)))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [c.to_dict() for c in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
    }), 200


@concepts_bp.route('/concepts', methods=['POST'])
@requires_role('read_write')
def create_concept():
    data = request.get_json(silent=True) or {}
    name = _sanitize(data.get('concept_name'))
    canon_lib = data.get('canonical_lib')
    if not name or not canon_lib:
        return jsonify({'error': 'concept_name and canonical_lib are required'}), 400
    if not _is_valid_uuid(canon_lib):
        return jsonify({'error': 'Invalid canonical_lib UUID'}), 400
    if not CanonicalLib.query.filter_by(guid=canon_lib).first():
        return jsonify({'error': 'Canonical library not found'}), 404

    # Validate optional UUID refs
    for fk_field in ('concept_type', 'response_type', 'unit', 'valueset'):
        val = data.get(fk_field)
        if val and not _is_valid_uuid(val):
            return jsonify({'error': f'Invalid UUID for {fk_field}'}), 400

    name = make_unique_concept_name(name)

    concept = Concept(
        concept_name=name,
        canonical_lib=canon_lib,
        canonical_refnumber=_sanitize(data.get('canonical_refnumber')),
        concept_display_text=_sanitize(data.get('concept_display_text')),
        concept_explain=_sanitize(data.get('concept_explain')),
        status=data.get('status', 'draft'),
        concept_type=data.get('concept_type'),
        response_type=data.get('response_type'),
        unit=data.get('unit'),
        range_low=data.get('range_low'),
        range_high=data.get('range_high'),
        anchor_low_text=_sanitize(data.get('anchor_low_text')),
        anchor_high_text=_sanitize(data.get('anchor_high_text')),
        valueset=data.get('valueset'),
        author=_sanitize(data.get('author')),
    )
    db.session.add(concept)
    db.session.commit()
    return jsonify(concept.to_dict()), 201


@concepts_bp.route('/concepts/<guid>', methods=['GET'])
def read_concept(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=guid).first()
    if not concept:
        return jsonify({'error': 'Not found'}), 404

    result = concept.to_dict()

    # Include valueset values if bound
    if concept.valueset:
        links = ValueSetValue.query.filter_by(
            valueset_guid=concept.valueset
        ).order_by(ValueSetValue.sort_order).all()
        values = []
        for link in links:
            val = ValueCatalog.query.filter_by(guid=link.value_guid).first()
            if val:
                d = val.to_dict()
                d['sort_order'] = link.sort_order
                values.append(d)
        result['valueset_values'] = values

    return jsonify(result), 200


@concepts_bp.route('/concepts/<guid>', methods=['PUT'])
@requires_role('read_write')
def update_concept(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=guid).first()
    if not concept:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json(silent=True) or {}

    # Validate UUID refs
    for fk_field in ('canonical_lib', 'concept_type', 'response_type', 'unit', 'valueset'):
        val = data.get(fk_field)
        if val and not _is_valid_uuid(val):
            return jsonify({'error': f'Invalid UUID for {fk_field}'}), 400

    string_fields = ('concept_name', 'concept_display_text', 'concept_explain',
                     'canonical_refnumber', 'anchor_low_text', 'anchor_high_text', 'author')
    for f in string_fields:
        if f in data:
            setattr(concept, f, _sanitize(data[f]))

    direct_fields = ('canonical_lib', 'concept_type', 'response_type', 'unit',
                     'valueset', 'status', 'range_low', 'range_high')
    for f in direct_fields:
        if f in data:
            setattr(concept, f, data[f])

    concept.vers_number = (concept.vers_number or 1) + 1
    concept.date_valid = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(concept.to_dict()), 200


@concepts_bp.route('/concepts/import', methods=['POST'])
@requires_role('admin')
def import_concepts():
    """Bulk-import concepts from an uploaded .xlsx or .csv.

    Ticket #134. Idempotent on concept_name (upsert). FK fields
    (canonical_lib, concept_type, response_type, unit) resolve by
    human name or GUID. canonical_lib + canonical_refnumber are
    identity fields: changing them on an existing row is a conflict
    rather than a silent overwrite.

    Form fields:
      file:    The .xlsx/.csv (multipart upload)
      dry_run: 'true' to validate-only without committing

    Returns JSON report: {accepted, rejected, summary, operator,
    filename, sha256}.
    """
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'file field required'}), 400

    raw = f.read()
    if not raw:
        return jsonify({'error': 'uploaded file is empty'}), 400
    sha = compute_sha256(raw)
    filename = f.filename or 'unnamed'

    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == '.xlsx':
            rows = parse_xlsx(io.BytesIO(raw))
        elif ext == '.csv':
            rows = parse_csv(io.BytesIO(raw))
        else:
            return jsonify({
                'error': f'unsupported file extension {ext!r}; use .xlsx or .csv'
            }), 400
    except ImportError_ as e:
        return jsonify({'error': str(e), 'filename': filename, 'sha256': sha}), 400

    dry_run = (request.form.get('dry_run', '').strip().lower() == 'true')
    operator = _operator_identity()

    report = validate_and_import(
        rows, operator=operator, filename=filename, sha256=sha, dry_run=dry_run,
    )
    status = 200 if not report['rejected'] else 207  # 207 Multi-Status when partial
    return jsonify(report), status


def _operator_identity():
    """Best-effort identity of the current operator for audit logging."""
    blob = getattr(g, 'sso_user', None)
    if blob:
        return blob.get('email') or blob.get('user_guid') or 'sso:unknown'
    return f'service:{request.headers.get("X-Source-Service", "unknown")}'


@concepts_bp.route('/concepts/<guid>', methods=['DELETE'])
@requires_role('read_write')
def delete_concept(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=guid).first()
    if not concept:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(concept)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


# ---------------------------------------------------------------------------
# Concept ↔ Values (through ValueSet)
# ---------------------------------------------------------------------------

@concepts_bp.route('/concepts/<concept_guid>/values', methods=['GET'])
def list_concept_values(concept_guid):
    if not _is_valid_uuid(concept_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=concept_guid).first()
    if not concept:
        return jsonify({'error': 'Concept not found'}), 404
    if not concept.valueset:
        return jsonify([]), 200

    links = ValueSetValue.query.filter_by(
        valueset_guid=concept.valueset
    ).order_by(ValueSetValue.sort_order).all()
    result = []
    for link in links:
        val = ValueCatalog.query.filter_by(guid=link.value_guid).first()
        if val:
            d = val.to_dict()
            d['sort_order'] = link.sort_order
            result.append(d)
    return jsonify(result), 200


@concepts_bp.route('/concepts/<concept_guid>/values', methods=['POST'])
@requires_role('read_write')
def add_concept_value(concept_guid):
    if not _is_valid_uuid(concept_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=concept_guid).first()
    if not concept:
        return jsonify({'error': 'Concept not found'}), 404
    if not concept.valueset:
        return jsonify({'error': 'Concept does not have a valueset'}), 400

    data = request.get_json(silent=True) or {}
    value_guid = data.get('value_guid')
    if not value_guid or not _is_valid_uuid(value_guid):
        return jsonify({'error': 'Valid value_guid is required'}), 400
    if not ValueCatalog.query.filter_by(guid=value_guid).first():
        return jsonify({'error': 'Value not found'}), 404

    existing = ValueSetValue.query.filter_by(
        valueset_guid=concept.valueset, value_guid=value_guid
    ).first()
    if existing:
        return jsonify({'error': 'Value already in this ValueSet'}), 409

    link = ValueSetValue(
        valueset_guid=concept.valueset,
        value_guid=value_guid,
        sort_order=data.get('sort_order'),
    )
    db.session.add(link)

    concept.no_of_values_connected = ValueSetValue.query.filter_by(
        valueset_guid=concept.valueset
    ).count() + 1
    db.session.commit()
    return jsonify(link.to_dict()), 201


@concepts_bp.route('/concepts/<concept_guid>/values/<value_guid>', methods=['DELETE'])
@requires_role('read_write')
def remove_concept_value(concept_guid, value_guid):
    if not _is_valid_uuid(concept_guid) or not _is_valid_uuid(value_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    concept = Concept.query.filter_by(guid=concept_guid).first()
    if not concept:
        return jsonify({'error': 'Concept not found'}), 404
    if not concept.valueset:
        return jsonify({'error': 'Concept does not have a valueset'}), 400

    link = ValueSetValue.query.filter_by(
        valueset_guid=concept.valueset, value_guid=value_guid
    ).first()
    if not link:
        return jsonify({'error': 'Membership not found'}), 404
    db.session.delete(link)

    concept.no_of_values_connected = max(
        0, ValueSetValue.query.filter_by(valueset_guid=concept.valueset).count() - 1
    )
    db.session.commit()
    return jsonify({'message': 'Removed'}), 200
