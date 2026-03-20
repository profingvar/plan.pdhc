import uuid as uuid_mod
import bleach
from flask import Blueprint, request, jsonify
from app import db, limiter
from app.api.auth import requires_role
from app.models.concept_models import (
    CanonicalLib, ConceptType, ResponseType, Unit, PlanDefType, IntendedUse,
    ValueCatalog, ValueSet, ValueSetValue,
)
from app.services.name_uniqueness import make_unique_value_name, make_unique_valueset_name

lookup_bp = Blueprint('lookup', __name__)
limiter.limit("200/minute")(lookup_bp)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def _crud_routes(bp, url, model_class, name_field, display_field=None):
    """Register generic CRUD endpoints for a lookup table."""

    @bp.route(url, methods=['GET'], endpoint=f'{url}_list')
    def list_items():
        items = model_class.query.order_by(getattr(model_class, name_field)).all()
        return jsonify([i.to_dict() for i in items]), 200

    @bp.route(url, methods=['POST'], endpoint=f'{url}_create')
    @requires_role('read_write')
    def create_item():
        data = request.get_json(silent=True) or {}
        name_val = _sanitize(data.get(name_field))
        if not name_val:
            return jsonify({'error': f'{name_field} is required'}), 400

        existing = model_class.query.filter(
            getattr(model_class, name_field) == name_val
        ).first()
        if existing:
            return jsonify({'error': f'{name_field} already exists'}), 409

        item = model_class(**{name_field: name_val})
        if display_field and data.get(display_field):
            setattr(item, display_field, _sanitize(data[display_field]))
        for f in ('author',):
            if data.get(f):
                setattr(item, f, _sanitize(data[f]))
        # CanonicalLib extra field
        if hasattr(model_class, 'canonical_lib_url') and data.get('canonical_lib_url'):
            item.canonical_lib_url = _sanitize(data['canonical_lib_url'])

        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    @bp.route(f'{url}/<guid>', methods=['GET'], endpoint=f'{url}_read')
    def read_item(guid):
        if not _is_valid_uuid(guid):
            return jsonify({'error': 'Invalid GUID'}), 400
        item = model_class.query.filter_by(guid=guid).first()
        if not item:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(item.to_dict()), 200

    @bp.route(f'{url}/<guid>', methods=['PUT'], endpoint=f'{url}_update')
    @requires_role('read_write')
    def update_item(guid):
        if not _is_valid_uuid(guid):
            return jsonify({'error': 'Invalid GUID'}), 400
        item = model_class.query.filter_by(guid=guid).first()
        if not item:
            return jsonify({'error': 'Not found'}), 404
        data = request.get_json(silent=True) or {}
        if name_field in data:
            setattr(item, name_field, _sanitize(data[name_field]))
        if display_field and display_field in data:
            setattr(item, display_field, _sanitize(data[display_field]))
        if 'author' in data:
            item.author = _sanitize(data['author'])
        if hasattr(item, 'canonical_lib_url') and 'canonical_lib_url' in data:
            item.canonical_lib_url = _sanitize(data['canonical_lib_url'])
        item.vers_number = (item.vers_number or 1) + 1
        db.session.commit()
        return jsonify(item.to_dict()), 200

    @bp.route(f'{url}/<guid>', methods=['DELETE'], endpoint=f'{url}_delete')
    @requires_role('read_write')
    def delete_item(guid):
        if not _is_valid_uuid(guid):
            return jsonify({'error': 'Invalid GUID'}), 400
        item = model_class.query.filter_by(guid=guid).first()
        if not item:
            return jsonify({'error': 'Not found'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Deleted'}), 200


# Register lookup table CRUD
_crud_routes(lookup_bp, '/canonical-libs', CanonicalLib, 'canonical_lib_name', 'canonical_lib_display_text')
_crud_routes(lookup_bp, '/concept-types', ConceptType, 'concept_type_name', 'concept_type_display_text')
_crud_routes(lookup_bp, '/response-types', ResponseType, 'response_type_name', 'response_type_display_text')
_crud_routes(lookup_bp, '/units', Unit, 'unit_name', 'unit_display_text')
_crud_routes(lookup_bp, '/plandef-types', PlanDefType, 'plandef_type_name', 'plandef_type_display_text')
_crud_routes(lookup_bp, '/intended-uses', IntendedUse, 'intended_use_name', 'intended_use_display_text')


# ---------------------------------------------------------------------------
# Values CRUD
# ---------------------------------------------------------------------------

@lookup_bp.route('/values', methods=['GET'])
def list_values():
    items = ValueCatalog.query.order_by(ValueCatalog.value_name).all()
    return jsonify([i.to_dict() for i in items]), 200


@lookup_bp.route('/values', methods=['POST'])
@requires_role('read_write')
def create_value():
    data = request.get_json(silent=True) or {}
    name = _sanitize(data.get('value_name'))
    canon_lib = data.get('canonical_lib')
    if not name or not canon_lib:
        return jsonify({'error': 'value_name and canonical_lib are required'}), 400
    if not _is_valid_uuid(canon_lib):
        return jsonify({'error': 'Invalid canonical_lib UUID'}), 400
    if not CanonicalLib.query.filter_by(guid=canon_lib).first():
        return jsonify({'error': 'Canonical library not found'}), 404

    name = make_unique_value_name(name)
    item = ValueCatalog(
        value_name=name,
        canonical_lib=canon_lib,
        canonical_refnumber=_sanitize(data.get('canonical_refnumber')),
        value_display_text=_sanitize(data.get('value_display_text')),
        value_explanation=_sanitize(data.get('value_explanation')),
        author=_sanitize(data.get('author')),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@lookup_bp.route('/values/<guid>', methods=['GET'])
def read_value(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueCatalog.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item.to_dict()), 200


@lookup_bp.route('/values/<guid>', methods=['PUT'])
@requires_role('read_write')
def update_value(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueCatalog.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(silent=True) or {}
    for f in ('value_name', 'value_display_text', 'value_explanation', 'canonical_refnumber', 'author'):
        if f in data:
            setattr(item, f, _sanitize(data[f]))
    if 'canonical_lib' in data:
        if not _is_valid_uuid(data['canonical_lib']):
            return jsonify({'error': 'Invalid canonical_lib UUID'}), 400
        item.canonical_lib = data['canonical_lib']
    item.vers_number = (item.vers_number or 1) + 1
    db.session.commit()
    return jsonify(item.to_dict()), 200


@lookup_bp.route('/values/<guid>', methods=['DELETE'])
@requires_role('read_write')
def delete_value(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueCatalog.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


# ---------------------------------------------------------------------------
# ValueSets CRUD
# ---------------------------------------------------------------------------

@lookup_bp.route('/valuesets', methods=['GET'])
def list_valuesets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    page = max(1, page)
    per_page = max(1, min(200, per_page))
    pagination = ValueSet.query.order_by(ValueSet.valueset_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        'items': [i.to_dict() for i in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
    }), 200


@lookup_bp.route('/valuesets', methods=['POST'])
@requires_role('read_write')
def create_valueset():
    data = request.get_json(silent=True) or {}
    name = _sanitize(data.get('valueset_name'))
    canon_lib = data.get('canonical_lib')
    if not name or not canon_lib:
        return jsonify({'error': 'valueset_name and canonical_lib are required'}), 400
    if not _is_valid_uuid(canon_lib):
        return jsonify({'error': 'Invalid canonical_lib UUID'}), 400
    if not CanonicalLib.query.filter_by(guid=canon_lib).first():
        return jsonify({'error': 'Canonical library not found'}), 404

    name = make_unique_valueset_name(name)
    item = ValueSet(
        valueset_name=name,
        canonical_lib=canon_lib,
        canonical_refnumber=_sanitize(data.get('canonical_refnumber')),
        valueset_display_text=_sanitize(data.get('valueset_display_text')),
        valueset_explanation=_sanitize(data.get('valueset_explanation')),
        author=_sanitize(data.get('author')),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@lookup_bp.route('/valuesets/<guid>', methods=['GET'])
def read_valueset(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueSet.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(item.to_dict()), 200


@lookup_bp.route('/valuesets/<guid>', methods=['PUT'])
@requires_role('read_write')
def update_valueset(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueSet.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(silent=True) or {}
    for f in ('valueset_name', 'valueset_display_text', 'valueset_explanation', 'canonical_refnumber', 'author'):
        if f in data:
            setattr(item, f, _sanitize(data[f]))
    if 'canonical_lib' in data:
        if not _is_valid_uuid(data['canonical_lib']):
            return jsonify({'error': 'Invalid canonical_lib UUID'}), 400
        item.canonical_lib = data['canonical_lib']
    item.vers_number = (item.vers_number or 1) + 1
    db.session.commit()
    return jsonify(item.to_dict()), 200


@lookup_bp.route('/valuesets/<guid>', methods=['DELETE'])
@requires_role('read_write')
def delete_valueset(guid):
    if not _is_valid_uuid(guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    item = ValueSet.query.filter_by(guid=guid).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


# ---------------------------------------------------------------------------
# ValueSet membership
# ---------------------------------------------------------------------------

@lookup_bp.route('/valuesets/<valueset_guid>/values', methods=['GET'])
def list_valueset_values(valueset_guid):
    if not _is_valid_uuid(valueset_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    vs = ValueSet.query.filter_by(guid=valueset_guid).first()
    if not vs:
        return jsonify({'error': 'ValueSet not found'}), 404
    links = ValueSetValue.query.filter_by(valueset_guid=valueset_guid).order_by(
        ValueSetValue.sort_order
    ).all()
    result = []
    for link in links:
        val = ValueCatalog.query.filter_by(guid=link.value_guid).first()
        if val:
            d = val.to_dict()
            d['sort_order'] = link.sort_order
            result.append(d)
    return jsonify(result), 200


@lookup_bp.route('/valuesets/<valueset_guid>/values', methods=['POST'])
@requires_role('read_write')
def add_valueset_value(valueset_guid):
    if not _is_valid_uuid(valueset_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    vs = ValueSet.query.filter_by(guid=valueset_guid).first()
    if not vs:
        return jsonify({'error': 'ValueSet not found'}), 404
    data = request.get_json(silent=True) or {}
    value_guid = data.get('value_guid')
    if not value_guid or not _is_valid_uuid(value_guid):
        return jsonify({'error': 'Valid value_guid is required'}), 400
    if not ValueCatalog.query.filter_by(guid=value_guid).first():
        return jsonify({'error': 'Value not found'}), 404

    existing = ValueSetValue.query.filter_by(
        valueset_guid=valueset_guid, value_guid=value_guid
    ).first()
    if existing:
        return jsonify({'error': 'Value already in this ValueSet'}), 409

    link = ValueSetValue(
        valueset_guid=valueset_guid,
        value_guid=value_guid,
        sort_order=data.get('sort_order'),
    )
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201


@lookup_bp.route('/valuesets/<valueset_guid>/values/<value_guid>', methods=['PUT'])
@requires_role('read_write')
def update_valueset_value(valueset_guid, value_guid):
    if not _is_valid_uuid(valueset_guid) or not _is_valid_uuid(value_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    link = ValueSetValue.query.filter_by(
        valueset_guid=valueset_guid, value_guid=value_guid
    ).first()
    if not link:
        return jsonify({'error': 'Membership not found'}), 404
    data = request.get_json(silent=True) or {}
    if 'sort_order' in data:
        link.sort_order = data['sort_order']
    db.session.commit()
    return jsonify(link.to_dict()), 200


@lookup_bp.route('/valuesets/<valueset_guid>/values/<value_guid>', methods=['DELETE'])
@requires_role('read_write')
def remove_valueset_value(valueset_guid, value_guid):
    if not _is_valid_uuid(valueset_guid) or not _is_valid_uuid(value_guid):
        return jsonify({'error': 'Invalid GUID'}), 400
    link = ValueSetValue.query.filter_by(
        valueset_guid=valueset_guid, value_guid=value_guid
    ).first()
    if not link:
        return jsonify({'error': 'Membership not found'}), 404
    db.session.delete(link)
    db.session.commit()
    return jsonify({'message': 'Removed'}), 200
