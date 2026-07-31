"""Claude-backed authoring assistant — Layer 2 (GA-2, epic #516).

Sits on top of the deterministic validator (:mod:`app.services.plandef_validation`).
Its job is the fuzzy, knowledge-heavy translation rules can't do: turn a
non-expert's clinical intent ("track morning peak flow") into a correct,
terminology-bound Concept draft — the right ``response_type`` + ``unit`` +
terminology code — and explain every choice in plain language. It then runs
the Layer-1 validators on its *own* proposal so it can never hand back
something the floor would reject without saying so.

Guarantees:
  * **Opt-in.** Governed by ``AUTHORING_ASSISTANT_ENABLED`` (default off).
  * **Selectable model.** The caller picks a model from the config allowlist;
    a non-allowlisted model is refused.
  * **Search-first.** Existing concepts + termbank are consulted before any
    new binding is proposed, so novices reuse rather than duplicate.
  * **Graceful degradation.** No API key, a network error, a malformed reply,
    or the feature being disabled ⇒ a validation-only result carrying an
    ``assistant_available: false`` reason. It never raises into the request.
  * **No PHI leaves the box.** Only the author's intent text and concept/
    terminology *metadata* are sent to the API — never patient data.

Uses the Anthropic Messages API over ``requests`` (already a dependency);
the key is read from config/env and never hardcoded.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

import requests
from flask import current_app

from app.models.concept_models import CanonicalLib, Concept, ResponseType, Unit
from app.services import plandef_validation as v

log = logging.getLogger(__name__)

ANTHROPIC_VERSION = "2023-06-01"

# Reasons surfaced when Layer 2 can't run (Layer 1 still does).
R_DISABLED = "assistant_disabled"
R_NO_KEY = "no_api_key"
R_BAD_MODEL = "model_not_allowed"
R_NETWORK = "assistant_unreachable"
R_MALFORMED = "assistant_malformed_reply"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------
def _cfg(key: str, default=None):
    return current_app.config.get(key, default)


def models_info() -> dict:
    """What the UI needs to render (or grey out) the model picker."""
    return {
        "enabled": bool(_cfg("AUTHORING_ASSISTANT_ENABLED", False)),
        "key_configured": bool(_cfg("ANTHROPIC_API_KEY", "")),
        "models": list(_cfg("AUTHORING_ASSISTANT_MODELS", []) or []),
        "default_model": _cfg("AUTHORING_ASSISTANT_DEFAULT_MODEL", ""),
    }


def _resolve_model(requested: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """Return (model, error_reason). Falls back to the default when unset."""
    allow = list(_cfg("AUTHORING_ASSISTANT_MODELS", []) or [])
    default = _cfg("AUTHORING_ASSISTANT_DEFAULT_MODEL", "")
    model = (requested or default or "").strip()
    if not model:
        return (None, R_BAD_MODEL)
    if model not in allow:
        return (None, R_BAD_MODEL)
    return (model, None)


# ---------------------------------------------------------------------------
# Search-first context
# ---------------------------------------------------------------------------
def _reuse_candidates(intent_text: str, termbank=None, limit: int = 5) -> list[dict]:
    """Existing concepts (and termbank hits) that might already cover the intent."""
    out: list[dict] = []
    words = [w for w in re.split(r"\W+", intent_text or "") if len(w) > 3][:6]
    if words:
        from sqlalchemy import or_
        like_clauses = []
        for w in words:
            like = f"%{w}%"
            like_clauses.extend([
                Concept.concept_name.ilike(like),
                Concept.concept_display_text.ilike(like),
            ])
        rows = (Concept.query.filter(or_(*like_clauses))
                .order_by(Concept.concept_name).limit(limit).all())
        for c in rows:
            out.append({
                "concept_guid": c.guid,
                "concept_name": c.concept_name,
                "canonical_refnumber": c.canonical_refnumber,
                "why": "name/description overlaps the intent — reuse if it matches.",
            })
    # Best-effort termbank suggestions (never fatal).
    if termbank is not None and (intent_text or "").strip():
        try:
            res = termbank.search(intent_text, limit=limit) or {}
            for r in (res.get("results") or [])[:limit]:
                out.append({
                    "termbank_hit": True,
                    "system": r.get("system"),
                    "code": r.get("code"),
                    "display": r.get("display"),
                    "why": "candidate terminology code from termbank.",
                })
        except Exception as e:  # pragma: no cover - defensive
            log.warning("termbank search failed during assist: %s", e)
    return out


# ---------------------------------------------------------------------------
# The Anthropic call
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = (
    "You are a clinical-data-modelling assistant for the PDHC platform. You help "
    "a NON-EXPERT author create ONE correct, terminology-bound data element "
    "(a 'Concept') for a care PlanDefinition. Given the author's plain-language "
    "intent, propose the correct value type and binding.\n\n"
    "Rules:\n"
    "- response_type MUST be one of: quantity, single choice, multiple choice, "
    "slider, text, boolean.\n"
    "- If response_type is quantity or slider, you MUST give a unit. Prefer a "
    "UCUM unit and also give the human display unit.\n"
    "- If response_type is single/multiple choice, describe the answer options "
    "(valueset_hint); do not invent a value-set id.\n"
    "- Always propose a real terminology code: canonical_lib (e.g. LOINC or "
    "SNOMED CT) and canonical_refnumber (the code). If you are unsure of the "
    "exact code, say so in the rationale and give your best candidate.\n"
    "- Never include patient data. Reason only about the data element.\n\n"
    "Respond with ONLY a JSON object, no prose, with keys: response_type, "
    "unit_ucum, unit_display, canonical_lib, canonical_refnumber, valueset_hint, "
    "range_low, range_high, rationale. Use null where not applicable."
)


def _call_claude(model: str, intent_text: str, context: list[dict]) -> dict:
    """POST to the Anthropic Messages API; return the parsed proposal dict.

    Raises ``_Unavailable(reason)`` on any failure so the caller degrades.
    """
    key = _cfg("ANTHROPIC_API_KEY", "")
    if not key:
        raise _Unavailable(R_NO_KEY)
    base = (_cfg("ANTHROPIC_API_BASE", "https://api.anthropic.com") or "").rstrip("/")
    user = (
        f"Author intent: {intent_text!r}\n\n"
        f"Existing concepts / terminology candidates already in the system "
        f"(prefer reuse if one matches):\n{json.dumps(context, ensure_ascii=False)}\n\n"
        "Propose the single best data element as the specified JSON."
    )
    body = {
        "model": model,
        "max_tokens": int(_cfg("AUTHORING_ASSISTANT_MAX_TOKENS", 1500)),
        "system": _SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user}],
    }
    try:
        resp = requests.post(
            f"{base}/v1/messages",
            headers={
                "x-api-key": key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            json=body,
            timeout=float(_cfg("AUTHORING_ASSISTANT_TIMEOUT_SECONDS", 30)),
        )
    except requests.RequestException as e:
        log.warning("assistant call failed: %s", e)
        raise _Unavailable(R_NETWORK)
    if resp.status_code != 200:
        log.warning("assistant call HTTP %s: %s", resp.status_code, resp.text[:200])
        raise _Unavailable(R_NETWORK)
    try:
        data = resp.json()
        text = "".join(
            block.get("text", "")
            for block in data.get("content", [])
            if block.get("type") == "text"
        )
        return _extract_json(text)
    except (ValueError, KeyError, TypeError) as e:
        log.warning("assistant reply parse error: %s", e)
        raise _Unavailable(R_MALFORMED)


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of the model's reply."""
    text = (text or "").strip()
    try:
        return json.loads(text)
    except ValueError:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise _Unavailable(R_MALFORMED)
    return json.loads(m.group(0))  # may raise ValueError -> caller degrades


