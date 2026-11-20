"""2026-11-20 — continuous activities (CGM): ordered once, run for a period,
stream data about every sample interval.

MMD_plan modelled CGM as "repeat 4/h, count 410, duration 40 d", which ended
after ~4.3 days and said each reading lasted 40 days. The operator: ordering
CGM is ONE procedure that produces glucose values as long as it is on; and a
period is REQUIRED.
"""
from __future__ import annotations

import json
import uuid

from app.services import continuous_timing as ct
from tests.conftest import SAMPLE_ACCESS_BLOB, set_sso_session
from tests.test_diagnosis_review_984 import _export


def _cgm(**over):
    act = {"title": "CGM", "timing_type": "continuous",
           "timing_bounds_duration_value": 40, "timing_bounds_duration_unit": "d",
           "sample_interval_value": 15, "sample_interval_unit": "min",
           "transactions": [{"concept_guid": "22d0f6c6", "concept_name": "B-glucos"}]}
    act.update(over)
    return act


def _codes(issues):
    return sorted(i["code"] for i in issues)


# --- validation ---------------------------------------------------------------

def test_a_complete_continuous_activity_is_accepted_and_normalised():
    act = _cgm(timing_frequency=4, timing_period=1, timing_period_unit="h",
               timing_bounds_mode="count", timing_bounds_count=410,
               duration_value=40, duration_unit="d")
    assert ct.validate_actions([act]) == []
    # the workaround's fields are cleared, so no reader sees 410 orders
    for k in ("timing_frequency", "timing_period", "timing_period_unit",
              "timing_bounds_count", "duration_value", "duration_unit"):
        assert act[k] is None, k
    assert act["timing_bounds_mode"] == "duration"
    assert (act["timing_bounds_duration_value"], act["timing_bounds_duration_unit"]) == (40, "d")


def test_the_period_is_required():
    assert _codes(ct.validate_actions([_cgm(timing_bounds_duration_value=None)])) == \
        ["continuous_period_required"]
    assert _codes(ct.validate_actions([_cgm(timing_bounds_duration_value=0)])) == \
        ["continuous_period_required"]
    assert _codes(ct.validate_actions([_cgm(timing_bounds_duration_unit="min")])) == \
        ["continuous_period_required"]


def test_the_sample_interval_is_required():
    assert _codes(ct.validate_actions([_cgm(sample_interval_value=None)])) == \
        ["continuous_interval_required"]
    assert _codes(ct.validate_actions([_cgm(sample_interval_unit="d")])) == \
        ["continuous_interval_required"]


def test_a_refused_activity_is_not_normalised():
    act = _cgm(timing_bounds_duration_value=None, timing_bounds_count=410)
    ct.validate_actions([act])
    assert act["timing_bounds_count"] == 410


def test_only_a_measurement_can_be_continuous():
    assert _codes(ct.validate_actions([_cgm(is_form=True)])) == ["continuous_not_measurement"]


def test_other_timings_are_untouched():
    act = {"title": "Sleep", "timing_type": "repeat", "timing_frequency": 1,
           "timing_period": 1, "timing_period_unit": "d", "timing_bounds_count": 8}
    before = dict(act)
    assert ct.validate_actions([act]) == [] and act == before


# --- FHIR export --------------------------------------------------------------

def test_export_is_one_occurrence_lasting_the_period(app):
    a = _cgm()
    ct.validate_actions([a])
    (act,) = _export([a], app)
    assert act["timingTiming"] == {"repeat": {"count": 1, "duration": 40, "durationUnit": "d"}}
    assert "frequency" not in json.dumps(act["timingTiming"])
    assert act["extension"] == [{
        "url": ct.SAMPLE_INTERVAL_EXT,
        "valueDuration": {"value": 15, "unit": "min",
                          "system": "http://unitsofmeasure.org", "code": "min"}}]


# --- API and editor -----------------------------------------------------------

def _api_create(client, actions):
    return client.post("/api/v1/plandefinitions", json={
        "title": f"ct-{uuid.uuid4().hex[:8]}", "status": "draft",
        "goals": [], "actions": actions})


def test_api_refuses_a_continuous_activity_without_a_period(client):
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    r = _api_create(client, [_cgm(timing_bounds_duration_value=None)])
    assert r.status_code == 422
    assert r.get_json()["error"] == "continuous_timing_invalid"


def test_editor_save_stores_the_interval_and_exports_it(client, app):
    from app.models.activity_models import Activity
    from app.models.fhir_models import PlanDefinition
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"ct-web-{uuid.uuid4().hex[:8]}"
    r = client.post("/plandefinitions/create", data={
        "title": title, "goal": "[]",
        "action": json.dumps([_cgm(timing_bounds_count=410, timing_frequency=4)])})
    assert r.status_code == 302 and "/builder" not in r.headers["Location"]
    with app.app_context():
        pd = PlanDefinition.query.filter_by(title=title).one()
        stored = json.loads(pd.action)[0]
        assert stored["timing_bounds_count"] is None and stored["timing_frequency"] is None
        fa = pd.fhir_data["action"][0]
        assert fa["timingTiming"]["repeat"] == {"count": 1, "duration": 40, "durationUnit": "d"}
        act = Activity.query.filter_by(title="CGM").order_by(Activity.id.desc()).first()
        assert (act.timing_type, act.sample_interval_value, act.sample_interval_unit) == \
            ("continuous", 15, "min")


def test_editor_refuses_a_continuous_activity_without_a_period(client, app):
    from app.models.fhir_models import PlanDefinition
    set_sso_session(client, SAMPLE_ACCESS_BLOB)
    title = f"ct-bad-{uuid.uuid4().hex[:8]}"
    r = client.post("/plandefinitions/create", data={
        "title": title, "goal": "[]",
        "action": json.dumps([_cgm(timing_bounds_duration_value=None)])}, follow_redirects=True)
    assert "active period" in r.get_data(as_text=True)
    with app.app_context():
        assert PlanDefinition.query.filter_by(title=title).count() == 0
