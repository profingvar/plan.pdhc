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

    # Forms (FHIR Questionnaires)
    _endpoint('GET', '/forms', 'API key or SSO', 'List form catalogue (paginated)'),
    _endpoint('GET', '/forms/<form_guid>', 'API key or SSO', 'Get form definition (latest or specific version)'),
    _endpoint('GET', '/forms/<form_guid>/versions', 'API key or SSO', 'Get version history for a form'),
    _endpoint('POST', '/forms/produce', True, 'Produce a FHIR Questionnaire from concepts or PlanDefinition'),
    _endpoint('POST', '/forms/<form_guid>/publish', True, 'Publish a form version (draft → active)'),
    _endpoint('GET', '/forms/<form_guid>/immutability', True, 'Check latest version immutability status'),

    # Form Definitions
    _endpoint('GET', '/form-definitions', True, 'List form definitions (paginated, filterable)'),
    _endpoint('POST', '/form-definitions', True, 'Create a form definition'),
    _endpoint('GET', '/form-definitions/<guid>', True, 'Get form definition with resolved items'),
    _endpoint('PUT', '/form-definitions/<guid>', True, 'Update form definition metadata'),
    _endpoint('DELETE', '/form-definitions/<guid>', True, 'Delete a draft form definition'),
    _endpoint('GET', '/form-definitions/<guid>/items', True, 'List items in a form definition'),
    _endpoint('POST', '/form-definitions/<guid>/items', True, 'Add a concept to a form definition'),
    _endpoint('PUT', '/form-definitions/<guid>/items/<item_guid>', True, 'Update item settings'),
    _endpoint('DELETE', '/form-definitions/<guid>/items/<item_guid>', True, 'Remove item from definition'),
    _endpoint('POST', '/form-definitions/<guid>/reorder', True, 'Bulk reorder items'),
    _endpoint('POST', '/form-definitions/<guid>/produce', True, 'Produce FHIR Questionnaire from definition'),
    _endpoint('GET', '/form-definitions/<guid>/preview', True, 'Preview resolved form without persisting'),
    _endpoint('GET', '/form-definitions/<guid>/questionnaire', 'API key or SSO', 'Get produced FHIR Questionnaire JSON'),
    _endpoint('GET', '/form-definitions/<guid>/render-ready', 'API key or SSO', 'Get render-ready JSON for frontend integration'),

    # Documentation
    _endpoint('GET', '/docs', False, 'List all available documentation files'),
    _endpoint('GET', '/docs/<filename>', False, 'Download a documentation file'),

    # FHIR Capability
    _endpoint('GET', '/metadata', False, 'FHIR R5 CapabilityStatement resource'),
]


@capability_bp.route('/capability-statement', methods=['GET'])
def capability_statement():
    resources = {}
    for ep in ENDPOINTS:
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
            'type': 'SSO (sso.pdhc.se)',
            'login': f'{BASE}/auth/login',
            'callback': f'{BASE}/auth/callback',
            'note': 'Authentication delegated to sso.pdhc.se via SSO handshake. '
                    'Read endpoints are public. Write endpoints require "planning" phase access.',
        },
        'rate_limiting': {
            'default': '200 requests/minute per IP',
            'login': '10 requests/minute per IP',
            'headers': ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset'],
        },
        'roles': {
            'read_only': 'Any authenticated SSO user — can read all resources',
            'read_write': 'Professional with "planning" phase — can read and write all resources',
            'admin': 'SSO SU admin — full access',
        },
        'resources': resources,
        'total_endpoints': len(ENDPOINTS),
    }), 200