class _Unavailable(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


# ---------------------------------------------------------------------------
# Proposal → validated draft
# ---------------------------------------------------------------------------
def _resolve_proposal_to_payload(proposal: dict) -> tuple[dict, list[str]]:
    """Map the model's *named* proposal to a guid-payload for Layer-1 checking.

    Returns (payload, notes). A named response_type / unit / canonical_lib that
    doesn't exist in the lookup tables is left blank (so the validator flags it)
    and recorded as a note the author can act on ("create this unit first").
    """
    notes: list[str] = []
    payload: dict[str, Any] = {
        "canonical_refnumber": (proposal.get("canonical_refnumber") or None),
        "range_low": proposal.get("range_low"),
        "range_high": proposal.get("range_high"),
    }

    rt_name = (proposal.get("response_type") or "").strip()
    if rt_name:
        rt = ResponseType.query.filter(
            ResponseType.response_type_name.ilike(rt_name)
        ).first()
        if rt:
            payload["response_type"] = rt.guid
        else:
            notes.append(f"Response type {rt_name!r} is not yet a lookup row — add it or pick an existing one.")

    unit_name = (proposal.get("unit_display") or proposal.get("unit_ucum") or "").strip()
    if unit_name:
        u = Unit.query.filter(Unit.unit_name.ilike(unit_name)).first()
        if u:
            payload["unit"] = u.guid
        else:
            notes.append(f"Unit {unit_name!r} is not yet a lookup row — add it before saving.")

    lib_name = (proposal.get("canonical_lib") or "").strip()
    if lib_name:
        lib = CanonicalLib.query.filter(
            CanonicalLib.canonical_lib_name.ilike(lib_name)
        ).first()
        if lib:
            payload["canonical_lib"] = lib.guid
        else:
            notes.append(f"Canonical library {lib_name!r} is not registered — register it or choose another.")

    return payload, notes


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def suggest_concept(
    intent_text: str,
    model: Optional[str] = None,
    *,
    termbank=None,
    verify_terminology: bool = True,
) -> dict:
    """Suggest a concept draft for a plain-language intent.

    Always returns a dict (never raises). When the Claude assistant can't run,
    ``assistant_available`` is False with a ``reason``, and the response still
    carries the search-first ``reuse_candidates`` so the author isn't stuck.
    """
    intent_text = (intent_text or "").strip()
    result: dict[str, Any] = {
        "intent": intent_text,
        "assistant_available": False,
        "reason": None,
        "model_used": None,
        "reuse_candidates": [],
        "proposal": None,
        "resolution_notes": [],
        "validation": v.summarise([]),
    }

    if not _cfg("AUTHORING_ASSISTANT_ENABLED", False):
        result["reason"] = R_DISABLED
        return result

    chosen, err = _resolve_model(model)
    if err:
        result["reason"] = err
        result["reuse_candidates"] = _reuse_candidates(intent_text, termbank)
        return result

    # search-first context (also returned to the author)
    candidates = _reuse_candidates(intent_text, termbank)
    result["reuse_candidates"] = candidates

    try:
        proposal = _call_claude(chosen, intent_text, candidates)
    except _Unavailable as u:
        result["reason"] = u.reason
        return result

    result["assistant_available"] = True
    result["model_used"] = chosen
    result["proposal"] = proposal

    # Self-check: resolve named proposal to guids, then run Layer 1 on it.
    payload, notes = _resolve_proposal_to_payload(proposal)
    result["resolution_notes"] = notes
    issues = v.validate_concept(
        payload, termbank=termbank, verify_terminology=verify_terminology
    )
    result["validation"] = v.summarise(issues)
    return result
