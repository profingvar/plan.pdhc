"""FHIR R5 CodeSystem resource + ``$lookup`` operation (§6.3).

Publishes plan.pdhc's local concept set as the single CodeSystem
``plan-pdhc-local`` (ADR D2). The code identifier inside every entry
is the ``Concept.guid`` (ADR D1) — paired with ``concept_display_text``
or ``concept_name`` as ``display``.

``$lookup`` is a thin two-branch facade:

  - If ``system`` matches the local CodeSystem URL → return Concept
    properties from this database.
  - Otherwise resolve ``system`` as a registered ``CanonicalLib``
    (URL or name) and delegate to the existing
    ``TermbankClient.lookup()`` — the cached HTTP client that also
    backs ``/api/v1/termbank/concept/...``.

Routes registered under ``/api/v1``:

  GET  /CodeSystem                — searchset Bundle (the singleton
                                     platform CodeSystem)
  GET  /CodeSystem/{id}           — read the CodeSystem
  GET  /CodeSystem/$lookup        — lookup by query params
  POST /CodeSystem/$lookup        — lookup by Parameters body
"""
from __future__ import annotations

import uuid as uuid_mod
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request

from app import db
from app.api.fhir_helpers import (
    fhir_json_response,
    operation_outcome,
    parse_parameters_body,
)
from app.api.fhir_valueset import resolve_canonical_lib
from app.models.concept_models import (
    LOCAL_CODESYSTEM_ID,
    PLAN_BASE,
    CanonicalLib,
    Concept,
    fhir_canonical_url,
)


def _codesystem_version() -> str:
    """FHIR `version` for the local CodeSystem (ADR D4).

    The local CodeSystem is the union of all Concepts; its effective
    version is the max ``Concept.vers_number`` — monotonically increasing
    as any concept gets bumped, matching FHIR semantics. Returns "1" when
    the table is empty (first deploy, before any imports).
    """
    n = db.session.query(db.func.max(Concept.vers_number)).scalar()
    return str(n or 1)


fhir_codesystem_bp = Blueprint('fhir_codesystem', __name__)

# Local CodeSystem canonical URL — emitted on every read and matched
# against incoming ``system`` parameters.
LOCAL_CS_URL = fhir_canonical_url('CodeSystem', LOCAL_CODESYSTEM_ID)
LOCAL_CS_NAME = 'PlanPDHCLocal'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _str_param(params: dict, key: str) -> str:
    v = params.get(key)
    if v is None:
        return ''
    return str(v).strip()


def _local_display(c: Concept) -> str:
    return c.concept_display_text or c.concept_name or c.guid


def _property_part(code: str, value: str) -> dict:
    """Build a FHIR Parameters 'property' part for $lookup responses."""
    return {
        'name': 'property',
        'part': [
            {'name': 'code', 'valueCode': code},
            {'name': 'value', 'valueString': str(value)},
        ],
    }


# ADR D6 — property URI scheme is {LOCAL_CS_URL}#{property-code}.
# Defined inline below as f-strings so the URIs stay in sync with
# LOCAL_CS_URL if PLAN_BASE ever moves.
CODESYSTEM_PROPERTY_DEFS = [
    {
        'code': 'canonical-lib',
        'uri': f'{LOCAL_CS_URL}#canonical-lib',
        'description': (
            'Name of the CanonicalLib the Concept is bound to '
            '(e.g. loinc, snomed). Empty when the Concept is locally '
            'defined and not yet mapped.'
        ),
        'type': 'string',
    },
    {
        'code': 'canonical-ref',
        'uri': f'{LOCAL_CS_URL}#canonical-ref',
        'description': (
            "The canonical_refnumber within the bound CanonicalLib "
            "(e.g. '4548-4' for LOINC HbA1c)."
        ),
        'type': 'string',
    },
    {
        'code': 'status',
        'uri': f'{LOCAL_CS_URL}#status',
        'description': "Concept editorial status (draft, active, retired).",
        'type': 'string',
    },
]


# ---------------------------------------------------------------------------
# CodeSystem resource construction
# ---------------------------------------------------------------------------
def _concept_to_fhir_entry(c: Concept,
                            lib_name_by_guid: dict[str, str]) -> dict:
    entry: dict = {
        'code': c.guid,  # ADR D1
        'display': _local_display(c),
    }
    if c.concept_explain:
        entry['definition'] = c.concept_explain

    props: list[dict] = []
    if c.canonical_lib and c.canonical_lib in lib_name_by_guid:
        props.append(_property_part(
            'canonical-lib', lib_name_by_guid[c.canonical_lib],
        ))
    if c.canonical_refnumber:
        props.append(_property_part('canonical-ref', c.canonical_refnumber))
    if getattr(c, 'status', None):
        props.append(_property_part('status', c.status))

    if props:
        # CodeSystem.concept[].property uses a simpler shape than the
        # $lookup Parameters part — flatten it here.
        entry['property'] = [
            {'code': p['part'][0]['valueCode'],
             'valueString': p['part'][1]['valueString']}
            for p in props
        ]
    return entry


