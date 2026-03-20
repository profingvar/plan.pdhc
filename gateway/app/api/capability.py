import os
from flask import Blueprint, jsonify, send_file, abort
from app import limiter

capability_bp = Blueprint('capability', __name__)
limiter.limit("200/minute")(capability_bp)

API_VERSION = '1.0.0'
BASE = '/api/v1'


def _endpoint(method, path, auth, description):
    return {
        'method': method,
        'path': f'{BASE}{path}',
        'auth_required': auth,
        'description': description,
    }


ENDPOINTS = [
    # Auth
    _endpoint('POST', '/auth/login', False, 'Authenticate and receive JWT tokens'),
    _endpoint('POST', '/auth/logout', True, 'Logout (client discards token)'),
    _endpoint('GET', '/auth/me', True, 'Get current authenticated user'),
    _endpoint('POST', '/auth/refresh', True, 'Refresh access token using refresh token'),

    # Canonical Libraries
    _endpoint('GET', '/canonical-libs', False, 'List all canonical libraries'),
    _endpoint('POST', '/canonical-libs', True, 'Create a canonical library'),
    _endpoint('GET', '/canonical-libs/<guid>', False, 'Read a canonical library'),
    _endpoint('PUT', '/canonical-libs/<guid>', True, 'Update a canonical library'),
    _endpoint('DELETE', '/canonical-libs/<guid>', True, 'Delete a canonical library'),

    # Concept Types
    _endpoint('GET', '/concept-types', False, 'List all concept types'),
    _endpoint('POST', '/concept-types', True, 'Create a concept type'),
    _endpoint('GET', '/concept-types/<guid>', False, 'Read a concept type'),
    _endpoint('PUT', '/concept-types/<guid>', True, 'Update a concept type'),
    _endpoint('DELETE', '/concept-types/<guid>', True, 'Delete a concept type'),

    # Response Types
    _endpoint('GET', '/response-types', False, 'List all response types'),
    _endpoint('POST', '/response-types', True, 'Create a response type'),
    _endpoint('GET', '/response-types/<guid>', False, 'Read a response type'),
    _endpoint('PUT', '/response-types/<guid>', True, 'Update a response type'),
    _endpoint('DELETE', '/response-types/<guid>', True, 'Delete a response type'),

    # Units
    _endpoint('GET', '/units', False, 'List all units'),
    _endpoint('POST', '/units', True, 'Create a unit'),
    _endpoint('GET', '/units/<guid>', False, 'Read a unit'),
    _endpoint('PUT', '/units/<guid>', True, 'Update a unit'),
    _endpoint('DELETE', '/units/<guid>', True, 'Delete a unit'),

    # PlanDef Types
    _endpoint('GET', '/plandef-types', False, 'List all PlanDefinition types'),
    _endpoint('POST', '/plandef-types', True, 'Create a PlanDefinition type'),
    _endpoint('GET', '/plandef-types/<guid>', False, 'Read a PlanDefinition type'),
    _endpoint('PUT', '/plandef-types/<guid>', True, 'Update a PlanDefinition type'),
    _endpoint('DELETE', '/plandef-types/<guid>', True, 'Delete a PlanDefinition type'),

    # Intended Uses
    _endpoint('GET', '/intended-uses', False, 'List all intended uses'),
    _endpoint('POST', '/intended-uses', True, 'Create an intended use'),
    _endpoint('GET', '/intended-uses/<guid>', False, 'Read an intended use'),
    _endpoint('PUT', '/intended-uses/<guid>', True, 'Update an intended use'),
    _endpoint('DELETE', '/intended-uses/<guid>', True, 'Delete an intended use'),

    # Values
    _endpoint('GET', '/values', False, 'List all values'),
    _endpoint('POST', '/values', True, 'Create a value'),
    _endpoint('GET', '/values/<guid>', False, 'Read a value'),
    _endpoint('PUT', '/values/<guid>', True, 'Update a value'),
    _endpoint('DELETE', '/values/<guid>', True, 'Delete a value'),

    # ValueSets
    _endpoint('GET', '/valuesets', False, 'List all valuesets (paginated)'),
    _endpoint('POST', '/valuesets', True, 'Create a valueset'),
    _endpoint('GET', '/valuesets/<guid>', False, 'Read a valueset'),
    _endpoint('PUT', '/valuesets/<guid>', True, 'Update a valueset'),
    _endpoint('DELETE', '/valuesets/<guid>', True, 'Delete a valueset'),

    # ValueSet Membership
    _endpoint('GET', '/valuesets/<guid>/values', False, 'List values in a valueset'),
    _endpoint('POST', '/valuesets/<guid>/values', True, 'Add a value to a valueset'),
    _endpoint('PUT', '/valuesets/<guid>/values/<value_guid>', True, 'Update sort order of a value in a valueset'),
    _endpoint('DELETE', '/valuesets/<guid>/values/<value_guid>', True, 'Remove a value from a valueset'),

    # Concepts
    _endpoint('GET', '/concepts', False, 'List/search concepts (paginated, filterable)'),
    _endpoint('POST', '/concepts', True, 'Create a concept'),
    _endpoint('GET', '/concepts/<guid>', False, 'Read a concept (includes valueset values)'),
    _endpoint('PUT', '/concepts/<guid>', True, 'Update a concept'),
    _endpoint('DELETE', '/concepts/<guid>', True, 'Delete a concept'),

    # Concept Values
    _endpoint('GET', '/concepts/<guid>/values', False, 'List values for a concept'),
    _endpoint('POST', '/concepts/<guid>/values', True, 'Add a value to a concept\'s valueset'),
    _endpoint('DELETE', '/concepts/<guid>/values/<value_guid>', True, 'Remove a value from a concept\'s valueset'),

    # PlanDefinitions (CRUD)
    _endpoint('GET', '/plandefinitions', False, 'List/search PlanDefinitions (paginated)'),
    _endpoint('POST', '/plandefinitions', True, 'Create a PlanDefinition with goals and activities'),
    _endpoint('GET', '/plandefinitions/<guid>', False, 'Read a PlanDefinition with full detail'),
    _endpoint('PUT', '/plandefinitions/<guid>', True, 'Update a PlanDefinition'),
    _endpoint('DELETE', '/plandefinitions/<guid>', True, 'Delete a PlanDefinition'),

    # FHIR PlanDefinition (read-only FHIR format)
    _endpoint('GET', '/PlanDefinition', False, 'FHIR R5 searchset Bundle'),
    _endpoint('GET', '/PlanDefinition/<fhir_id>', False, 'FHIR R5 PlanDefinition resource'),
    _endpoint('GET', '/PlanDefinition/<fhir_id>/$expand', False, 'Force regenerate FHIR JSON'),

    # Documentation
    _endpoint('GET', '/docs', False, 'List all available documentation files'),
    _endpoint('GET', '/docs/<filename>', False, 'Download a documentation file'),
]


