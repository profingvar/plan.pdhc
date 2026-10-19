"""Shared FHIR-shaped response helpers for the terminology profile.

Single source of truth for:
- OperationOutcome shape (errors)
- Parameters body shape (operation responses + POST inputs)
- application/fhir+json Content-Type

Used by the new ValueSet / CodeSystem / ConceptMap blueprints introduced
under plan_pdhc_fhir_terminology_profile_instruction.md §6. The existing
`app/api/terminology.py` retains its own private copies for backward
compatibility; new code should import from here.

See plan_pdhc_fhir_terminology_profile_DECISIONS.md D3 (URL scheme) and
the instruction doc §6.5 (cross-cutting I/O conventions) for context.
"""
from __future__ import annotations

from typing import Any

from flask import Response, jsonify, request


FHIR_CONTENT_TYPE = 'application/fhir+json'

# FHIR R5 PublicationStatus. `unknown` exists for when the status cannot be
# determined; we always can, so it is deliberately not produced here.
FHIR_PUBLICATION_STATUSES = ('draft', 'active', 'retired', 'unknown')

# What Concept.status is allowed to hold. fhir_codesystem advertises exactly
# these three in its CodeSystem property description, and as of #839 a CHECK
# constraint enforces them — the column is a bare String(20) and accepted any
# value before that.
CONCEPT_STATUSES = ('draft', 'active', 'retired')


def derive_publication_status(statuses) -> str:
    """FHIR resource-level status, derived from the content's own statuses.

    #839 — the three terminology wrappers each hardcoded ``'status': 'active'``
    while every Concept underneath carried ``status='draft'``. A client reading
    both was told the CodeSystem was active and that every concept in it was
    editorially draft, which cannot both be useful.

    The rule, and why:

      * any content ``active``  -> ``active``. A resource that publishes even
        one adopted concept is in use.
      * content, all ``retired`` -> ``retired``.
      * anything else, including no content at all -> ``draft``. Nothing has
        been adopted, so claiming otherwise is the bug this function exists to
        remove.

    Unrecognised and empty values are ignored rather than trusted, so a stray
    status cannot promote a resource.
    """
    seen = {str(s).strip().lower() for s in statuses
            if s is not None and str(s).strip()}
    seen &= set(CONCEPT_STATUSES)
    if 'active' in seen:
        return 'active'
    if seen == {'retired'}:
        return 'retired'
    return 'draft'



# ---------------------------------------------------------------------------
# OperationOutcome
# ---------------------------------------------------------------------------
def operation_outcome(
    severity: str,
    code: str,
    text: str,
    status: int,
) -> tuple[Response, int]:
    """Build a FHIR OperationOutcome response.

    severity: 'fatal' | 'error' | 'warning' | 'information'
    code:     FHIR issue code (e.g. 'required', 'not-found', 'exception')
    text:     human-readable diagnostic
    status:   HTTP status code

    Returns (flask_response, status) — ready to ``return`` from a route.
    Content-Type is set to ``application/fhir+json``.
    """
    body = {
        'resourceType': 'OperationOutcome',
        'issue': [{
            'severity': severity,
            'code': code,
            'details': {'text': text},
        }],
    }
    resp = jsonify(body)
    resp.headers['Content-Type'] = FHIR_CONTENT_TYPE
    return resp, status


# ---------------------------------------------------------------------------
# Parameters (response shape for FHIR operations)
# ---------------------------------------------------------------------------
def parameters_response(result: bool, **fields: Any) -> dict[str, Any]:
    """Build a FHIR Parameters body for an operation response.

    The canonical first parameter is named 'result' (Boolean). Additional
    keyword fields are appended as valueBoolean (if bool) or valueString
    (otherwise). None values are omitted.

    Returns a plain dict — wrap with ``fhir_json_response()`` (or jsonify)
    at the call site.
    """
    parts: list[dict] = [{'name': 'result', 'valueBoolean': result}]
    for name, value in fields.items():
        if value is None:
            continue
        if isinstance(value, bool):
            parts.append({'name': name, 'valueBoolean': value})
        else:
            parts.append({'name': name, 'valueString': str(value)})
    return {'resourceType': 'Parameters', 'parameter': parts}


def fhir_json_response(body: dict, status: int = 200) -> tuple[Response, int]:
    """Wrap a FHIR resource dict in a Flask response with the FHIR
    content type set."""
    resp = jsonify(body)
    resp.headers['Content-Type'] = FHIR_CONTENT_TYPE
    return resp, status


# ---------------------------------------------------------------------------
# Parameters body parsing (POST inputs)
# ---------------------------------------------------------------------------
_VALUE_KEYS = (
    'valueBoolean',
    'valueString',
    'valueCode',
    'valueInteger',
    'valueUrl',
    'valueUri',
)


def parse_parameters_body(req_or_body: Any = None) -> dict[str, Any]:
    """Parse a FHIR Parameters body POSTed to an operation.

    Returns a flat dict mapping each parameter name to its first
    recognised value (Boolean, String, Code, Integer, Url, or Uri).
    Returns an empty dict if no body is present or the body isn't a
    Parameters resource — callers should check for required fields
    explicitly and return OperationOutcome(required) if missing.

    Accepts a Flask request object (defaults to the current request) or
    a body dict directly.
    """
    if req_or_body is None:
        body = request.get_json(silent=True) or {}
    elif isinstance(req_or_body, dict):
        body = req_or_body
    else:
        body = req_or_body.get_json(silent=True) or {}

    if body.get('resourceType') != 'Parameters':
        return {}

    out: dict[str, Any] = {}
    for p in body.get('parameter') or []:
        name = p.get('name')
        if not name:
            continue
        for key in _VALUE_KEYS:
            if key in p:
                out[name] = p[key]
                break
    return out
