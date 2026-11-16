"""#987 — a reviewed one-value correction of a clinical limit."""
from __future__ import annotations

import json

import pytest


@pytest.fixture
def plan(app, db_session):
    from app.models.activity_models import Activity, PlanDefinitionActivity, Transaction
    from app.models.fhir_models import PlanDefinition
    pd = PlanDefinition(name="bp", title="BP", status="active", version="1.0.0")
    act = Activity(title="measure")
    db_session.add_all([pd, act]); db_session.flush()
    dia = Transaction(activity_guid=act.guid, concept_guid="c-dia", range_min=80, range_max=120)
    sys_ = Transaction(activity_guid=act.guid, concept_guid="c-sys", range_min=100, range_max=160)
    db_session.add_all([dia, sys_, PlanDefinitionActivity(plandefinition_guid=pd.guid, activity_guid=act.guid, sort_order=0)])
    pd.action = json.dumps([{"id": act.guid, "transactions": [
        {"concept_guid": "c-dia", "range_min": 80, "range_max": 120},
        {"concept_guid": "c-sys", "range_min": 100, "range_max": 160}]}])
    db_session.commit()
    return pd, act, dia, sys_


def _set(pd, **kw):
    from app.services.plandef_range import set_range
    return set_range(pd.guid, kw.pop("concept", "c-dia"), kw.pop("lo", 60), kw.pop("hi", 90),
                     reviewer=kw.pop("reviewer", "Dr Test"), **kw)


def test_dry_run_reports_and_writes_nothing(plan):
    pd, _a, dia, _s = plan
    r = _set(pd)
    assert r["before"] == [(80.0, 120.0)] and r["after"] == (60, 90) and not r["applied"]
    assert (dia.range_min, dia.range_max, pd.version) == (80, 120, "1.0.0")


def test_apply_changes_all_three_copies_and_records_the_review(plan):
    pd, _a, dia, sys_ = plan
    _set(pd, apply=True)
    assert (dia.range_min, dia.range_max) == (60, 90)
    assert (sys_.range_min, sys_.range_max) == (100, 160), "only the named concept"
    tx = {t["concept_guid"]: t for t in json.loads(pd.action)[0]["transactions"]}
    assert (tx["c-dia"]["range_min"], tx["c-dia"]["range_max"]) == (60, 90)
    assert tx["c-sys"]["range_min"] == 100
    assert pd.version == "1.1.0" and pd.reviewer == "Dr Test" and pd.last_review_date
    assert pd.fhir_data


def test_the_order_snapshot_source_shows_the_new_range(plan, client):
    """request.pdhc snapshots _plandef_full_dict; that is what must change."""
    from app.api.plandefinitions import _plandef_full_dict
    pd, *_ = plan
    _set(pd, apply=True)
    txs = [t for a in _plandef_full_dict(pd)["activities"] for t in a["transactions"]]
    dia, = [t for t in txs if t["concept_guid"] == "c-dia"]
    assert (dia["range_min"], dia["range_max"]) == (60, 90)


@pytest.mark.parametrize("kw,why", [({"lo": 90, "hi": 60}, "min < max"), ({"lo": 60, "hi": 60}, "min < max"),
                                    ({"reviewer": " "}, "reviewer"), ({"concept": "nope"}, "no transaction")])
def test_refusals(plan, kw, why):
    from app.services.plandef_range import RangeChangeRefused
    pd, *_ = plan
    with pytest.raises(RangeChangeRefused, match=why):
        _set(pd, apply=True, **kw)


def test_a_SHARED_activity_is_refused(plan, db_session):
    from app.models.activity_models import PlanDefinitionActivity
    from app.models.fhir_models import PlanDefinition
    from app.services.plandef_range import RangeChangeRefused
    pd, act, dia, _ = plan
    other = PlanDefinition(name="other", title="Other", status="active")
    db_session.add(other); db_session.flush()
    db_session.add(PlanDefinitionActivity(plandefinition_guid=other.guid, activity_guid=act.guid, sort_order=0))
    db_session.commit()
    with pytest.raises(RangeChangeRefused, match="shared"):
        _set(pd, apply=True)
    assert dia.range_min == 80
