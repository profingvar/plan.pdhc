from flask import Blueprint, request, jsonify
from app.models.fhir_models import PlanDefinition
from app.services.fhir_service import FHIRService
from app import db, limiter

fhir_plandef_bp = Blueprint('fhir_plandefinitions', __name__)
limiter.limit("200/minute")(fhir_plandef_bp)


@fhir_plandef_bp.route('/PlanDefinition', methods=['GET'])
def search_plan_definitions():
    """FHIR searchset Bundle for PlanDefinitions."""
    query = PlanDefinition.query

    status = request.args.get('status')
    if status:
        query = query.filter(PlanDefinition.status == status)

    title = request.args.get('title')
    if title:
        query = query.filter(PlanDefinition.title.ilike(f'%{title}%'))

    count = max(1, min(200, request.args.get('_count', 20, type=int)))
    offset = max(0, request.args.get('_offset', 0, type=int))

    total = query.count()
    items = query.order_by(PlanDefinition.date_created.desc()).offset(offset).limit(count).all()

    entries = []
    for pd in items:
        resource = pd.fhir_data or FHIRService.create_fhir_plandefinition(pd)
        # Ensure identifier and url are present
        if 'identifier' not in resource:
            resource['identifier'] = [{
                'system': 'https://pdhc.se/plan-definitions',
                'value': pd.name or pd.fhir_id,
            }]
        if 'url' not in resource:
            resource['url'] = f'https://pdhc.se/PlanDefinition/{pd.fhir_id}'

        entries.append({
            'fullUrl': f'https://pdhc.se/PlanDefinition/{pd.fhir_id}',
            'resource': resource,
        })

    bundle = {
        'resourceType': 'Bundle',
        'type': 'searchset',
        'total': total,
        'entry': entries,
    }
    return jsonify(bundle), 200


@fhir_plandef_bp.route('/PlanDefinition/<fhir_id>', methods=['GET'])
def read_plan_definition(fhir_id):
    pd = PlanDefinition.query.filter_by(fhir_id=fhir_id).first()
    if not pd:
        return jsonify({'error': 'Not found'}), 404

    resource = pd.fhir_data or FHIRService.create_fhir_plandefinition(pd)
    if 'identifier' not in resource:
        resource['identifier'] = [{
            'system': 'https://pdhc.se/plan-definitions',
            'value': pd.name or pd.fhir_id,
        }]
    if 'url' not in resource:
        resource['url'] = f'https://pdhc.se/PlanDefinition/{pd.fhir_id}'

    return jsonify(resource), 200


@fhir_plandef_bp.route('/PlanDefinition/<fhir_id>/$expand', methods=['GET'])
def expand_plan_definition(fhir_id):
    """Force regeneration of FHIR JSON for full expansion."""
    pd = PlanDefinition.query.filter_by(fhir_id=fhir_id).first()
    if not pd:
        return jsonify({'error': 'Not found'}), 404

    resource = FHIRService.create_fhir_plandefinition(pd)
    pd.fhir_data = resource
    db.session.commit()
    return jsonify(resource), 200


@fhir_plandef_bp.route('/PlanDefinition', methods=['POST'])
def create_plan_definition_fhir():
    """Not yet implemented — use the web builder."""
    return jsonify({
        'error': 'FHIR PlanDefinition creation via API is not yet supported. '
                 'Please use the web builder at /plandefinitions/builder.'
    }), 501
