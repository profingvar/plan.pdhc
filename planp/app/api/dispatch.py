"""Dispatch endpoint — validates a PlanDefinition dispatch request.

Canonical route is `/PlanDefinition/<guid>/dispatch`. The
legacy `/CarePlan/<guid>/dispatch` alias existed pre-#310 when the
URL misnamed PlanDefinition as CarePlan (#318); it was dropped by
#334 after a 24h access-log soak (2026-06-30 → 2026-07-01) showed
zero callers.
"""

import bleach
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.dispatch_service import handle_dispatch

dispatch_bp = Blueprint('dispatch_api', __name__)
# Rate limiting via global RATELIMIT_DEFAULT in app/__init__.py.


def _dispatch(guid):
    guid = bleach.clean(guid)
    payload = request.get_json(silent=True) or {}

    provider_guid = payload.get('provider_guid')
    if not provider_guid:
        return jsonify({'error': 'provider_guid is required'}), 400

    result, status = handle_dispatch(guid, provider_guid)
    return jsonify(result), status


@dispatch_bp.route('/PlanDefinition/<guid>/dispatch', methods=['POST'])
def dispatch_plan_definition(guid):
    """Validate a PlanDefinition dispatch: checks PlanDefinition exists
    and contract is active."""
    return _dispatch(guid)
