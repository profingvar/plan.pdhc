"""Dispatch endpoint — validates a PlanDefinition dispatch request.

The canonical route is `/PlanDefinition/<guid>/dispatch`. The
legacy `/CarePlan/<guid>/dispatch` alias is kept for one release
cycle because pre-#310 the platform used "CarePlan" as a URL-level
misnomer for PlanDefinition (#318). Both routes call the same
handler. Callers should switch to the canonical name.
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


@dispatch_bp.route('/CarePlan/<guid>/dispatch', methods=['POST'])
def dispatch_careplan_legacy(guid):
    """DEPRECATED legacy alias of /PlanDefinition/<guid>/dispatch
    kept for one release cycle (#318). Drop after no caller uses it.
    """
    return _dispatch(guid)
