import uuid as uuid_mod
import bleach
from flask import Blueprint, request, jsonify
from app import db  # limiter exemption handled globally via request_filter in app/__init__.py
from app.api.auth import requires_role
from app.models.concept_models import (
    CanonicalLib, ConceptType, ResponseType, Unit, PlanDefType, IntendedUse,
    ValueCatalog, ValueSet, ValueSetValue,
)
from app.services.name_uniqueness import (NameUniquenessService,
                                          make_unique_value_name,
                                          make_unique_valueset_name)

lookup_bp = Blueprint('lookup', __name__)
# Rate limiting via global RATELIMIT_DEFAULT in app/__init__.py.
# Service-key callers (canonicaliser warmup) bypass via the global
# request_filter registered there.


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


def _crud_routes(bp, url, model_class, name_field, display_field=None, *,
                 public_read):
    """Register generic CRUD endpoints for a lookup table.

    ``public_read`` is REQUIRED and keyword-only (#925). Before, this function
    decorated CREATE/UPDATE/DELETE with ``@requires_role('read_write')`` and
    decorated LIST and READ with NOTHING, so six lookup tables served full
    records to anyone who asked while CLAUDE.md §3 recorded this service as
    `Auth: SSO`.

    THAT WAS AN OMISSION, NOT A POSTURE, and the proof is in this same module:
    ``/values`` is the one lookup route written by hand rather than through
    this factory, and its GET carries ``@requires_role('read_only')``. The
    author who wrote a read route reached for the gate; the factory forgot it.
    ``/api/v1/ValueSet`` is gated too, while ``CodeSystem`` and ``ConceptMap``
    are not — three postures across one set of blueprints.

    Making the parameter required means a new lookup table CANNOT be
    registered without someone deciding, and the decision is visible at the
    registration line instead of being the absence of a decorator forty lines
    away. That is the actual fix; gating two tables is the smaller half.

    WHY SOME READS STAY OPEN, measured 2026-11-04 rather than assumed. The
    deeper problem is that **plan.pdhc has no working machine-auth door**:
    `KNOWN_SERVICES` holds only `sim.pdhc` and `SIM_PDHC_SERVICE_KEY` is unset
    in production, so that dict admits nobody — and `outbound_session_headers()`,
    which several clients do send, carries `X-Operator-Session-Id` only. It is
    session propagation (#408), not authentication. So every internal consumer
    reads plan unauthenticated BY NECESSITY, and the open reads are load-bearing
    scaffolding for that absence rather than a convenience. Closing them is
    sequenced behind giving those callers a credential, which needs an
    operator-set key (§15) and is tracked as #931.
    """
    _read_gate = (lambda f: f) if public_read else requires_role('read_only')

    def _project(item):
        """The response body. On a PUBLIC read it drops `author` (#925).

        Measured in production 2026-11-04, the publicly readable tables served:
            canonical-libs   loader.pdhc x3, 'migration c3d4e5f6a7b8' x1
            concept-types    loader.pdhc x1   (now gated)
            response-types   one internal ticket slug x1
            units            one internal ticket slug x1, 'system' x65

        `loader.pdhc` was RETIRED by #736 — no repo, and its live never-rotated
        key was destroyed. Serving its name, plus a migration revision id and
        two internal ticket slugs, is internal history handed to anyone who
        asks. Not a credential leak; it is the kind of detail used to date a
        system and enumerate its services.

        THE DATA IS NOT REWRITTEN, deliberately. `author` records WHO created
        the row, and rewriting it would falsify that — the same argument
        CLAUDE.md §2 makes for leaving a code comment that cites a superseded
        ticket number alone. So the projection changes and the record stays
        true.

        The projection does NOT vary by caller. A route that may be read
        anonymously should not return different fields to different callers:
        that is a security-relevant difference which is harder to reason about
        than a single shape. plan's own admin UI is unaffected either way — it
        is server-rendered straight off the model (`{{ i.author }}`), not off
        this API.

        Verified before changing: no consumer reads `author` off a lookup
        response. The four files that call these paths mention it only as the
        word "authority" in prose or as `author_org_guid`, a different field;
        alert.pdhc WRITES `author` in a POST body and never reads it back.
        """
        d = item.to_dict()
        if public_read:
            d.pop('author', None)
        return d

    @bp.route(url, methods=['GET'], endpoint=f'{url}_list')
    @_read_gate
    def list_items():
        items = model_class.query.order_by(getattr(model_class, name_field)).all()
        return jsonify([_project(i) for i in items]), 200

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
        # CanonicalLib extra field. #875: this is UNIQUE now, and the check
        # mirrors the `name already exists` 409 a few lines above — the name
        # was guarded here and the URL was not, which is how `icd10` came to
        # hold `snomed`'s URL in production and made the resolver answer with
        # the wrong library.
        if hasattr(model_class, 'canonical_lib_url') and 'canonical_lib_url' in data:
            from app.services.canonical_libs import (normalise_lib_url,
                                                     url_conflict,
                                                     url_convention_error)
            url = normalise_lib_url(_sanitize(data['canonical_lib_url']))
            # #923: UNIQUE said no two libraries may share a url; it never said
            # what a url should BE. snomed's was a human browser address with a
            # perspective, a concept id, an edition and a language list, served
            # as `compose.include[].system` for every SNOMED value.
            bad = url_convention_error(name_val, url)
            if bad:
                return jsonify({'error': bad, 'canonical_lib_url': url}), 400
            clash = url_conflict(url)
            if clash is not None:
                return jsonify({
                    'error': f'canonical_lib_url already belongs to '
                             f'{clash.canonical_lib_name!r}',
                    'canonical_lib_url': url,
                }), 409
            item.canonical_lib_url = url

        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    @bp.route(f'{url}/<guid>', methods=['GET'], endpoint=f'{url}_read')
    @_read_gate
    def read_item(guid):
        if not _is_valid_uuid(guid):
            return jsonify({'error': 'Invalid GUID'}), 400
        item = model_class.query.filter_by(guid=guid).first()
        if not item:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(_project(item)), 200

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
            # #922: the name column is UNIQUE on all six models this factory
            # serves, and CREATE above has answered 409 for a taken name
            # since it was written. UPDATE checked nothing, so the only thing
            # standing here was the database constraint -- and it speaks SQL:
            # renaming to a taken name raised an unhandled IntegrityError and
            # the caller got a bare 500.
            #
            # Uses the service the rest of this codebase already uses
            # (routes/concepts.py, routes/values.py, api/plandefinitions.py
            # and three more) rather than a seventh inline query. `lookup_tables`
            # was the exception on both paths, which is the whole finding.
            new_name = _sanitize(data[name_field])
            if new_name != getattr(item, name_field):
                error = NameUniquenessService.validate_name_for_manual_entry(
                    new_name, model_class, name_field, exclude_guid=item.guid)
                if error:
                    return jsonify({'error': error}), 409
            setattr(item, name_field, new_name)
        if display_field and display_field in data:
            setattr(item, display_field, _sanitize(data[display_field]))
        if 'author' in data:
            item.author = _sanitize(data['author'])
        if hasattr(item, 'canonical_lib_url') and 'canonical_lib_url' in data:
            from app.services.canonical_libs import (normalise_lib_url,
                                                     url_conflict,
                                                     url_convention_error)
            url = normalise_lib_url(_sanitize(data['canonical_lib_url']))
            # #923. The name here is the one the row will END UP with: a rename
            # and a url change can arrive in the same PUT, and checking the old
            # name would validate against the wrong convention.
            bad = url_convention_error(getattr(item, name_field, None), url)
            if bad:
                return jsonify({'error': bad, 'canonical_lib_url': url}), 400
            # exclude_guid, or the row conflicts with itself on every save
            clash = url_conflict(url, exclude_guid=item.guid)
            if clash is not None:
                return jsonify({
                    'error': f'canonical_lib_url already belongs to '
                             f'{clash.canonical_lib_name!r}',
                    'canonical_lib_url': url,
                }), 409
            item.canonical_lib_url = url
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
# #925: every read posture below is a DECISION with its consumer named. A
# survey of all 26 repos found who actually calls each path and whether that
# caller sends a credential; `public_read=True` means a DEPLOYED consumer reads
# it with none, so gating it would break that consumer — one of them silently.
#
# `public_read=False` is the goal state for all six. The blocker is above: plan
# has no machine-auth door, so these callers have nothing to send. #931 carries
# it, including a cheaper route for canonical-libs specifically: cdr's gate needs
# only three fields, so a narrow public endpoint would let the FULL table be
# gated without giving cdr a credential at all.

