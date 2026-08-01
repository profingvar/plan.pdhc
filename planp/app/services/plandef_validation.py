"""Deterministic PlanDefinition / Concept validation — Layer 1 (GA-1, epic #516).

This is the **floor** of the guided-authoring tool: a pure, deterministic set
of invariants that both the web route and the JSON API can call to tell a
non-expert author what is wrong with a draft, in plain language. It contains
**no LLM** and makes **no required network call** — the core path only reads
the plan.pdhc lookup tables. Terminology verification against termbank is an
*optional*, injected extra (pass a ``termbank`` client); without it the
terminology-existence check is simply skipped, keeping the core deterministic.

Why it exists: the authoring-surface audit found the data model permissive
(almost every clinically-meaningful column nullable), ``response_type`` is a
free-text lookup rather than an enum, terminology codes are never verified,
and the one real cross-field rule (choice ⇒ valueset) lives only in the web
route so the JSON API bypasses it. These validators encode the missing
invariants once, in a place both surfaces share.

Severity contract:
  * ``error``   — a real defect; blocks a *future* fail-closed save (GA-5).
  * ``warning`` — worth surfacing, never blocks.

Nothing here mutates or saves. See docs/plandef_authoring_assistant_design.md.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

from app.models.concept_models import (
    CanonicalLib, Concept, ResponseType, Unit, ValueCatalog, ValueSet,
)
from app.services.forms_service import RESPONSE_TYPE_MAP

ERROR = "error"
WARNING = "warning"

# forms_service.RESPONSE_TYPE_MAP is the base vocabulary. Production also has
# response-type lookup rows whose names that map doesn't cover ('numerical',
# 'Free text'); we recognise those here so a legitimate concept isn't wrongly
# flagged E-RESPONSE-TYPE-UNKNOWN. (forms_service has the same latent gap in
# form production — tracked as a separate follow-up; not touched here so the
# live form-production path is unchanged.)
_RESPONSE_TYPE_ALIASES = {
    "numerical": "numeric",
    "free text": "text",
}

# Only a true quantity (numeric) requires a unit. Sliders / integers are
# ordinal scales or counts and are commonly dimensionless, so requiring a unit
# there would be a false positive.
_UNIT_REQUIRED_KINDS = {"numeric"}
_CHOICE_KINDS = {"single_choice", "multiple_choice"}


@dataclass(frozen=True)
class Issue:
    """One validation finding. ``field`` is the draft key it concerns."""
    code: str
    severity: str
    message: str
    field: Optional[str] = None
    hint: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def _s(val: Any) -> str:
    return ("" if val is None else str(val)).strip()


def _resolve_response_kind(response_type_guid: Optional[str]):
    """Map a ``response_type`` guid → (name, internal_kind, recognised).

    ``recognised`` is False when the guid is missing, does not resolve to a
    lookup row, or resolves to a name the downstream map doesn't understand
    (a typo that would silently break form/FHIR production).
    """
    guid = _s(response_type_guid)
    if not guid:
        return (None, None, False)
    rt = ResponseType.query.filter_by(guid=guid).first()
    if rt is None:
        return (None, None, False)
    name = rt.response_type_name
    name_l = _s(name).lower()
    kind = RESPONSE_TYPE_MAP.get(name_l) or _RESPONSE_TYPE_ALIASES.get(name_l)
    return (name, kind, kind is not None)


# ---------------------------------------------------------------------------
# Concept-level validation
# ---------------------------------------------------------------------------
def validate_concept(
    payload: dict,
    *,
    termbank=None,
    verify_terminology: bool = True,
) -> list[Issue]:
    """Validate a draft Concept payload (the same shape the API accepts).

    Reads only lookup tables. If a ``termbank`` client is supplied *and*
    ``verify_terminology`` is True, the ``(canonical_lib, canonical_refnumber)``
    pair is additionally checked for existence (best-effort; a miss is a
    warning, never an error, because termbank may simply be unreachable).
    Never raises on a partial/empty draft.
    """
    issues: list[Issue] = []
    payload = payload or {}

    # -- range coherence (mirrors ck_concept_range, but friendlier + earlier) --
    lo, hi = payload.get("range_low"), payload.get("range_high")
    try:
        if lo is not None and hi is not None and float(lo) > float(hi):
            issues.append(Issue(
                "E-RANGE-INVERTED", ERROR,
                f"range_low ({lo}) is greater than range_high ({hi}).",
                field="range_low",
                hint="Swap the two values so the low bound is not above the high bound.",
            ))
    except (TypeError, ValueError):
        pass  # non-numeric range values are a separate concern; don't crash

    # -- response type --------------------------------------------------------
    name, kind, recognised = _resolve_response_kind(payload.get("response_type"))
    if not recognised:
        if not _s(payload.get("response_type")):
            issues.append(Issue(
                "E-RESPONSE-TYPE-UNKNOWN", ERROR,
                "No response type (value type) is set for this concept.",
                field="response_type",
                hint="Pick a response type, e.g. quantity, single choice, text, or boolean.",
            ))
        else:
            issues.append(Issue(
                "E-RESPONSE-TYPE-UNKNOWN", ERROR,
                f"Response type {name!r} is not one the platform recognises, so "
                "downstream form/FHIR production cannot map it.",
                field="response_type",
                hint="Use a recognised response type (quantity, single/multiple choice, "
                     "slider, text, boolean).",
            ))

    # -- unit required for quantities ----------------------------------------
    if kind in _UNIT_REQUIRED_KINDS and not _s(payload.get("unit")):
        issues.append(Issue(
            "E-UNIT-REQUIRED", ERROR,
            f"A {name or 'numeric'} concept must have a unit of measure.",
            field="unit",
            hint="Set a unit (e.g. mmHg, mmol/L, /min). A numeric value with no "
                 "unit is ambiguous to every downstream service.",
        ))
    # dangling unit reference
    unit_guid = _s(payload.get("unit"))
    if unit_guid and Unit.query.filter_by(guid=unit_guid).first() is None:
        issues.append(Issue(
            "E-DANGLING-REF", ERROR,
            "The selected unit does not exist.",
            field="unit",
            hint="Choose a unit from the units lookup.",
        ))

    # -- valueset required for choices ---------------------------------------
    if kind in _CHOICE_KINDS and not _s(payload.get("valueset")):
        issues.append(Issue(
            "E-VALUESET-REQUIRED", ERROR,
            f"A {name or 'choice'} concept must reference a value set (its answer options).",
            field="valueset",
            hint="Attach a value set so the concept can actually be answered and validated.",
        ))
    vs_guid = _s(payload.get("valueset"))
    if vs_guid and ValueSet.query.filter_by(guid=vs_guid).first() is None:
        issues.append(Issue(
            "E-DANGLING-REF", ERROR,
            "The selected value set does not exist.",
            field="valueset",
            hint="Choose a value set from the value-sets lookup.",
        ))

    # -- terminology binding --------------------------------------------------
    refnumber = _s(payload.get("canonical_refnumber"))
    if not refnumber:
        # WARNING, not error (#521 decision 2026-08-01): some legitimate concepts
        # — free-text info fields, PROMs like QOL, self-reported values — have no
        # standard LOINC/SNOMED code. Surface it, but don't block the save.
        issues.append(Issue(
            "W-TERM-MISSING", WARNING,
            "No terminology code (canonical_refnumber) is set — the concept is unbound.",
            field="canonical_refnumber",
            hint="Bind the concept to a code in its canonical library (e.g. a LOINC or "
                 "SNOMED code) where one exists. Use the termbank search to find it.",
        ))
    elif verify_terminology and termbank is not None:
        system = _terminology_system(payload.get("canonical_lib"))
        if system and termbank.lookup(system, refnumber) is None:
            issues.append(Issue(
                "W-TERM-UNVERIFIED", WARNING,
                f"Code {refnumber!r} could not be confirmed in {system!r} "
                "(it may be wrong, or termbank may be temporarily unavailable).",
                field="canonical_refnumber",
                hint="Double-check the code via termbank search.",
            ))

    return issues


def _terminology_system(canonical_lib_guid: Optional[str]) -> Optional[str]:
    """Resolve a canonical_lib guid to the system name termbank keys on."""
    guid = _s(canonical_lib_guid)
    if not guid:
        return None
    lib = CanonicalLib.query.filter_by(guid=guid).first()
    if lib is None:
        return None
    # termbank keys on the library's short name (e.g. "LOINC"); fall back to
    # whatever identifying attribute the row exposes.
    return (
        getattr(lib, "canonical_lib_name", None)
        or getattr(lib, "name", None)
        or None
    )


# ---------------------------------------------------------------------------
# PlanDefinition-level validation
# ---------------------------------------------------------------------------
def validate_plandef(payload: dict) -> list[Issue]:
    """Validate a draft PlanDefinition's structure and cross-references.

    Accepts a normalised dict::

        {
          "goals": [ {"concept_guid", "target_unit", "target_value_guid", ...} ],
          "activities": [ {"transactions": [ {"concept_guid", "unit", ...} ]} ],
          # or a flat "transactions": [...] for convenience
        }

    Checks emptiness, dangling concept / value references, and unit
    contradictions between a goal/transaction and its concept's own unit.
    Never raises on a partial draft.
    """
    issues: list[Issue] = []
    payload = payload or {}

    goals = payload.get("goals") or []
    activities = payload.get("activities") or []
    transactions = list(payload.get("transactions") or [])
    for act in activities:
        transactions.extend((act or {}).get("transactions") or [])

    if not goals and not transactions and not activities:
        issues.append(Issue(
            "W-EMPTY-PLANDEF", WARNING,
            "This plan has no goals and no activities yet.",
            field=None,
            hint="Add at least one goal or one activity before publishing.",
        ))

    # concept-name cache so we resolve each guid once
    _concept_cache: dict[str, Optional[Concept]] = {}

    def _concept(guid: str) -> Optional[Concept]:
        if guid not in _concept_cache:
            _concept_cache[guid] = Concept.query.filter_by(guid=guid).first()
        return _concept_cache[guid]

    def _check_concept_ref(guid: str, where: str):
        if guid and _concept(guid) is None:
            issues.append(Issue(
                "E-DANGLING-REF", ERROR,
                f"{where} references a concept that does not exist ({guid}).",
                field="concept_guid",
                hint="Pick an existing concept, or create it first.",
            ))

    def _check_unit_contradiction(free_unit: str, guid: str, where: str, field: str):
        c = _concept(guid) if guid else None
        if not free_unit or c is None or not c.unit:
            return
        u = Unit.query.filter_by(guid=c.unit).first()
        if u is not None and _s(u.unit_name).lower() != _s(free_unit).lower():
            issues.append(Issue(
                "W-UNIT-CONTRADICTS", WARNING,
                f"{where} uses unit {free_unit!r} but its concept's unit is "
                f"{u.unit_name!r}.",
                field=field,
                hint="Reconcile the units — a threshold in a different unit than the "
                     "concept will misfire in request.pdhc.",
            ))

    for i, g in enumerate(goals):
        g = g or {}
        cg = _s(g.get("concept_guid"))
        _check_concept_ref(cg, f"Goal #{i + 1}")
        _check_unit_contradiction(_s(g.get("target_unit")), cg,
                                  f"Goal #{i + 1}", "target_unit")
        tvg = _s(g.get("target_value_guid"))
        if tvg and ValueCatalog.query.filter_by(guid=tvg).first() is None:
            issues.append(Issue(
                "E-DANGLING-REF", ERROR,
                f"Goal #{i + 1} references a target value that does not exist ({tvg}).",
                field="target_value_guid",
                hint="Pick an existing value from the concept's value set.",
            ))

    for i, t in enumerate(transactions):
        t = t or {}
        cg = _s(t.get("concept_guid"))
        _check_concept_ref(cg, f"Measurement #{i + 1}")
        _check_unit_contradiction(_s(t.get("unit")), cg,
                                  f"Measurement #{i + 1}", "unit")

    return issues


def summarise(issues: list[Issue]) -> dict:
    """Compact envelope for API responses / self-checks."""
    errors = [i for i in issues if i.severity == ERROR]
    warnings = [i for i in issues if i.severity == WARNING]
    return {
        "ok": not errors,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "issues": [i.to_dict() for i in issues],
    }
