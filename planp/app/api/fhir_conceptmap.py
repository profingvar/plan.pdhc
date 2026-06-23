"""FHIR R5 ConceptMap resource + ``$translate`` operation (§6.4).

Projects plan.pdhc's local↔canonical mapping (every ``Concept`` row's
``canonical_lib`` + ``canonical_refnumber`` binding) as a single
ConceptMap whose source is the local CodeSystem ``plan-pdhc-local``
(ADR D2) and whose targets are the external CanonicalLib URLs.

Routes registered under ``/api/v1``:

  GET  /ConceptMap                    — searchset Bundle (the singleton
                                         platform ConceptMap)
  GET  /ConceptMap/{id}               — read the ConceptMap by id
  GET  /ConceptMap/$translate         — translate by query params
  POST /ConceptMap/$translate         — translate by Parameters body

Per ADR D1: local source code = ``Concept.guid``. Target code =
``Concept.canonical_refnumber``. Relationship: ``equivalent`` (plan.pdhc
treats the canonical binding as a 1:1 equivalence by design).

Per Risk §9.5: even though each Concept holds 0..1 canonical binding
today, the ``$translate`` response always shapes ``match`` as repeating
FHIR Parameters parts so a future N>1 binding doesn't break the
contract.
"""
from __future__ import annotations

import uuid as uuid_mod
from datetime import datetime, timezone

from flask import Blueprint, request

from app import db
from app.api.fhir_helpers import (
    fhir_json_response,
    operation_outcome,
    parse_parameters_body,
)
from app.models.concept_models import (
    CanonicalLib,
    Concept,
    LOCAL_CODESYSTEM_ID,
    LOCAL_CONCEPTMAP_ID,
    PLAN_BASE,
    fhir_canonical_url,
)


fhir_conceptmap_bp = Blueprint('fhir_conceptmap', __name__)