# cdr1's whole-system assertion gate (#874) reads this to learn which libraries
# are whole-system answer spaces, through a client that sends only
# `X-Operator-Session-Id`. Gating it would degrade a deployed SECURITY control
# to its floor — it would still refuse `icd11-mms` and `icd10`, but would stop
# following plan for anything flagged later.
_crud_routes(lookup_bp, '/canonical-libs', CanonicalLib, 'canonical_lib_name', 'canonical_lib_display_text', public_read=True)

# GATED. The only non-plan reference is `sim.pdhc/concepts/load_to_plan.py:110`,
# and it calls `/api/v1/concept-types` WITHOUT the `/lookup` prefix — measured
# 404 in production, alongside `/api/v1/canonical-libs` on the next line of that
# tool. So that caller is already broken and gating this breaks nothing. (Its
# own bug is not fixed here; it is not this ticket.)
_crud_routes(lookup_bp, '/concept-types', ConceptType, 'concept_type_name', 'concept_type_display_text', public_read=False)

# request.pdhc's `context_service.py:61-62` reads both of these with
# `{'Accept': 'application/json'}` and nothing else. Its own comment says a
# plan failure "doesn't regress every concept to 'text'/no-unit" because of
# stale-if-error — which means gating these would regress exactly that, SILENTLY,
# on the next cold start rather than at the moment of the change.
_crud_routes(lookup_bp, '/response-types', ResponseType, 'response_type_name', 'response_type_display_text', public_read=True)
_crud_routes(lookup_bp, '/units', Unit, 'unit_name', 'unit_display_text', public_read=True)

