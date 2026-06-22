"""FHIR R5 ValueSet resource + ``$expand`` operation (§6.1).

This blueprint publishes plan.pdhc's ValueSets as conformant FHIR R5
``ValueSet`` resources. It is **additive** — the existing custom CRUD
JSON at ``/api/v1/lookup/valuesets/{guid}`` is untouched (§2 regression
contract).

Routes registered under ``/api/v1``:

  GET  /ValueSet                      — searchset Bundle
                                        (``?url=``, ``?_count=``, ``?_offset=``)
  GET  /ValueSet/{guid}               — read FHIR ValueSet resource
  GET  /ValueSet/{guid}/$expand       — expand by id
  POST /ValueSet/$expand              — expand by Parameters body
                                        (``url`` | ``valueSet`` parameter)

Canonical url scheme per ADR D3:
  The ``url`` field on a resource is built via ``fhir_canonical_url()``
  (the single source of truth) — see ADR D3 + Risk §9.3. Routes remain
  under ``/api/v1/`` — the canonical url is an identifier and is not
  guaranteed to resolve. Search by ``?url=`` accepts both the new
  canonical form and the legacy ValueSet CRUD url emitted by
  ``ValueSet.to_dict()`` (transition rule D3.b).

Version per ADR D4: ``version = str(vers_number)``.

Status: every plan.pdhc ValueSet is emitted as ``status: active`` (the
schema has no dedicated status column; everything in the editorial set
is treated as in-use). If a dedicated status column is added later, this
can be sharpened without a route change.
"""
from __future__ import annotations

import uuid as uuid_mod
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Blueprint, jsonify, request

from app import db
from app.api.fhir_helpers import (
    fhir_json_response,
    operation_outcome,
    parameters_response,
    parse_parameters_body,
)
from app.models.concept_models import (
    CanonicalLib,
    PLAN_BASE,
    ValueCatalog,
    ValueSet,
    ValueSetValue,
    fhir_canonical_url,
    fhir_version,
)