# The local CodeSystem URL — used as the ``source`` of every group and
# as the ``targetsystem`` for canonical→local translations.
LOCAL_CS_URL = fhir_canonical_url('CodeSystem', LOCAL_CODESYSTEM_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _is_valid_uuid(s: str) -> bool:
    try:
        uuid_mod.UUID(str(s))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def _str_param(params: dict, key: str) -> str:
    v = params.get(key)
    if v is None:
        return ''
    return str(v).strip()


def _local_display(c: Concept) -> str:
    return c.concept_display_text or c.concept_name or c.guid


def _resolve_lib_for_input(system_or_url: str) -> CanonicalLib | None:
    """Find a CanonicalLib by URL (FHIR-canonical form) or by name
    (cdr.pdhc/global form). Mirrors the lenience of
    ``fhir_valueset.resolve_canonical_lib`` for consistency."""
    if not system_or_url:
        return None
    lib = CanonicalLib.query.filter_by(canonical_lib_url=system_or_url).first()
    if lib is not None:
        return lib
    return CanonicalLib.query.filter_by(
        canonical_lib_name=system_or_url,
    ).first()


def _build_match_parameter(*, relationship: str, system: str, code: str,
                            display: str) -> dict:
    """Build a single ``match`` Parameters part per FHIR R5 $translate."""
    return {
        'name': 'match',
        'part': [
            {'name': 'relationship', 'valueCode': relationship},
            {'name': 'concept', 'valueCoding': {
                'system': system,
                'code': code,
                'display': display,
            }},
        ],
    }


def _build_translate_response(
    *, result: bool, message: str, matches: list[dict],
) -> dict:
    """Build the FHIR Parameters body for $translate.

    ``matches`` is a list of dicts produced by ``_build_match_parameter``
    (already in Parameters-part shape). One ``match`` parameter per match.
    Risk §9.5 — ``match`` is always shaped as a repeating parameter so
    multi-binding support is additive.
    """
    parts: list[dict] = [{'name': 'result', 'valueBoolean': result}]
    if message:
        parts.append({'name': 'message', 'valueString': message})
    parts.extend(matches)
    return {'resourceType': 'Parameters', 'parameter': parts}


# ---------------------------------------------------------------------------
# ConceptMap resource construction
# ---------------------------------------------------------------------------
def _build_conceptmap() -> dict:
    """Project every Concept row with a complete canonical binding into
    a single FHIR R5 ConceptMap. Groups are keyed by target system."""
    concepts = Concept.query.filter(
        Concept.canonical_lib.isnot(None),
        Concept.canonical_refnumber.isnot(None),
    ).all()

    libs_by_guid: dict[str, CanonicalLib] = {}
    by_lib_guid: dict[str, list[Concept]] = {}
    for c in concepts:
        if not c.canonical_refnumber:
            continue
        if c.canonical_lib not in libs_by_guid:
            lib = CanonicalLib.query.filter_by(guid=c.canonical_lib).first()
            if lib is None or not lib.canonical_lib_url:
                continue
            libs_by_guid[c.canonical_lib] = lib
        by_lib_guid.setdefault(c.canonical_lib, []).append(c)

    groups: list[dict] = []
    for lib_guid, members in by_lib_guid.items():
        lib = libs_by_guid[lib_guid]
        elements = [{
            'code': c.guid,
            'display': _local_display(c),
            'target': [{
                'code': c.canonical_refnumber,
                'display': _local_display(c),
                'relationship': 'equivalent',
            }],
        } for c in members]
        groups.append({
            'source': LOCAL_CS_URL,
            'target': lib.canonical_lib_url,
            'element': elements,
        })

    return {
        'resourceType': 'ConceptMap',
        'id': LOCAL_CONCEPTMAP_ID,
        'url': fhir_canonical_url('ConceptMap', LOCAL_CONCEPTMAP_ID),
        'version': '1',
        'name': 'PlanPDHCCanonicalBindings',
        'title': 'plan.pdhc local concepts ↔ external canonicals',
        'status': 'active',
        'experimental': False,
        'date': _now_iso(),
        'publisher': 'PDHC',
        'description': (
            'Mapping from plan.pdhc local concepts (CodeSystem '
            f'{LOCAL_CODESYSTEM_ID}) to external canonicals registered '
            'as CanonicalLibs (LOINC, SNOMED, ICD-10, ATC, …).'
        ),
        # No sourceScopeUri: the FHIR R5 spec requires sourceScope[x]
        # to reference a ValueSet (not a CodeSystem). plan.pdhc does not
        # define a single ValueSet covering every local concept; the
        # source CodeSystem is identified per-group via group[].source
        # instead, which is FHIR-conformant and validates clean.
        'group': groups,
    }


# ---------------------------------------------------------------------------
# Translate logic — both directions
# ---------------------------------------------------------------------------
def _translate(
    system: str, code: str, targetsystem: str | None,
) -> dict:
    """Bidirectional translate.

      - If ``system`` == LOCAL_CS_URL: source code is a Concept.guid;
        return its canonical binding (filtered by targetsystem if given).
      - Otherwise ``system`` names a CanonicalLib (URL or name):
        source code is a canonical_refnumber; return the matching local
        Concept (only when ``targetsystem`` is absent or equals
        LOCAL_CS_URL).
    """
    if system == LOCAL_CS_URL:
        c = Concept.query.filter_by(guid=code).first()
        if c is None:
            return _build_translate_response(
                result=False,
                message=f'no plan.pdhc Concept with guid {code!r}',
                matches=[],
            )
        if not c.canonical_lib or not c.canonical_refnumber:
            return _build_translate_response(
                result=False,
                message=(
                    f'Concept {code!r} has no canonical binding '
                    '(canonical_lib / canonical_refnumber is null)'
                ),
                matches=[],
            )
        lib = CanonicalLib.query.filter_by(guid=c.canonical_lib).first()
        if lib is None or not lib.canonical_lib_url:
            return _build_translate_response(
                result=False,
                message=(
                    f'Concept {code!r} is bound to lib {c.canonical_lib!r}'
                    ' which has no canonical_lib_url'
                ),
                matches=[],
            )
        if targetsystem and lib.canonical_lib_url != targetsystem:
            return _build_translate_response(
                result=False,
                message=(
                    f'Concept {code!r} is bound to '
                    f'{lib.canonical_lib_url!r}, not to '
                    f'targetsystem {targetsystem!r}'
                ),
                matches=[],
            )
        return _build_translate_response(
            result=True, message='matched 1 target',
            matches=[_build_match_parameter(
                relationship='equivalent',
                system=lib.canonical_lib_url,
                code=c.canonical_refnumber,
                display=_local_display(c),
            )],
        )

    lib = _resolve_lib_for_input(system)
    if lib is None:
        return _build_translate_response(
            result=False,
            message=(
                f'system {system!r} is not registered as a CanonicalLib '
                'in plan.pdhc'
            ),
            matches=[],
        )
    if targetsystem and targetsystem != LOCAL_CS_URL:
        return _build_translate_response(
            result=False,
            message=(
                f'plan.pdhc only translates canonical→local; '
                f'targetsystem must be {LOCAL_CS_URL!r} (got '
                f'{targetsystem!r})'
            ),
            matches=[],
        )
    c = Concept.query.filter_by(
        canonical_lib=lib.guid, canonical_refnumber=code,
    ).first()
    if c is None:
        return _build_translate_response(
            result=False,
            message=(
                f'no plan.pdhc Concept binds '
                f'({lib.canonical_lib_name!r}, {code!r})'
            ),
            matches=[],
        )
    return _build_translate_response(
        result=True, message='matched 1 target',
        matches=[_build_match_parameter(
            relationship='equivalent',
            system=LOCAL_CS_URL,
            code=c.guid,
            display=_local_display(c),
        )],
    )


# ---------------------------------------------------------------------------
# GET /ConceptMap/{id}
# ---------------------------------------------------------------------------
@fhir_conceptmap_bp.route('/ConceptMap/<id_>', methods=['GET'])
def read_conceptmap(id_: str):
    if id_ != LOCAL_CONCEPTMAP_ID:
        return operation_outcome(
            'error', 'not-found', f'ConceptMap/{id_} not found', 404,
        )
    return fhir_json_response(_build_conceptmap())


# ---------------------------------------------------------------------------
# GET /ConceptMap — searchset Bundle
# ---------------------------------------------------------------------------
@fhir_conceptmap_bp.route('/ConceptMap', methods=['GET'])
def search_conceptmaps():
    url_filter = (request.args.get('url') or '').strip() or None
    canonical = fhir_canonical_url('ConceptMap', LOCAL_CONCEPTMAP_ID)
    show = (url_filter is None) or (url_filter == canonical)
    if show:
        entries = [{
            'fullUrl': canonical,
            'resource': _build_conceptmap(),
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
# GET /ConceptMap/$translate
# ---------------------------------------------------------------------------
@fhir_conceptmap_bp.route('/ConceptMap/$translate', methods=['GET'])
@fhir_conceptmap_bp.route('/ConceptMap/%24translate', methods=['GET'])
def translate_get():
    system = (request.args.get('system') or '').strip()
    code = (request.args.get('code') or '').strip()
    targetsystem = (request.args.get('targetsystem') or '').strip() or None
    if not system or not code:
        return operation_outcome(
            'error', 'required',
            "Both 'system' and 'code' query parameters are required.", 400,
        )
    return fhir_json_response(_translate(system, code, targetsystem))


# ---------------------------------------------------------------------------
# POST /ConceptMap/$translate — Parameters body
# ---------------------------------------------------------------------------
@fhir_conceptmap_bp.route('/ConceptMap/$translate', methods=['POST'])
@fhir_conceptmap_bp.route('/ConceptMap/%24translate', methods=['POST'])
def translate_post():
    params = parse_parameters_body()
    system = _str_param(params, 'system')
    code = _str_param(params, 'code')
    targetsystem = _str_param(params, 'targetsystem') or None
    if not system or not code:
        return operation_outcome(
            'error', 'required',
            "'system' and 'code' parameters are required in the "
            'Parameters body.', 400,
        )
    return fhir_json_response(_translate(system, code, targetsystem))
