"""Opt-in guided-authoring API — GA-3 (epic #516).

Three endpoints under ``/api/v1/authoring``:

  GET  /authoring/models    — allowlisted Claude models + whether a key is
                              configured, so the builder can render (or grey)
                              the model picker.
  POST /authoring/validate  — run the deterministic Layer-1 validators on a
                              draft concept or plandef; returns structured
                              issues. Works with no API key.
  POST /authoring/assist    — Claude-backed suggestion for a plain-language
                              intent (Layer 2), self-checked against Layer 1.

The whole surface is gated by ``AUTHORING_ASSISTANT_ENABLED`` (default off):
when the tool is disabled every endpoint returns ``{"enabled": false}`` and
nothing about existing concept/plandef saving is affected. All endpoints are
@requires_role('read_write') — the authoring role. Nothing here mutates data.
"""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from app.api.auth import requires_role
from app.services import plandef_assistant as assistant
from app.services import plandef_validation as validation

authoring_bp = Blueprint("authoring", __name__)


def _enabled() -> bool:
    return bool(current_app.config.get("AUTHORING_ASSISTANT_ENABLED", False))


def _termbank():
    return getattr(current_app, "termbank_client", None)


@authoring_bp.route("/authoring/models", methods=["GET"])
@requires_role("read_write")
def authoring_models():
    if not _enabled():
        return jsonify({"enabled": False, "reason": assistant.R_DISABLED}), 200
    return jsonify(assistant.models_info()), 200


@authoring_bp.route("/authoring/validate", methods=["POST"])
@requires_role("read_write")
def authoring_validate():
    if not _enabled():
        return jsonify({"enabled": False, "reason": assistant.R_DISABLED}), 200
    body = request.get_json(silent=True) or {}
    kind = (body.get("kind") or "concept").strip().lower()
    payload = body.get("payload") or {}
    if kind == "plandef":
        issues = validation.validate_plandef(payload)
    else:
        issues = validation.validate_concept(payload, termbank=_termbank())
    out = validation.summarise(issues)
    out["kind"] = kind
    return jsonify(out), 200


@authoring_bp.route("/authoring/assist", methods=["POST"])
@requires_role("read_write")
def authoring_assist():
    if not _enabled():
        return jsonify({"enabled": False, "reason": assistant.R_DISABLED}), 200
    body = request.get_json(silent=True) or {}
    intent = (body.get("intent") or "").strip()
    model = body.get("model")
    if not intent:
        return jsonify({"error": "intent is required"}), 400
    result = assistant.suggest_concept(intent, model, termbank=_termbank())
    return jsonify(result), 200
