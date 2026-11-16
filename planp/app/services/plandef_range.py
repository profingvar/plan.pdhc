"""Change one transaction's reference range in a PlanDefinition (#987).

The range lives in three places, and all three must agree:
  * the `transactions` row -- AUTHORITATIVE; request.pdhc's order snapshot is
    built from it (`_plandef_full_dict`);
  * the PlanDefinition's stored `action` JSON (the builder's copy);
  * `fhir_data`, regenerated from the above.
A PUT on /plandefinitions rebuilds every activity, which is far too blunt for
a reviewed one-value clinical correction; this changes exactly the range and
records the review on the PlanDefinition (reviewer, last_review_date, minor
version bump). It refuses an activity SHARED with another PlanDefinition,
because the change would silently alter that plan too.

Issued orders are NOT touched: their snapshot is frozen by design.
"""
from __future__ import annotations

import json
import logging
from datetime import date

from app import db

log = logging.getLogger("plan.clinical_change")


class RangeChangeRefused(ValueError):
    pass


def _bump_minor(v: str | None) -> str:
    parts = (v or "1.0.0").split(".")
    try:
        major, minor = int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
    except ValueError:
        raise RangeChangeRefused(f"version {v!r} is not semantic; set it by hand first")
    return f"{major}.{minor + 1}.0"


def set_range(pd_guid, concept_guid, lo, hi, *, reviewer, apply=False):
    from app.models.activity_models import PlanDefinitionActivity, Transaction
    from app.models.fhir_models import PlanDefinition
    from app.services.fhir_service import FHIRService

    if lo is None or hi is None or not lo < hi:
        raise RangeChangeRefused(f"range must satisfy min < max, got {lo}..{hi}")
    if not (reviewer or "").strip():
        raise RangeChangeRefused("a reviewer is required for a clinical limit change")
    pd = PlanDefinition.query.filter_by(guid=pd_guid).first()
    if pd is None:
        raise RangeChangeRefused(f"no PlanDefinition {pd_guid}")
    act_guids = [l.activity_guid for l in PlanDefinitionActivity.query.filter_by(plandefinition_guid=pd_guid)]
    txns = (Transaction.query.filter(Transaction.activity_guid.in_(act_guids))
            .filter_by(concept_guid=concept_guid).all()) if act_guids else []
    if not txns:
        raise RangeChangeRefused(f"concept {concept_guid} has no transaction in {pd_guid}")
    for t in txns:
        others = {l.plandefinition_guid for l in PlanDefinitionActivity.query.filter_by(activity_guid=t.activity_guid)} - {pd_guid}
        if others:
            raise RangeChangeRefused(f"activity {t.activity_guid} is shared with {sorted(others)}")

    before = sorted({(t.range_min, t.range_max) for t in txns})
    actions = json.loads(pd.action) if pd.action else []
    json_hits = 0
    for a in actions if isinstance(actions, list) else []:
        for tx in (a.get("transactions") or []) if isinstance(a, dict) else []:
            if isinstance(tx, dict) and tx.get("concept_guid") == concept_guid:
                tx["range_min"], tx["range_max"] = lo, hi
                json_hits += 1
    report = {"plandef": pd.name, "concept_guid": concept_guid, "before": before, "after": (lo, hi),
              "transactions": len(txns), "action_json_entries": json_hits,
              "version": f"{pd.version} -> {_bump_minor(pd.version)}", "applied": False}
    if not apply:
        return report
    for t in txns:
        t.range_min, t.range_max = lo, hi
    pd.action = json.dumps(actions)
    pd.version = _bump_minor(pd.version)
    pd.reviewer = reviewer.strip()
    pd.last_review_date = date.today()
    pd.fhir_data = FHIRService.create_fhir_plandefinition(pd)
    db.session.commit()
    log.warning("clinical limit changed: plandef=%s concept=%s %s -> %s..%s reviewer=%s version=%s",
                pd.guid, concept_guid, before, lo, hi, pd.reviewer, pd.version)
    report["applied"] = True
    return report