fhir_valueset_bp = Blueprint('fhir_valueset', __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _is_valid_uuid(s: str) -> bool:
    try:
        uuid_mod.UUID(str(s))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _extract_guid_from_url(url: str) -> str | None:
    """Pull a UUID guid out of a canonical-form OR legacy ValueSet URL.

    Accepts (ADR D3 + D3.b):
      - ``<base>/fhir/ValueSet/<guid>``           (new canonical)
      - ``<base>/api/v1/valuesets/<guid>``        (legacy CRUD)
      - ``<base>/api/v1/lookup/valuesets/<guid>`` (route form)

    Returns the guid string if the last path segment is a valid UUID;
    None otherwise.
    """
    if not url:
        return None
    try:
        path = urlparse(url).path
    except ValueError:
        return None
    if not path:
        return None
    last = path.rstrip('/').rsplit('/', 1)[-1]
    return last if _is_valid_uuid(last) else None


def _value_rows(vs: ValueSet):
    """Yield (ValueSetValue link, ValueCatalog value, CanonicalLib lib)
    triples for every value in the ValueSet, ordered by ``sort_order``
    then by ``value_name``. Skips broken FK rows."""
    links = (
        ValueSetValue.query
        .filter_by(valueset_guid=vs.guid)
        .order_by(ValueSetValue.sort_order, ValueSetValue.id)
        .all()
    )
    for link in links:
        val = ValueCatalog.query.filter_by(guid=link.value_guid).first()
        if val is None:
            continue
        lib = CanonicalLib.query.filter_by(guid=val.canonical_lib).first()
        if lib is None:
            continue
        yield link, val, lib


def _build_compose(vs: ValueSet) -> dict:
    """Build ValueSet.compose: group values by their canonical_lib's url
    so the FHIR compose.include[].system is the lib URL and each system
    block lists the concepts under it."""
    grouped: dict[str, list[dict]] = {}
    for _, val, lib in _value_rows(vs):
        if not val.canonical_refnumber or not lib.canonical_lib_url:
            continue
        entry = {
            'code': val.canonical_refnumber,
            'display': val.value_display_text or val.value_name,
        }
        grouped.setdefault(lib.canonical_lib_url, []).append(entry)
    include = [
        {'system': system, 'concept': concepts}
        for system, concepts in grouped.items()
    ]
    return {'include': include}


def _build_expansion(vs: ValueSet) -> dict:
    """Build ValueSet.expansion.contains[] — flat list, one entry per
    resolvable (system, code, display) tuple."""
    contains: list[dict] = []
    for _, val, lib in _value_rows(vs):
        if not val.canonical_refnumber or not lib.canonical_lib_url:
            continue
        contains.append({
            'system': lib.canonical_lib_url,
            'code': val.canonical_refnumber,
            'display': val.value_display_text or val.value_name,
        })
    return {
        'identifier': f'urn:uuid:{uuid_mod.uuid4()}',
        'timestamp': _now_iso(),
        'total': len(contains),
        'contains': contains,
    }


def _to_fhir_valueset(vs: ValueSet, *, with_expansion: bool = False) -> dict:
    """Project a ValueSet model row into a FHIR R5 ValueSet resource."""
    body: dict = {
        'resourceType': 'ValueSet',
        'id': vs.guid,
        'url': fhir_canonical_url('ValueSet', vs.guid),
        'version': fhir_version(vs),
        'name': vs.valueset_name,
        'status': 'active',
        'experimental': False,
        'date': (
            vs.date_created.strftime('%Y-%m-%dT%H:%M:%SZ')
            if vs.date_created else _now_iso()
        ),
        'publisher': vs.author or 'PDHC',
        'compose': _build_compose(vs),
    }
    if vs.valueset_display_text:
        body['title'] = vs.valueset_display_text
    if vs.valueset_explanation:
        body['description'] = vs.valueset_explanation
    if with_expansion:
        body['expansion'] = _build_expansion(vs)
    return body


# ---------------------------------------------------------------------------
# Scoped $validate-code helpers (§6.2)
# ---------------------------------------------------------------------------
def resolve_canonical_lib(system_or_url: str) -> CanonicalLib | None:
    """Find a CanonicalLib by either ``canonical_lib_url`` (FHIR-canonical
    form, preferred) or ``canonical_lib_name`` (legacy/cdr.pdhc form).
    Returns None if neither matches."""
    if not system_or_url:
        return None
    lib = CanonicalLib.query.filter_by(canonical_lib_url=system_or_url).first()
    if lib is not None:
        return lib
    return CanonicalLib.query.filter_by(
        canonical_lib_name=system_or_url,
    ).first()


def scoped_validate_code(vs: ValueSet, system: str, code: str) -> dict:
    """Check whether ``(system, code)`` is a member of ``vs``'s expansion.

    Returns a FHIR ``Parameters`` body. ``system`` may be the CanonicalLib
    URL (FHIR-canonical form) OR its name (cdr.pdhc/global form); an
    empty ``system`` matches by code alone.

    Called from this file's POST handler and the scoped GET handler, AND
    delegated to from ``terminology.py::validate_code`` when ``?url=`` is
    present (§6.2 — keeping the cdr.pdhc global contract untouched).
    """
    valueset_canonical = fhir_canonical_url('ValueSet', vs.guid)

    target_lib = resolve_canonical_lib(system) if system else None
    if system and target_lib is None:
        return parameters_response(
            result=False,
            message=(
                f"system {system!r} is not registered as a CanonicalLib "
                'in plan.pdhc'
            ),
            system=system,
            code=code or None,
            valueset_url=valueset_canonical,
        )

    for _, val, lib in _value_rows(vs):
        if val.canonical_refnumber != code:
            continue
        if target_lib is not None and lib.guid != target_lib.guid:
            continue
        return parameters_response(
            result=True,
            display=val.value_display_text or val.value_name,
            system=lib.canonical_lib_url,
            code=code,
            valueset_url=valueset_canonical,
        )

    return parameters_response(
        result=False,
        message=f"code {code!r} is not in ValueSet/{vs.guid}",
        system=system or None,
        code=code,
        valueset_url=valueset_canonical,
    )


# ---------------------------------------------------------------------------
# GET /ValueSet/{guid}
# ---------------------------------------------------------------------------
@fhir_valueset_bp.route('/ValueSet/<guid>', methods=['GET'])
def read_valueset(guid: str):
    if not _is_valid_uuid(guid):
        return operation_outcome(
            'error', 'value',
            f'invalid id {guid!r} — expected a UUID', 400,
        )
    vs = ValueSet.query.filter_by(guid=guid).first()
    if vs is None:
        return operation_outcome(
            'error', 'not-found', f'ValueSet/{guid} not found', 404,
        )
    return fhir_json_response(_to_fhir_valueset(vs))


# ---------------------------------------------------------------------------
# GET /ValueSet — searchset Bundle
# ---------------------------------------------------------------------------
@fhir_valueset_bp.route('/ValueSet', methods=['GET'])
def search_valuesets():
    url_filter = (request.args.get('url') or '').strip() or None

    if url_filter:
        target_guid = _extract_guid_from_url(url_filter)
        if target_guid is None:
            # Unparseable url → empty bundle (FHIR search returns empty,
            # not an error, when filters yield no matches).
            target_guid = '00000000-0000-0000-0000-000000000000'
        query = ValueSet.query.filter_by(guid=target_guid)
    else:
        query = ValueSet.query

    count = max(1, min(200, request.args.get('_count', 20, type=int)))
    offset = max(0, request.args.get('_offset', 0, type=int))

    total = query.count()
    rows = (
        query.order_by(ValueSet.valueset_name)
        .offset(offset)
        .limit(count)
        .all()
    )

    entries = [
        {
            'fullUrl': fhir_canonical_url('ValueSet', vs.guid),
            'resource': _to_fhir_valueset(vs),
        }
        for vs in rows
    ]

    bundle = {
        'resourceType': 'Bundle',
        'type': 'searchset',
        'total': total,
        'entry': entries,
    }
    return fhir_json_response(bundle)


# ---------------------------------------------------------------------------
# GET /ValueSet/{guid}/$expand
# ---------------------------------------------------------------------------
@fhir_valueset_bp.route('/ValueSet/<guid>/$expand', methods=['GET'])
@fhir_valueset_bp.route('/ValueSet/<guid>/%24expand', methods=['GET'])
def expand_valueset_by_id(guid: str):
    if not _is_valid_uuid(guid):
        return operation_outcome(
            'error', 'value',
            f'invalid id {guid!r} — expected a UUID', 400,
        )
    vs = ValueSet.query.filter_by(guid=guid).first()
    if vs is None:
        return operation_outcome(
            'error', 'not-found', f'ValueSet/{guid} not found', 404,
        )
    return fhir_json_response(_to_fhir_valueset(vs, with_expansion=True))


# ---------------------------------------------------------------------------
# POST /ValueSet/$expand — Parameters body input
# ---------------------------------------------------------------------------
@fhir_valueset_bp.route('/ValueSet/$expand', methods=['POST'])
@fhir_valueset_bp.route('/ValueSet/%24expand', methods=['POST'])
def expand_valueset_by_parameters():
    params = parse_parameters_body()
    url = params.get('url') or params.get('valueSet')
    if not url:
        return operation_outcome(
            'error', 'required',
            "POST $expand requires a 'url' or 'valueSet' parameter in the "
            'Parameters body. To expand a known id, GET '
            '/ValueSet/{id}/$expand instead.', 400,
        )
    target_guid = _extract_guid_from_url(str(url))
    if target_guid is None:
        return operation_outcome(
            'error', 'value',
            f'could not extract a ValueSet id from url={url!r}', 400,
        )
    vs = ValueSet.query.filter_by(guid=target_guid).first()
    if vs is None:
        return operation_outcome(
            'error', 'not-found', f'ValueSet/{target_guid} not found', 404,
        )
    return fhir_json_response(_to_fhir_valueset(vs, with_expansion=True))


# ---------------------------------------------------------------------------
# §6.2 — scoped $validate-code
# (The unscoped/global form stays in terminology.py for backward compat
# with cdr.pdhc. terminology.py delegates to scoped_validate_code() above
# when a ?url= or ?valueSet= identifier is supplied.)
# ---------------------------------------------------------------------------
@fhir_valueset_bp.route('/ValueSet/<guid>/$validate-code', methods=['GET'])
@fhir_valueset_bp.route('/ValueSet/<guid>/%24validate-code', methods=['GET'])
def scoped_validate_code_by_id(guid: str):
    if not _is_valid_uuid(guid):
        return operation_outcome(
            'error', 'value',
            f'invalid id {guid!r} — expected a UUID', 400,
        )
    vs = ValueSet.query.filter_by(guid=guid).first()
    if vs is None:
        return operation_outcome(
            'error', 'not-found', f'ValueSet/{guid} not found', 404,
        )
    system = (request.args.get('system') or '').strip()
    code = (request.args.get('code') or '').strip()
    if not code:
        return operation_outcome(
            'error', 'required',
            "'code' query parameter is required", 400,
        )
    return fhir_json_response(scoped_validate_code(vs, system, code))


@fhir_valueset_bp.route('/ValueSet/$validate-code', methods=['POST'])
@fhir_valueset_bp.route('/ValueSet/%24validate-code', methods=['POST'])
def scoped_validate_code_by_post():
    """POST $validate-code with Parameters body. Always scoped — the
    Parameters body MUST include ``url`` (or ``valueSet``) to identify a
    target ValueSet. For unscoped global validation, callers should
    continue using GET ``/ValueSet/$validate-code?system=&code=`` (the
    existing cdr.pdhc contract handled in terminology.py)."""
    params = parse_parameters_body()
    url = params.get('url') or params.get('valueSet')
    code = params.get('code') or ''
    system = params.get('system') or ''
    if not url:
        return operation_outcome(
            'error', 'required',
            "POST /ValueSet/$validate-code requires a 'url' or 'valueSet' "
            'parameter in the Parameters body. For unscoped global '
            'validation, use GET /ValueSet/$validate-code?system=&code=.',
            400,
        )
    if not code:
        return operation_outcome(
            'error', 'required',
            "'code' parameter is required", 400,
        )
    target_guid = _extract_guid_from_url(str(url))
    if target_guid is None:
        return operation_outcome(
            'error', 'value',
            f'could not extract a ValueSet id from url={url!r}', 400,
        )
    vs = ValueSet.query.filter_by(guid=target_guid).first()
    if vs is None:
        return operation_outcome(
            'error', 'not-found',
            f'ValueSet/{target_guid} not found', 404,
        )
    return fhir_json_response(
        scoped_validate_code(vs, str(system), str(code)),
    )
