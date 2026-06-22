"""Terminology API — plan.pdhc's surface for termbank integration.

Three endpoints:

  GET /api/v1/ValueSet/$validate-code?system=&code=
      Answers "is `(canonical_lib_name, canonical_refnumber)` referenced
      from any active Concept or ValueCatalog row?". Returns FHIR-shaped
      Parameters with a ``result`` boolean. Used by cdr.pdhc's $validate-code
      shim to gate writes (Phase 1 of the platform plan).

  GET /api/v1/termbank/concept/<system>/<code>
      Server-side proxy to termbank's ``GET /CodeSystem/<system>/<code>``.
      Lets the "View in termbank" panel call same-origin (no CORS) and
      benefits from the in-process TTL cache.

  GET /api/v1/termbank/search?q=&system=&limit=
      Server-side proxy to termbank's ``/search`` for the click-to-fill
      widget on Concept / ValueCatalog forms.

All three are GET-only. The blueprint is read-only by design — no
mutations live here.
"""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from app import db
from app.models.concept_models import CanonicalLib, Concept, ValueCatalog, ValueSet


bp = Blueprint("terminology_api", __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _operation_outcome(severity: str, code: str, text: str, status: int):
    """Return a (jsonify, status_code) tuple shaped like FHIR OperationOutcome."""
    return (
        jsonify({
            "resourceType": "OperationOutcome",
            "issue": [{
                "severity": severity,
                "code": code,
                "details": {"text": text},
            }],
        }),
        status,
    )


def _validate_parameters(result: bool, **fields):
    """Build a FHIR ``Parameters`` body for the $validate-code response."""
    parts = [{"name": "result", "valueBoolean": result}]
    for name, value in fields.items():
        if value is None:
            continue
        if isinstance(value, bool):
            parts.append({"name": name, "valueBoolean": value})
        else:
            parts.append({"name": name, "valueString": str(value)})
    return {"resourceType": "Parameters", "parameter": parts}


# ---------------------------------------------------------------------------
# $validate-code
# ---------------------------------------------------------------------------
@bp.get("/ValueSet/$validate-code")
@bp.get("/ValueSet/%24validate-code")  # for clients that escape '$'
def validate_code():
    """Is `(system, code)` adopted by plan.pdhc?

    "Adopted" means: there exists at least one ``Concept`` or
    ``ValueCatalog`` row with ``canonical_lib`` matching the named
    library and ``canonical_refnumber`` equal to ``code``. We don't
    require an "active" flag — plan.pdhc's editorial state IS the
    working set; if a row exists, the code is in scope.

    §6.2 — if the caller supplies a ``url`` or ``valueSet`` query
    parameter, the question becomes scoped: "is (system, code) in *this
    specific ValueSet*?". The scoped path is delegated to
    ``fhir_valueset.scoped_validate_code``. The unscoped path (no
    identifier) is unchanged and preserves the cdr.pdhc shim contract
    in ``cdr.pdhc/cdr_app/app/services/plan_client.py``.
    """
    scoping_url = (
        (request.args.get("url") or "").strip()
        or (request.args.get("valueSet") or "").strip()
    )
    if scoping_url:
        # Local import — avoids any startup-time import cycle and keeps
        # the global path fast (no extra module load on the cdr.pdhc
        # hot path).
        from app.api.fhir_valueset import (
            _extract_guid_from_url,
            scoped_validate_code,
        )
        target_guid = _extract_guid_from_url(scoping_url)
        if target_guid is None:
            return _operation_outcome(
                "error", "value",
                f"could not extract a ValueSet id from url={scoping_url!r}",
                400,
            )
        vs = ValueSet.query.filter_by(guid=target_guid).first()
        if vs is None:
            return _operation_outcome(
                "error", "not-found",
                f"ValueSet/{target_guid} not found", 404,
            )
        system = (request.args.get("system") or "").strip()
        code = (request.args.get("code") or "").strip()
        if not code:
            return _operation_outcome(
                "error", "required",
                "scoped $validate-code requires a 'code' parameter", 400,
            )
        return jsonify(scoped_validate_code(vs, system, code))

    system = (request.args.get("system") or "").strip()
    code = (request.args.get("code") or "").strip()
    if not system or not code:
        return _operation_outcome(
            "error",
            "required",
            "Both 'system' and 'code' query parameters are required.",
            400,
        )

    lib = db.session.query(CanonicalLib).filter_by(
        canonical_lib_name=system
    ).first()
    if lib is None:
        return jsonify(_validate_parameters(
            result=False,
            message=(
                f"system '{system}' is not registered as a CanonicalLib "
                "in plan.pdhc"
            ),
        ))

    # Concept first (the rich PDHC clinical concept), then ValueCatalog
    # (individual answer values inside ValueSets).
    concept = db.session.query(Concept).filter_by(
        canonical_lib=lib.guid,
        canonical_refnumber=code,
    ).first()
    if concept is not None:
        return jsonify(_validate_parameters(
            result=True,
            display=concept.concept_name,
            ref_via="Concept",
            ref_guid=concept.guid,
            system=system,
            code=code,
        ))

    value = db.session.query(ValueCatalog).filter_by(
        canonical_lib=lib.guid,
        canonical_refnumber=code,
    ).first()
    if value is not None:
        return jsonify(_validate_parameters(
            result=True,
            display=value.value_name,
            ref_via="ValueCatalog",
            ref_guid=value.guid,
            system=system,
            code=code,
        ))

    return jsonify(_validate_parameters(
        result=False,
        message=(
            "not adopted by plan.pdhc — "
            "no Concept or ValueCatalog references this canonical"
        ),
        system=system,
        code=code,
    ))


# ---------------------------------------------------------------------------
# Termbank proxies
# ---------------------------------------------------------------------------
@bp.get("/termbank/concept/<string:system>/<path:code>")
def termbank_concept_proxy(system: str, code: str):
    """Proxy ``GET termbank.pdhc/CodeSystem/<system>/<code>``.

    Powers the "View in termbank" panel on Concept / ValueCatalog views.
    Same-origin so the browser doesn't need CORS gymnastics; cached via
    the TermbankClient's in-process TTL.
    """
    client = current_app.termbank_client
    data = client.lookup(system, code)
    if data is None:
        return _operation_outcome(
            "warning",
            "not-found",
            f"termbank has no concept for system='{system}' code='{code}' "
            "(or termbank is currently unreachable).",
            404,
        )
    return jsonify(data)


@bp.get("/termbank/search")
def termbank_search_proxy():
    """Proxy ``GET termbank.pdhc/search?q=&system=&limit=``.

    Powers the click-to-fill widget on Concept / ValueCatalog create-edit
    forms. Returns whatever termbank returns; if termbank is unreachable
    the response will have an ``error`` field and an empty ``results``.
    """
    q = (request.args.get("q") or "").strip()
    system = (request.args.get("system") or "").strip() or None
    try:
        limit = max(1, min(int(request.args.get("limit", 20)), 200))
    except (TypeError, ValueError):
        limit = 20
    client = current_app.termbank_client
    return jsonify(client.search(q, system=system, limit=limit))
