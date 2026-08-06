"""Transfer API — promote synthetic cdr_6 content into a working CDR (#530).

plan.pdhc is the authoring plane and does NOT move CDR data itself. These
endpoints are a THIN PROXY over cdr_6's server-side engine (#529,
``POST /api/v1/transfer``): plan only triggers it. The source is always
cdr_6 (the synthetic sim sink) — no real, spärr/consent-protected patient
data can be moved — so any authenticated ``read_write`` professional may use it.

  GET  /api/v1/transfer/targets   — config + the destination CDRs to offer
  POST /api/v1/transfer/preview   — dry-run count (proxies cdr_6 dry_run=true)
  POST /api/v1/transfer/execute   — real copy/move (proxies cdr_6), audit-logged

cdr_6 is sim-only (its top_rules Rule 2), so we call it presenting
``X-Source-Service: sim.pdhc`` with ``CDR6_SERVICE_KEY`` (= cdr_6's sim key).
"""
from __future__ import annotations

import requests
from flask import Blueprint, current_app, jsonify, request, session

from app.api.auth import requires_role

transfer_bp = Blueprint("transfer", __name__)

SOURCE = "cdr_6 (synthetic test sink)"


def _targets() -> list:
    return current_app.config.get("CDR_TRANSFER_TARGETS", []) or []


def _call_cdr6(payload: dict):
    """POST to cdr_6's /api/v1/transfer. Returns (body_dict, status_code).
    Degrades gracefully — never raises — mirroring the rosetta proxy (#523)."""
    base = (current_app.config.get("CDR6_BASE_URL") or "").rstrip("/")
    if not base:
        return {"error": "cdr6_not_configured"}, 503
    try:
        r = requests.post(
            base + "/api/v1/transfer",
            json=payload,
            headers={
                # cdr_6 is sim-only (its Rule 2): present the sim identity.
                "X-Source-Service": "sim.pdhc",
                "X-Service-Key": current_app.config.get("CDR6_SERVICE_KEY", ""),
                "Content-Type": "application/json",
            },
            timeout=current_app.config.get("CDR6_TIMEOUT", 120),
        )
    except requests.RequestException as e:
        return {"error": "cdr6_unreachable", "detail": str(e)[:200]}, 502
    try:
        return r.json(), r.status_code
    except ValueError:
        return {"error": "cdr6_bad_response", "status": r.status_code}, 502


def _validate_to(body):
    """Return (to, error_response_or_none). Destination must be one we offer."""
    to = ((body or {}).get("to") or "").strip()
    if not to:
        return None, (jsonify({"error": "missing 'to' (destination CDR)"}), 400)
    if to not in _targets():
        return None, (jsonify({"error": f"unknown destination: {to!r}"}), 400)
    return to, None


@transfer_bp.route("/transfer/targets", methods=["GET"])
@requires_role("read_write")
def transfer_targets():
    """Populate the Transfer page: whether the feature is wired + the
    destination CDRs to offer. Source is fixed to cdr_6."""
    return jsonify({
        "configured": bool(current_app.config.get("CDR6_BASE_URL")),
        "source": SOURCE,
        "targets": _targets(),
    }), 200


@transfer_bp.route("/transfer/preview", methods=["POST"])
@requires_role("read_write")
def transfer_preview():
    """Dry-run: how many rows / runs would move. No writes."""
    body = request.get_json(silent=True) or {}
    to, err = _validate_to(body)
    if err:
        return err
    result, status = _call_cdr6({
        "to": to,
        "sim_run_id": body.get("sim_run_id") or None,
        "dry_run": True,
    })
    return jsonify(result), status


@transfer_bp.route("/transfer/execute", methods=["POST"])
@requires_role("read_write")
def transfer_execute():
    """Real copy (or move, with purge_source). Proxies cdr_6 and audit-logs."""
    body = request.get_json(silent=True) or {}
    to, err = _validate_to(body)
    if err:
        return err
    sim_run_id = body.get("sim_run_id") or None
    purge_source = bool(body.get("purge_source", False))

    payload = {"to": to, "sim_run_id": sim_run_id,
               "purge_source": purge_source, "dry_run": False}
    batch_size = body.get("batch_size")
    if batch_size is not None:
        payload["batch_size"] = batch_size

    result, status = _call_cdr6(payload)

    # Operation-log every execute (Rule 24), whatever the outcome.
    user_guid = (session.get("sso_user") or {}).get("user_guid")
    current_app.logger.info(
        "cdr6-transfer execute user=%s to=%s run=%s purge=%s -> "
        "status=%s verified=%s accepted=%s duplicate=%s rejected=%s "
        "http_errors=%s purged=%s",
        user_guid, to, sim_run_id, purge_source, status,
        result.get("verified"), result.get("accepted"),
        result.get("duplicate"), result.get("rejected"),
        result.get("http_errors"), result.get("purged"))

    return jsonify(result), status