def _build_codesystem(*, include_concepts: bool = True) -> dict:
    """Project the local concept set into a FHIR R5 CodeSystem."""
    concepts = (
        Concept.query.order_by(Concept.concept_name)
        if include_concepts
        else Concept.query
    ).all()
    total = len(concepts)

    # Pre-fetch lib names so we don't N+1 inside the loop.
    lib_guids = {c.canonical_lib for c in concepts if c.canonical_lib}
    libs = CanonicalLib.query.filter(CanonicalLib.guid.in_(lib_guids)).all()
    lib_name_by_guid = {l.guid: l.canonical_lib_name for l in libs}

    body: dict = {
        'resourceType': 'CodeSystem',
        'id': LOCAL_CODESYSTEM_ID,
        'url': LOCAL_CS_URL,
        'version': _codesystem_version(),
        'name': LOCAL_CS_NAME,
        'title': 'plan.pdhc local concept system',
        'status': 'active',
        'experimental': False,
        'date': _now_iso(),
        'publisher': 'PDHC',
        'description': (
            'All locally-defined concepts in plan.pdhc, identified by '
            'Concept.guid (ADR D1). Each entry carries its canonical_lib '
            'binding as a property; the full local↔canonical mapping is '
            'published separately as the ConceptMap '
            '"plan-pdhc-canonical-bindings".'
        ),
        'caseSensitive': True,
        'content': 'complete' if include_concepts else 'not-present',
        'count': total,
        'property': CODESYSTEM_PROPERTY_DEFS,
    }
    if include_concepts:
        body['concept'] = [
            _concept_to_fhir_entry(c, lib_name_by_guid) for c in concepts
        ]
    return body


# ---------------------------------------------------------------------------
# $lookup — local and delegated paths
# ---------------------------------------------------------------------------
def _build_local_lookup_response(c: Concept) -> dict:
    """FHIR Parameters body for a local-system $lookup hit."""
    parts: list[dict] = [
        {'name': 'name', 'valueString': LOCAL_CS_NAME},
        {'name': 'version', 'valueString': _codesystem_version()},
        {'name': 'display', 'valueString': _local_display(c)},
    ]
    if c.concept_explain:
        parts.append({'name': 'definition', 'valueString': c.concept_explain})

    if c.canonical_lib:
        lib = CanonicalLib.query.filter_by(guid=c.canonical_lib).first()
        if lib is not None:
            parts.append(_property_part(
                'canonical-lib', lib.canonical_lib_name,
            ))
    if c.canonical_refnumber:
        parts.append(_property_part(
            'canonical-ref', c.canonical_refnumber,
        ))
    if getattr(c, 'status', None):
        parts.append(_property_part('status', c.status))

    return {'resourceType': 'Parameters', 'parameter': parts}


def _do_lookup(system: str, code: str):
    """Dispatch $lookup to the local CodeSystem path or to termbank."""
    if not system or not code:
        return operation_outcome(
            'error', 'required',
            "Both 'system' and 'code' parameters are required.", 400,
        )

    if system == LOCAL_CS_URL:
        c = Concept.query.filter_by(guid=code).first()
        if c is None:
            return operation_outcome(
                'error', 'not-found',
                f'no Concept with guid={code!r} in {LOCAL_CS_URL}', 404,
            )
        return fhir_json_response(_build_local_lookup_response(c))

    lib = resolve_canonical_lib(system)
    if lib is None:
        return operation_outcome(
            'error', 'not-found',
            f'system {system!r} is not the local CodeSystem and is not '
            'a registered CanonicalLib in plan.pdhc', 404,
        )

    # Delegate to termbank — pass the canonical_lib NAME, which is what
    # the existing TermbankClient + the termbank service itself use.
    client = current_app.termbank_client
    data = client.lookup(lib.canonical_lib_name, code)
    if data is None:
        return operation_outcome(
            'warning', 'not-found',
            f"termbank has no concept for system={lib.canonical_lib_name!r} "
            f"code={code!r} (or termbank is currently unreachable)", 404,
        )
    return fhir_json_response(data)


# ---------------------------------------------------------------------------
# GET /CodeSystem/{id}
# ---------------------------------------------------------------------------
@fhir_codesystem_bp.route('/CodeSystem/<id_>', methods=['GET'])
def read_codesystem(id_: str):
    if id_ != LOCAL_CODESYSTEM_ID:
        return operation_outcome(
            'error', 'not-found', f'CodeSystem/{id_} not found', 404,
        )
    return fhir_json_response(_build_codesystem())


# ---------------------------------------------------------------------------
# GET /CodeSystem — searchset Bundle
# ---------------------------------------------------------------------------
@fhir_codesystem_bp.route('/CodeSystem', methods=['GET'])
def search_codesystems():
    url_filter = (request.args.get('url') or '').strip() or None
    show = (url_filter is None) or (url_filter == LOCAL_CS_URL)
    if show:
        entries = [{
            'fullUrl': LOCAL_CS_URL,
            'resource': _build_codesystem(),
        }]
        total = 1
    else:
        entries = []
        total = 0
    return fhir_json_response({
        'resourceType': 'Bundle',
        'type': 'searchset',
        # bdl-18: searchsets require a self link.
        'link': [{'relation': 'self', 'url': request.url}],
        'total': total,
        'entry': entries,
    })


# ---------------------------------------------------------------------------
# GET /CodeSystem/$lookup
# ---------------------------------------------------------------------------
@fhir_codesystem_bp.route('/CodeSystem/$lookup', methods=['GET'])
@fhir_codesystem_bp.route('/CodeSystem/%24lookup', methods=['GET'])
def lookup_get():
    system = (request.args.get('system') or '').strip()
    code = (request.args.get('code') or '').strip()
    return _do_lookup(system, code)


# ---------------------------------------------------------------------------
# POST /CodeSystem/$lookup — Parameters body
# ---------------------------------------------------------------------------
@fhir_codesystem_bp.route('/CodeSystem/$lookup', methods=['POST'])
@fhir_codesystem_bp.route('/CodeSystem/%24lookup', methods=['POST'])
def lookup_post():
    params = parse_parameters_body()
    system = _str_param(params, 'system')
    code = _str_param(params, 'code')
    return _do_lookup(system, code)
