"""M0 #421 — plan adopts the reform blob's session_phases with legacy fallback.

plan gates on the orthogonal 'planning' phase only (no org filter, no patient
data). Consistency adoption: prefer session_phases, fall back to
effective_phases during the migration window.
"""
from app.api.auth import _phases


def test_prefers_session_phases():
    assert _phases({'session_phases': ['planning'], 'effective_phases': []}) == ['planning']


def test_falls_back_to_effective_phases():
    assert _phases({'effective_phases': ['planning']}) == ['planning']


def test_empty_when_neither():
    assert _phases({}) == []


def test_planning_gate_equivalent():
    assert ('planning' in _phases({'session_phases': ['planning']})) is True
    assert ('planning' in _phases({'effective_phases': ['planning']})) is True
    assert ('planning' in _phases({'session_phases': ['analysis']})) is False