# request.pdhc's `plan_definition_service.py:96` sends `_headers()`, which LOOKS
# like a credential and is not: `{'Accept': ...} | outbound_session_headers()`.
# I read it as safe to gate on the first pass and was wrong; the difference is
# worth the comment.
_crud_routes(lookup_bp, '/plandef-types', PlanDefType, 'plandef_type_name', 'plandef_type_display_text', public_read=True)

# GATED. No consumer in any of the 26 repos, in Python, JS, HTML or shell.
_crud_routes(lookup_bp, '/intended-uses', IntendedUse, 'intended_use_name', 'intended_use_display_text', public_read=False)


# ---------------------------------------------------------------------------
# Values CRUD
# ---------------------------------------------------------------------------

@lookup_bp.route('/values', methods=['GET'])
@requires_role('read_only')
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
@requires_role('read_only')
def list_valuesets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    page = max(1, page)
    per_page = max(1, min(200, per_page))
    pagination = ValueSet.query.order_by(ValueSet.valueset_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        'items': [i.to_dict(include_values=False) for i in pagination.items],
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
    db.session.flush()

    # Accept values with sort_order during creation
    values_list = data.get('values', [])
    for idx, entry in enumerate(values_list, start=1):
        value_guid = entry.get('value_guid') if isinstance(entry, dict) else entry
        if not value_guid or not _is_valid_uuid(value_guid):
            continue
        if not ValueCatalog.query.filter_by(guid=value_guid).first():
            continue
        sort_order = entry.get('sort_order', idx) if isinstance(entry, dict) else idx
        link = ValueSetValue(
            valueset_guid=item.guid,
            value_guid=value_guid,
            sort_order=sort_order,
        )
        db.session.add(link)

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
@requires_role('read_only')
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
