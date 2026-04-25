"""Dispatch endpoint — handles CarePlan dispatch requests from request.pdhc."""

import bleach
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.dispatch_service import handle_dispatch

dispatch_bp = Blueprint('dispatch_api', __name__)
limiter.limit("200/minute")(dispatch_bp)


@dispatch_bp.route('/CarePlan/<guid>/dispatch', methods=['POST'])
def dispatch_careplan(guid):
    """Validate a CarePlan dispatch: checks PlanDefinition exists and contract is active."""
    guid = bleach.clean(guid)
    payload = request.get_json(silent=True) or {}

    provider_guid = payload.get('provider_guid')
    if not provider_guid:
        return jsonify({'error': 'provider_guid is required'}), 400

    result, status = handle_dispatch(guid, provider_guid)
    return jsonify(result), status
