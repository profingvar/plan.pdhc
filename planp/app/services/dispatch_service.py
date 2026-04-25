"""Dispatch validation — verifies PlanDefinition + Contract for the dispatch chain."""

import requests as http_requests
from flask import current_app
from app.models.fhir_models import PlanDefinition


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

    # Contract topics reference the fhir_id, not the database guid
    fhir_id = pd.fhir_id

    # Find matching contract via contract.pdhc
    contract_base = current_app.config['CONTRACT_BASE_URL'].rstrip('/')
    try:
        resp = http_requests.get(f"{contract_base}/fhir/Contract", timeout=15)
        if resp.status_code != 200:
            return {'error': 'Contract service unavailable'}, 502

        entries = resp.json().get('entry', [])
        matching = _find_matching_contract(entries, fhir_id, provider_org_guid)

        if not matching:
            return {
                'error': 'No active contract found',
                'detail': (
                    f'No active contract references '
                    f'PlanDefinition/{fhir_id} '
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


def _find_matching_contract(entries, plan_definition_guid, provider_org_guid):
    """Find an active contract that references the PlanDefinition and provider org."""
    for entry in entries:
        c = entry.get('resource', entry)
        if c.get('status') not in ('executed', 'executable', 'offered', 'renewed'):
            continue

        # Check topic references this PlanDefinition
        topics = c.get('topic', [])
        topic_match = any(
            t.get('reference') == f'PlanDefinition/{plan_definition_guid}'
            for t in topics
        )
        if not topic_match:
            continue

        # Check provider org is in party references
        for party in c.get('party', []):
            for ref in party.get('reference', []):
                if ref.get('reference') == f'Organization/{provider_org_guid}':
                    return c

    return None
