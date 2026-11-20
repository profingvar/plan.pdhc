"""Continuous activities: ordered once, run for a period, stream data (2026-11-20).

A CGM is not 410 separate measurements. It is ONE procedure (the sensor) that,
while it is on, produces a stream of glucose values. Before this, the only
timings were `once` and `repeat`, so MMD_plan modelled CGM as "repeat 4/h,
count 410, duration 40 d": the count ended it after ~4.3 days and the duration
said each single reading lasted 40 days.

`timing_type = 'continuous'` says what is meant:

  * the activity is ordered once;
  * it runs for an active period, which is REQUIRED (operator 2026-11-20: a
    sensor has a known lifetime, and an open-ended order leaves nothing to
    measure coverage against). Stored as the duration bound
    (`timing_bounds_mode='duration'` + value/unit), the same fields a bounded
    repeat uses;
  * while it runs, data is expected about every `sample_interval` (e.g. 15
    min). That is an expectation about the stream, not an order.

Frequency, cycle, count and per-occurrence duration mean nothing here and are
cleared, so no reader can mistake the plan for thousands of orders.

FHIR: one occurrence lasting the active period, which is exactly what
`Timing.repeat {count: 1, duration, durationUnit}` means, plus the expected
sampling interval as an extension.
"""
from __future__ import annotations

from app.models.concept_models import fhir_canonical_url

CONTINUOUS = 'continuous'
PERIOD_UNITS = ('d', 'wk', 'mo')
INTERVAL_UNITS = ('s', 'min', 'h')
SAMPLE_INTERVAL_EXT = fhir_canonical_url('StructureDefinition', 'expected-sampling-interval')
UCUM = 'http://unitsofmeasure.org'

_CLEARED = ('timing_frequency', 'timing_period', 'timing_period_unit',
            'timing_bounds_count', 'duration_value', 'duration_unit')


def _positive(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f > 0 else None


def _num(f):
    return int(f) if float(f).is_integer() else f


def is_continuous(act) -> bool:
    return isinstance(act, dict) and act.get('timing_type') == CONTINUOUS


def validate_actions(actions) -> list[dict]:
    """Check every continuous action and normalise it IN PLACE.

    Returns issues `{"code", "message", "action_index"}` (same shape as
    diagnosis_review.validate_actions); empty means the actions may be saved.
    """
    issues: list[dict] = []
    if not isinstance(actions, list):
        return issues

    def refuse(idx, code, message):
        issues.append({"code": code, "message": message, "action_index": idx})

    for idx, act in enumerate(actions):
        if not is_continuous(act):
            continue
        title = act.get('title') or f'activity {idx + 1}'
        if act.get('is_form') or act.get('is_diagnosis_review'):
            refuse(idx, 'continuous_not_measurement',
                   f'"{title}": only a measurement activity can be continuous')
            continue
        period = _positive(act.get('timing_bounds_duration_value'))
        period_unit = act.get('timing_bounds_duration_unit')
        if period is None or period_unit not in PERIOD_UNITS:
            refuse(idx, 'continuous_period_required',
                   f'"{title}": a continuous activity needs an active period '
                   f'(days, weeks or months)')
        interval = _positive(act.get('sample_interval_value'))
        interval_unit = act.get('sample_interval_unit')
        if interval is None or interval_unit not in INTERVAL_UNITS:
            refuse(idx, 'continuous_interval_required',
                   f'"{title}": a continuous activity needs the expected '
                   f'interval between values (seconds, minutes or hours)')
        if period is None or interval is None or period_unit not in PERIOD_UNITS \
                or interval_unit not in INTERVAL_UNITS:
            continue
        act['timing_bounds_mode'] = 'duration'
        act['timing_bounds_duration_value'] = _num(period)
        act['sample_interval_value'] = _num(interval)
        for k in _CLEARED:
            act[k] = None
    return issues


def issue_messages(issues) -> list[str]:
    return [i['message'] for i in issues]


def fhir_timing(act) -> dict | None:
    """`timingTiming` for a continuous action: one occurrence lasting the
    active period."""
    period = _positive(act.get('timing_bounds_duration_value'))
    unit = act.get('timing_bounds_duration_unit')
    if period is None or unit not in PERIOD_UNITS:
        return None
    return {'repeat': {'count': 1, 'duration': _num(period), 'durationUnit': unit}}


def fhir_extension(act) -> dict | None:
    interval = _positive(act.get('sample_interval_value'))
    unit = act.get('sample_interval_unit')
    if interval is None or unit not in INTERVAL_UNITS:
        return None
    return {'url': SAMPLE_INTERVAL_EXT,
            'valueDuration': {'value': _num(interval), 'unit': unit,
                              'system': UCUM, 'code': unit}}
