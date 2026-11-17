"""Diagnosis-review PlanDefinition step (#984, contract section 1).

A PlanDefinition action stored as::

    {"is_diagnosis_review": true, "title": ..., "description": ...,
     "code_scope": ["5A1"], "timing_type": ..., ...same timing fields as forms}

opens an icd11.pdhc diagnosis session for a clinician. ``code_scope`` lists the
ICD-11 MMS stem-code prefixes the session may change. This module owns the
validation (refuse by name, never drop) and the FHIR ``PlanDefinition.action``
shape. The contract lives in ``~/T7_sidewinder/plans/984_diagnosis_review_contract.md``.
"""
from __future__ import annotations

import re

from app.models.concept_models import fhir_canonical_url

ACTIVITY_DEFINITION_CANONICAL = (
    "https://icd11.pdhc.se/fhir/ActivityDefinition/diagnosis-review"
)
# The contract's extension URL, built by the ADR D3 helper (the lint in
# tests/test_fhir_helpers.py forbids hardcoding plan's /fhir/ scheme).
CODE_SCOPE_EXTENSION_URL = fhir_canonical_url("StructureDefinition", "diagnosis-code-scope")
ACTION_TYPE_SYSTEM = "http://terminology.hl7.org/CodeSystem/action-type"

# Contract grammar: a stem code or a prefix of one. No '&', '/', wildcards.
STEM_PREFIX_RE = re.compile(r"^[0-9A-HJ-NP-Z][A-HJ-NP-Z0-9]{0,3}(\.[A-Z0-9]{1,2})?$")

# The step is performed by a clinician, never the patient.
_ALLOWED_PERFORMERS = (None, "", "Practitioner")


def is_diagnosis_review(act) -> bool:
    return isinstance(act, dict) and act.get("is_diagnosis_review") is True


def code_scope_prefix_error(prefix) -> str | None:
    """Return why ``prefix`` is not a valid scope prefix, or None if it is."""
    if not isinstance(prefix, str):
        return f"{prefix!r} is not a string"
    if prefix.startswith("X"):
        # The grammar's first character class admits X; the contract excludes
        # extension codes (chapter X) explicitly.
        return f"'{prefix}' is an ICD-11 extension code (X...), not a stem code"
    if not STEM_PREFIX_RE.match(prefix):
        return (f"'{prefix}' is not an ICD-11 MMS stem-code prefix "
                "(no '&', '/', wildcards, spaces or lower case)")
    return None


def validate_actions(actions) -> list[dict]:
    """Validate every diagnosis-review action in ``actions``.

    Returns a list of issues ``{"code", "message", "action_index"}``; an empty
    list means the actions may be saved. Non-review actions are only checked
    for a stray ``code_scope`` (which would otherwise be silently ignored).
    """
    issues: list[dict] = []
    if not isinstance(actions, list):
        return issues

    def refuse(idx, code, message):
        issues.append({"code": code, "message": message, "action_index": idx})

    for idx, act in enumerate(actions):
        if not isinstance(act, dict):
            continue
        label = f"action {idx + 1} ('{act.get('title') or ''}')"
        flag = act.get("is_diagnosis_review")
        if flag is not None and not isinstance(flag, bool):
            refuse(idx, "E-DIAGREVIEW-FLAG",
                   f"{label}: is_diagnosis_review must be true or false, got {flag!r}")
            continue
        if not flag:
            if "code_scope" in act:
                refuse(idx, "E-DIAGREVIEW-SCOPE-WITHOUT-REVIEW",
                       f"{label}: code_scope is only allowed on a diagnosis-review action")
            continue

        if act.get("is_form") or act.get("form_guid"):
            refuse(idx, "E-DIAGREVIEW-IS-FORM",
                   f"{label}: a diagnosis-review action cannot also be a form")
        if act.get("performer_type") not in _ALLOWED_PERFORMERS:
            refuse(idx, "E-DIAGREVIEW-PERFORMER",
                   f"{label}: a diagnosis review is performed by a clinician, "
                   f"not '{act.get('performer_type')}'")
        if act.get("transactions"):
            refuse(idx, "E-DIAGREVIEW-TRANSACTIONS",
                   f"{label}: a diagnosis-review action carries no transactions")

        scope = act.get("code_scope")
        if not isinstance(scope, list):
            refuse(idx, "E-DIAGREVIEW-SCOPE-MISSING",
                   f"{label}: code_scope is required (a list of ICD-11 stem-code prefixes)")
            continue
        if not scope:
            refuse(idx, "E-DIAGREVIEW-SCOPE-EMPTY",
                   f"{label}: code_scope must name at least one ICD-11 stem-code prefix")
            continue
        for prefix in scope:
            why = code_scope_prefix_error(prefix)
            if why:
                refuse(idx, "E-DIAGREVIEW-SCOPE-INVALID", f"{label}: code_scope {why}")
        dupes = sorted({p for p in scope if isinstance(p, str) and scope.count(p) > 1})
        if dupes:
            refuse(idx, "E-DIAGREVIEW-SCOPE-DUPLICATE",
                   f"{label}: code_scope names {', '.join(dupes)} more than once")
    return issues


def issue_messages(issues) -> list[str]:
    return [f"{i['code']}: {i['message']}" for i in issues]


def to_fhir_action(act, timing_timing=None) -> dict:
    """Build the contract's FHIR ``PlanDefinition.action`` for a review step.

    ``timing_timing`` is the already-built ``timingTiming`` (same builder as
    form actions) or None.
    """
    fhir_act = {"title": act.get("title", "")}
    if act.get("description"):
        fhir_act["description"] = act["description"]
    fhir_act["type"] = {"coding": [{
        "system": ACTION_TYPE_SYSTEM, "code": "update", "display": "Update",
    }]}
    fhir_act["definitionCanonical"] = ACTIVITY_DEFINITION_CANONICAL
    fhir_act["participant"] = [{"type": "practitioner"}]
    fhir_act["extension"] = [
        {"url": CODE_SCOPE_EXTENSION_URL, "valueString": prefix}
        for prefix in (act.get("code_scope") or [])
    ]
    if timing_timing:
        fhir_act["timingTiming"] = timing_timing
    return fhir_act
