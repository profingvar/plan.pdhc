"""Pin response_type -> question_type -> FHIR item resolution for the
production vocabulary (audit #526, 2026-08-06).

The two names that motivated the audit — 'numerical' and 'Free text' —
must resolve to numeric/decimal and text/string respectively. They were
already correct via forms_service._map_response_type's substring fallback;
these tests lock that in so a future refactor of the fallback can't
silently regress the mapping for the explicit prod names.
"""
from __future__ import annotations

import pytest

from app.services.forms_service import (
    _map_response_type,
    RESPONSE_TYPE_MAP,
    FHIR_TYPE_MAP,
)


@pytest.mark.parametrize(
    "name, expected_qtype, expected_fhir",
    [
        ("Free text", "text", "string"),
        ("free text", "text", "string"),
        ("numerical", "numeric", "decimal"),
        ("numeric", "numeric", "decimal"),
        ("Single choice", "single_choice", "choice"),
        ("multiple choice", "multiple_choice", "choice"),
        ("Slider", "slider", "integer"),
        ("Integer", "slider", "integer"),
        ("boolean", "boolean", "boolean"),
    ],
)
def test_response_type_resolution(name, expected_qtype, expected_fhir):
    qtype = _map_response_type(name)
    assert qtype == expected_qtype, f"{name!r} -> {qtype!r}, expected {expected_qtype!r}"
    assert FHIR_TYPE_MAP.get(qtype) == expected_fhir


def test_prod_names_are_explicit_in_map():
    """The two audited prod names are now first-class map entries, not
    only heuristic-fallback survivors — single source of truth for both
    forms_service and plandef_validation."""
    assert RESPONSE_TYPE_MAP.get("numerical") == "numeric"
    assert RESPONSE_TYPE_MAP.get("free text") == "text"


def test_free_text_is_never_numeric():
    """Regression guard for the audit concern: a free-text concept must
    never be produced as a numeric/decimal item."""
    assert _map_response_type("Free text") != "numeric"
    assert FHIR_TYPE_MAP.get(_map_response_type("Free text")) == "string"