@capability_bp.route('/capability-statement', methods=['GET'])
def capability_statement():
    resources = {}
    for ep in ENDPOINTS:
        # Group by resource (first path segment after /api/v1/)
        path = ep['path'].replace(BASE + '/', '')
        resource = path.split('/')[0]
        if resource not in resources:
            resources[resource] = []
        resources[resource].append(ep)

    return jsonify({
        'name': 'PDHC PlanDef Builder API',
        'version': API_VERSION,
        'status': 'active',
        'publisher': 'PDHC',
        'description': 'RESTful API for managing clinical concepts, values, valuesets, '
                       'and FHIR R5 PlanDefinitions.',
        'fhir_version': 'R5',
        'format': ['json'],
        'authentication': {
            'type': 'JWT Bearer',
            'login': f'{BASE}/auth/login',
            'refresh': f'{BASE}/auth/refresh',
            'note': 'Read endpoints are public. Write endpoints require JWT with read_write or admin role.',
        },
        'rate_limiting': {
            'default': '200 requests/minute per IP',
            'login': '10 requests/minute per IP',
            'headers': ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset'],
        },
        'roles': {
            'read_only': 'Can read all resources',
            'read_write': 'Can read and write all resources',
            'admin': 'Full access including user management',
        },
        'resources': resources,
        'total_endpoints': len(ENDPOINTS),
    }), 200


@capability_bp.route('/endpoints', methods=['GET'])
def list_endpoints():
    return jsonify({
        'total': len(ENDPOINTS),
        'endpoints': ENDPOINTS,
    }), 200


# --- Documentation API ---

DOCS_CATALOG = {
    'api_reference.md': 'Comprehensive REST API reference with examples',
    'db_schema_snapshot.md': 'Database schema — all 17 tables with samples and GUIDs',
    'plan_description.md': 'Domain architecture — concepts, values, valuesets, PlanDefinitions',
    'readme.md': 'Deployment plan — step-by-step setup and configuration',
    'progress.md': 'Progress log — completed and pending steps',
    'top_rules.md': 'Project rules (immutable)',
    'repo_css.md': 'Frontend design system — colours, typography, components',
    'pdhc_markdown_layout_standard.md': 'Markdown formatting standard',
    'changed_files.md': 'Registry of all created and edited files',
    'nginx_implement_server19March.md': 'Nginx reverse proxy deployment template',
}


def _resolve_doc_path(filename):
    # Search order: gateway/docs/ → project root → /project-docs/ (Docker mount)
    gateway_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    search_dirs = [
        os.path.join(gateway_dir, 'docs'),
        os.path.dirname(gateway_dir),
        '/project-docs',
    ]
    for d in search_dirs:
        path = os.path.join(d, filename)
        if os.path.isfile(path):
            return path
    return None


@capability_bp.route('/docs', methods=['GET'])
def list_docs():
    docs = []
    for filename, description in DOCS_CATALOG.items():
        path = _resolve_doc_path(filename)
        if path:
            docs.append({
                'filename': filename,
                'description': description,
                'download_url': f'{BASE}/docs/{filename}',
                'size_bytes': os.path.getsize(path),
            })
    return jsonify({'total': len(docs), 'documents': docs}), 200


@capability_bp.route('/docs/<filename>', methods=['GET'])
def download_doc(filename):
    if filename not in DOCS_CATALOG:
        return jsonify({'error': 'Document not found'}), 404
    path = _resolve_doc_path(filename)
    if not path:
        return jsonify({'error': 'Document not found'}), 404
    return send_file(path, as_attachment=True, download_name=filename)
