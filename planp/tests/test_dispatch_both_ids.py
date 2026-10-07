"""#771 — a PlanDefinition answers to two identifiers, and contracts use both.

Measured across the 10 live contracts on 2026-10-07:

    7 topics reference the `guid`     (incl. 3 inert #755 test artifacts)
    3 topics reference the `fhir_id`  (Medituner, CambioCaregiver, ff10d695)

`handle_dispatch` passed only `fhir_id`, so dispatch answered "No active
contract found" for all seven — a live defect sitting underneath the identifier
question.
"""
from __future__ import annotations

from app.services.dispatch_service import _find_matching_contract

GUID = "febf8ec1-1c2a-454e-ad42-0b294dc59493"
FHIR = "b6f30058-8dfe-42ec-82d1-eda893ba5f1e"
ORG = "7a69ab02-dfce-43ae-ade7-fabf6b858d84"


def _contract(topic_ref, org=ORG, status="executed"):
    return {"resource": {
        "status": status,
        "topic": [{"reference": f"PlanDefinition/{topic_ref}"}],
        "party": [{"reference": [{"reference": f"Organization/{org}"}],
                   "role": [{"coding": [{"code": "provider"}]}]}]}}


def test_a_topic_referencing_the_GUID_matches():
    """The seven that could not match before."""
    assert _find_matching_contract([_contract(GUID)], [GUID, FHIR], ORG)


def test_a_topic_referencing_the_FHIR_ID_matches():
    """The three live provider contracts — Medituner and CambioCaregiver among
    them — must keep working."""
    assert _find_matching_contract([_contract(FHIR)], [GUID, FHIR], ORG)


def test_passing_only_one_identifier_misses_the_other():
    """The defect, stated as a test: this is what the old call site did."""
    assert _find_matching_contract([_contract(GUID)], [FHIR], ORG) is None


def test_an_unrelated_plandefinition_still_does_not_match():
    """Accepting two identifiers must not accept any identifier."""
    assert _find_matching_contract(
        [_contract("00000000-0000-0000-0000-000000000000")], [GUID, FHIR], ORG) is None


def test_the_provider_org_still_has_to_match():
    assert _find_matching_contract([_contract(GUID, org="someone-else")],
                                   [GUID, FHIR], ORG) is None


def test_an_inactive_contract_is_still_skipped():
    for bad in ("terminated", "cancelled", "draft"):
        assert _find_matching_contract([_contract(GUID, status=bad)],
                                       [GUID, FHIR], ORG) is None


def test_a_None_identifier_is_ignored_not_matched():
    """`PlanDefinition/None` must never match — the #755 shape, one entity over."""
    assert _find_matching_contract([_contract("None")], [GUID, None], ORG) is None
