"""Dispatch validation — verifies PlanDefinition + Contract for the dispatch chain."""

import requests as http_requests
from flask import current_app
from app.models.fhir_models import PlanDefinition
from app.services.session_headers import outbound_session_headers


def handle_dispatch(plan_definition_guid, provider_org_guid):
    """Validate a dispatch request.

    1. Verify PlanDefinition exists
    2. Find matching contract from contract.pdhc
    3. Return contract + PlanDefinition info

    Returns:
        tuple: (result_dict, status_code)
    """
    # Look up by guid first, then by fhir_id
    pd = PlanDefinition.query.filter_by(guid=plan_definition_guid).first()
    if not pd:
        pd = PlanDefinition.query.filter_by(fhir_id=plan_definition_guid).first()
    if not pd:
        return {'error': 'PlanDefinition not found', 'guid': plan_definition_guid}, 404

    # #771: contract topics reference EITHER identifier in production — 7 of
    # the 10 live contracts use the `guid` and 3 use the `fhir_id`, for the same
    # PlanDefinition. This comment previously asserted only the second, and the
    # matcher was given only `fhir_id`, so dispatch could never find the other
    # seven. Pass both until the two identifiers are collapsed.
    plan_definition_refs = [pd.guid, pd.fhir_id]

    # Find matching contract via contract.pdhc
    contract_base = current_app.config['CONTRACT_BASE_URL'].rstrip('/')
    try:
        resp = http_requests.get(f"{contract_base}/fhir/Contract",
                                 headers=outbound_session_headers(), timeout=15)
        if resp.status_code != 200:
            return {'error': 'Contract service unavailable'}, 502

        entries = resp.json().get('entry', [])
        matching = _find_matching_contract(entries, plan_definition_refs,
                                           provider_org_guid)

        if not matching:
            return {
                'error': 'No active contract found',
                'detail': (
                    f'No active contract references '
                    f'PlanDefinition/{pd.guid} (or /{pd.fhir_id}) '
                    f'with provider Organization/{provider_org_guid}'
                ),
            }, 404

        return {
            'status': 'dispatched',
            'plan_definition_guid': pd.guid,
            'plan_definition_title': pd.title,
            'contract_guid': matching.get('id'),
            'contract_status': matching.get('status'),
            'provider_org_guid': provider_org_guid,
        }, 201

    except http_requests.RequestException as e:
        return {'error': f'Contract service unavailable: {str(e)}'}, 502


def _find_matching_contract(entries, plan_definition_refs, provider_org_guid):
    """Find an active contract that references the PlanDefinition and provider org.

    `plan_definition_refs` is every identifier this PlanDefinition answers to.
    #771: a PlanDefinition carries TWO independent GUIDs — `guid` and `fhir_id`,
    each from its own uuid4(), strictly 1:1 and never equal — and contracts in
    production reference BOTH. Measured 2026-10-07 across the 10 live contracts:

        7 topics reference the `guid`     (incl. 3 inert test artifacts)
        3 topics reference the `fhir_id`  (Medituner, CambioCaregiver, ff10d695)

    This function was passed only `fhir_id`, so the seven guid-referencing
    contracts could never match and dispatch answered "No active contract
    found" for every one of them.

    Accepting both is a bridge, not the destination: #771 collapses the two
    identifiers, and once every topic references one value this takes a single
    reference again. Accepting both FIRST means that convergence can rewrite
    contract topics without a window in which dispatch is broken.
    """
    wanted = {f'PlanDefinition/{r}' for r in plan_definition_refs if r}
    for entry in entries:
        c = entry.get('resource', entry)
        if c.get('status') not in ('executed', 'executable', 'offered', 'renewed'):
            continue

        # Check topic references this PlanDefinition, under either identifier
        topics = c.get('topic', [])
        topic_match = any(t.get('reference') in wanted for t in topics)
        if not topic_match:
            continue

        # Check provider org is in party references
        for party in c.get('party', []):
            for ref in party.get('reference', []):
                if ref.get('reference') == f'Organization/{provider_org_guid}':
                    return c

    return None
