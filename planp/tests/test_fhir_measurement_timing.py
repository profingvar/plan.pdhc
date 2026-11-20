"""2026-11-20 — a measurement action's schedule reaches the FHIR export.

Only form and diagnosis-review actions got `timingTiming`. A measurement
action (MMD_plan's CGM: 4 per hour, 400 times, 40 d) was exported with
plan.pdhc's own field names only, so a FHIR reader saw no schedule.
"""
from __future__ import annotations

from app.services.fhir_service import FHIRService
from tests.test_diagnosis_review_984 import _export


def _cgm(**over):
    act = {"title": "CGM", "timing_type": "repeat", "timing_frequency": 4,
           "timing_period": 1, "timing_period_unit": "h",
           "timing_bounds_mode": "count", "timing_bounds_count": 400,
           "duration_value": 40, "duration_unit": "d",
           "transactions": [{"concept_guid": "22d0f6c6", "concept_name": "CGM"}]}
    act.update(over)
    return act


def test_a_measurement_action_carries_timingTiming(app):
    (act,) = _export([_cgm()], app)
    assert act["timingTiming"] == {"repeat": {
        "frequency": 4, "period": 1, "periodUnit": "h", "count": 400,
        "duration": 40, "durationUnit": "d"}}


def test_the_plan_pdhc_fields_stay_for_existing_readers(app):
    (act,) = _export([_cgm()], app)
    assert act["timing_frequency"] == 4 and act["transactions"][0]["concept_name"] == "CGM"


def test_bounds_duration_is_exported_as_boundsDuration(app):
    (act,) = _export([_cgm(timing_bounds_mode="duration", timing_bounds_count=None,
                           timing_bounds_duration_value=40,
                           timing_bounds_duration_unit="d",
                           duration_value=None, duration_unit=None)], app)
    assert act["timingTiming"]["repeat"]["boundsDuration"]["value"] == 40
    assert "count" not in act["timingTiming"]["repeat"]
    assert "duration" not in act["timingTiming"]["repeat"]


def test_once_is_count_one():
    t = FHIRService.measurement_timing({"timing_type": "once"})
    assert t == {"repeat": {"count": 1}}


def test_no_schedule_means_no_timingTiming(app):
    (act,) = _export([{"title": "x", "transactions": []}], app)
    assert "timingTiming" not in act


def test_a_unit_outside_UnitsOfTime_is_not_emitted_as_duration():
    t = FHIRService.measurement_timing(_cgm(duration_unit="days"))
    assert "duration" not in t["repeat"] and t["repeat"]["count"] == 400


def test_the_original_action_dict_is_not_mutated(app):
    a = _cgm()
    _export([a], app)
    assert "timingTiming" not in a