@capability_bp.route('/metadata', methods=['GET'])
def fhir_capability_statement():
    """FHIR R5-conformant CapabilityStatement resource."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    return jsonify({
        'resourceType': 'CapabilityStatement',
        'id': 'pdhc-plandef-builder',
        'url': 'https://plan.pdhc.se/api/v1/metadata',
        'version': API_VERSION,
        'name': 'PDHCPlanDefBuilderCapabilityStatement',
        'title': 'PDHC PlanDef Builder — FHIR Capability Statement',
        'status': 'active',
        'experimental': False,
        'date': now,
        'publisher': 'PDHC',
        'contact': [{
            'name': 'PDHC Development',
        }],
        'description': (
            'FHIR R5 capability statement for the PDHC PlanDefinition Builder. '
            'This server manages clinical concepts, values, valuesets, and '
            'FHIR R5 PlanDefinition resources for care plan authoring.'
        ),
        'kind': 'instance',
        'software': {
            'name': 'PDHC PlanDef Builder',
            'version': API_VERSION,
        },
        'implementation': {
            'description': 'PDHC PlanDef Builder production instance',
            'url': 'https://plan.pdhc.se',
        },
        'fhirVersion': '5.0.0',
        'format': ['json'],
        'rest': [{
            'mode': 'server',
            'documentation': (
                'RESTful FHIR R5 server with PlanDefinition read/search support. '
                'Full CRUD is available via the /api/v1/plandefinitions endpoints. '
                'Authentication uses JWT Bearer tokens. Read endpoints are public. '
                'Write endpoints require read_write or admin role. '
                'Rate limit: 200 requests/minute per IP.'
            ),
            'security': {
                'cors': True,
                'service': [{
                    'coding': [{
                        'system': 'http://terminology.hl7.org/CodeSystem/restful-security-service',
                        'code': 'OAuth',
                        'display': 'OAuth',
                    }],
                    'text': 'SSO via sso.pdhc.se — JWT Bearer token',
                }],
                'description': (
                    'Authentication delegated to sso.pdhc.se via SSO handshake (H1-H4). '
                    'Users are redirected to sso.pdhc.se/login and receive a JWT on callback. '
                    'Authorization uses SSO access blob: "planning" phase required for writes. '
                    'Read operations are public.'
                ),
            },
            'resource': [
                {
                    'type': 'PlanDefinition',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/PlanDefinition',
                    'documentation': (
                        'FHIR R5 PlanDefinition resources. Created and edited via the '
                        'builder UI or CRUD API. Exposed as read-only FHIR resources '
                        'with searchset Bundle support.'
                    ),
                    'interaction': [
                        {
                            'code': 'read',
                            'documentation': 'GET /api/v1/PlanDefinition/{fhir_id}',
                        },
                        {
                            'code': 'search-type',
                            'documentation': 'GET /api/v1/PlanDefinition',
                        },
                    ],
                    'versioning': 'versioned',
                    'readHistory': False,
                    'updateCreate': False,
                    'searchParam': [
                        {
                            'name': 'status',
                            'type': 'token',
                            'documentation': 'Filter by status (draft | active | retired)',
                        },
                        {
                            'name': 'title',
                            'type': 'string',
                            'documentation': 'Search by title (case-insensitive, contains)',
                        },
                        {
                            'name': '_count',
                            'type': 'number',
                            'documentation': 'Number of results per page (default 20)',
                        },
                        {
                            'name': '_offset',
                            'type': 'number',
                            'documentation': 'Starting offset for pagination',
                        },
                    ],
                    'operation': [
                        {
                            'name': 'expand',
                            'definition': 'https://plan.pdhc.se/api/v1/PlanDefinition/{fhir_id}/$expand',
                            'documentation': 'Force regeneration of FHIR JSON from current relational data.',
                        },
                    ],
                },
                {
                    'type': 'Questionnaire',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/Questionnaire',
                    'documentation': (
                        'FHIR R5 Questionnaire resources produced from clinical concepts. '
                        'Forms are versioned per form_guid with content fingerprinting for idempotency. '
                        'Managed via /api/v1/forms endpoints. Requires API key or SSO auth for reads, '
                        'read_write role for produce/publish.'
                    ),
                    'interaction': [
                        {
                            'code': 'read',
                            'documentation': 'GET /api/v1/forms/{form_guid}',
                        },
                        {
                            'code': 'search-type',
                            'documentation': 'GET /api/v1/forms',
                        },
                    ],
                    'versioning': 'versioned',
                    'readHistory': True,
                    'updateCreate': False,
                    'operation': [
                        {
                            'name': 'produce',
                            'definition': 'https://plan.pdhc.se/api/v1/forms/produce',
                            'documentation': 'Produce a FHIR Questionnaire from concept_guids or a PlanDefinition.',
                        },
                        {
                            'name': 'publish',
                            'definition': 'https://plan.pdhc.se/api/v1/forms/{form_guid}/publish',
                            'documentation': 'Transition a form version from draft to active status.',
                        },
                    ],
                },
                {
                    'type': 'ValueSet',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/ValueSet',
                    'documentation': (
                        'ValueSets are managed via /api/v1/valuesets (custom CRUD, not FHIR format). '
                        'Each ValueSet contains ordered Values from the values catalog.'
                    ),
                    'interaction': [
                        {
                            'code': 'read',
                            'documentation': 'GET /api/v1/valuesets/{guid}',
                        },
                        {
                            'code': 'search-type',
                            'documentation': 'GET /api/v1/valuesets',
                        },
                        {
                            'code': 'create',
                            'documentation': 'POST /api/v1/valuesets (requires auth)',
                        },
                        {
                            'code': 'update',
                            'documentation': 'PUT /api/v1/valuesets/{guid} (requires auth)',
                        },
                        {
                            'code': 'delete',
                            'documentation': 'DELETE /api/v1/valuesets/{guid} (requires auth)',
                        },
                    ],
                },
                {
                    'type': 'FormDefinition',
                    'profile': 'custom:form-definition',
                    'documentation': (
                        'Authored form definitions that serve as blueprints for FHIR Questionnaires. '
                        'Created via the Forms UI or API. Each definition references concepts '
                        'and can be produced into a versioned FHIR Questionnaire.'
                    ),
                    'interaction': [
                        {
                            'code': 'read',
                            'documentation': 'GET /api/v1/form-definitions/{guid}',
                        },
                        {
                            'code': 'search-type',
                            'documentation': 'GET /api/v1/form-definitions',
                        },
                        {
                            'code': 'create',
                            'documentation': 'POST /api/v1/form-definitions',
                        },
                        {
                            'code': 'update',
                            'documentation': 'PUT /api/v1/form-definitions/{guid}',
                        },
                        {
                            'code': 'delete',
                            'documentation': 'DELETE /api/v1/form-definitions/{guid}',
                        },
                    ],
                    'operation': [
                        {
                            'name': 'produce',
                            'definition': 'https://plan.pdhc.se/api/v1/form-definitions/{guid}/produce',
                            'documentation': 'Produce FHIR Questionnaire from form definition.',
                        },
                        {
                            'name': 'preview',
                            'definition': 'https://plan.pdhc.se/api/v1/form-definitions/{guid}/preview',
                            'documentation': 'Preview resolved form without persisting.',
                        },
                        {
                            'name': 'render-ready',
                            'definition': 'https://plan.pdhc.se/api/v1/form-definitions/{guid}/render-ready',
                            'documentation': 'Render-ready JSON optimized for frontend integration.',
                        },
                    ],
                },
                {
                    'type': 'CodeSystem',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/CodeSystem',
                    'documentation': (
                        'Canonical libraries (terminology authorities like SNOMED CT, LOINC, ICD-10) '
                        'are managed via /api/v1/canonical-libs. Concepts reference these as their '
                        'code system binding.'
                    ),
                    'interaction': [
                        {
                            'code': 'read',
                            'documentation': 'GET /api/v1/canonical-libs/{guid}',
                        },
                        {
                            'code': 'search-type',
                            'documentation': 'GET /api/v1/canonical-libs',
                        },
                        {
                            'code': 'create',
                            'documentation': 'POST /api/v1/canonical-libs (requires auth)',
                        },
                        {
                            'code': 'update',
                            'documentation': 'PUT /api/v1/canonical-libs/{guid} (requires auth)',
                        },
                        {
                            'code': 'delete',
                            'documentation': 'DELETE /api/v1/canonical-libs/{guid} (requires auth)',
                        },
                    ],
                },
            ],
        }],
    }), 200, {'Content-Type': 'application/fhir+json'}


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
    # Search order: planp/docs/ → project root → /project-docs/ (Docker mount)
    planp_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    search_dirs = [
        os.path.join(planp_dir, 'docs'),
        os.path.dirname(planp_dir),
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
