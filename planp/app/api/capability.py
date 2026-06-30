import os
from flask import Blueprint, jsonify, send_file, abort
from app import limiter

capability_bp = Blueprint('capability', __name__)
# Rate limiting is set globally via RATELIMIT_DEFAULT in app/__init__.py.
# /capability is intended to be freely pollable by service-discovery, so
# its view is decorated with @limiter.exempt below.

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
    # Auth — SSO redirect handshake. Plan.pdhc does not issue tokens
    # itself; bearer tokens are validated per-request against sso.pdhc.
    # Trusted sibling services may bypass SSO with X-Source-Service +
    # X-Service-Key headers (see KNOWN_SERVICES in app/api/auth.py).
    _endpoint('GET', '/auth/login', False,
              '302 redirect to sso.pdhc to begin the SSO handshake'),
    _endpoint('GET', '/auth/callback', False,
              'SSO redirect target — exchanges code for access token and sets session'),
    _endpoint('GET', '/auth/logout', True, 'Logout (clears session)'),
    _endpoint('POST', '/auth/logout', True, 'Logout (clears session)'),
    _endpoint('GET', '/auth/me', True, 'Get current authenticated user'),

    # Canonical Libraries (lookup blueprint, /api/v1/lookup prefix)
    _endpoint('GET', '/lookup/canonical-libs', False, 'List all canonical libraries'),
    _endpoint('POST', '/lookup/canonical-libs', True, 'Create a canonical library'),
    _endpoint('GET', '/lookup/canonical-libs/<guid>', False, 'Read a canonical library'),
    _endpoint('PUT', '/lookup/canonical-libs/<guid>', True, 'Update a canonical library'),
    _endpoint('DELETE', '/lookup/canonical-libs/<guid>', True, 'Delete a canonical library'),

    # Concept Types
    _endpoint('GET', '/lookup/concept-types', False, 'List all concept types'),
    _endpoint('POST', '/lookup/concept-types', True, 'Create a concept type'),
    _endpoint('GET', '/lookup/concept-types/<guid>', False, 'Read a concept type'),
    _endpoint('PUT', '/lookup/concept-types/<guid>', True, 'Update a concept type'),
    _endpoint('DELETE', '/lookup/concept-types/<guid>', True, 'Delete a concept type'),

    # Response Types
    _endpoint('GET', '/lookup/response-types', False, 'List all response types'),
    _endpoint('POST', '/lookup/response-types', True, 'Create a response type'),
    _endpoint('GET', '/lookup/response-types/<guid>', False, 'Read a response type'),
    _endpoint('PUT', '/lookup/response-types/<guid>', True, 'Update a response type'),
    _endpoint('DELETE', '/lookup/response-types/<guid>', True, 'Delete a response type'),

    # Units
    _endpoint('GET', '/lookup/units', False, 'List all units'),
    _endpoint('POST', '/lookup/units', True, 'Create a unit'),
    _endpoint('GET', '/lookup/units/<guid>', False, 'Read a unit'),
    _endpoint('PUT', '/lookup/units/<guid>', True, 'Update a unit'),
    _endpoint('DELETE', '/lookup/units/<guid>', True, 'Delete a unit'),

    # PlanDef Types
    _endpoint('GET', '/lookup/plandef-types', False, 'List all PlanDefinition types'),
    _endpoint('POST', '/lookup/plandef-types', True, 'Create a PlanDefinition type'),
    _endpoint('GET', '/lookup/plandef-types/<guid>', False, 'Read a PlanDefinition type'),
    _endpoint('PUT', '/lookup/plandef-types/<guid>', True, 'Update a PlanDefinition type'),
    _endpoint('DELETE', '/lookup/plandef-types/<guid>', True, 'Delete a PlanDefinition type'),

    # Intended Uses
    _endpoint('GET', '/lookup/intended-uses', False, 'List all intended uses'),
    _endpoint('POST', '/lookup/intended-uses', True, 'Create an intended use'),
    _endpoint('GET', '/lookup/intended-uses/<guid>', False, 'Read an intended use'),
    _endpoint('PUT', '/lookup/intended-uses/<guid>', True, 'Update an intended use'),
    _endpoint('DELETE', '/lookup/intended-uses/<guid>', True, 'Delete an intended use'),

    # Values
    _endpoint('GET', '/lookup/values', False, 'List all values'),
    _endpoint('POST', '/lookup/values', True, 'Create a value'),
    _endpoint('GET', '/lookup/values/<guid>', False, 'Read a value'),
    _endpoint('PUT', '/lookup/values/<guid>', True, 'Update a value'),
    _endpoint('DELETE', '/lookup/values/<guid>', True, 'Delete a value'),

    # ValueSets
    _endpoint('GET', '/lookup/valuesets', False, 'List all valuesets (paginated)'),
    _endpoint('POST', '/lookup/valuesets', True, 'Create a valueset'),
    _endpoint('GET', '/lookup/valuesets/<guid>', False, 'Read a valueset'),
    _endpoint('PUT', '/lookup/valuesets/<guid>', True, 'Update a valueset'),
    _endpoint('DELETE', '/lookup/valuesets/<guid>', True, 'Delete a valueset'),

    # ValueSet Membership
    _endpoint('GET', '/lookup/valuesets/<guid>/values', False, 'List values in a valueset'),
    _endpoint('POST', '/lookup/valuesets/<guid>/values', True, 'Add a value to a valueset'),
    _endpoint('PUT', '/lookup/valuesets/<guid>/values/<value_guid>', True, 'Update sort order of a value in a valueset'),
    _endpoint('DELETE', '/lookup/valuesets/<guid>/values/<value_guid>', True, 'Remove a value from a valueset'),

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
    _endpoint('GET', '/PlanDefinition/<fhir_id>/$expand', False,
              'Force regenerate FHIR JSON (note: NOT the FHIR ValueSet $expand — '
              'see /ValueSet/<guid>/$expand below for that)'),

    # FHIR R5 terminology profile (§6.1-§6.4) — additive; legacy CRUD untouched.
    # ValueSet — FHIR resource + $expand + scoped $validate-code
    _endpoint('GET', '/ValueSet', False, 'FHIR R5 searchset Bundle (?url=, _count, _offset)'),
    _endpoint('GET', '/ValueSet/<guid>', False, 'FHIR R5 ValueSet resource'),
    _endpoint('GET', '/ValueSet/<guid>/$expand', False, 'Expand by id — returns ValueSet with expansion.contains[]'),
    _endpoint('POST', '/ValueSet/$expand', False, 'Expand by FHIR Parameters body (url or valueSet)'),
    _endpoint('GET', '/ValueSet/$validate-code', False,
              'Global (no url): the cdr.pdhc adoption-check shim (unchanged). '
              'Scoped (with ?url= or ?valueSet=): FHIR ValueSet/$validate-code.'),
    _endpoint('GET', '/ValueSet/<guid>/$validate-code', False, 'Scoped $validate-code by path id'),
    _endpoint('POST', '/ValueSet/$validate-code', False, 'Scoped $validate-code by Parameters body'),

    # CodeSystem — local concept system + $lookup with termbank delegation
    _endpoint('GET', '/CodeSystem', False, 'FHIR R5 searchset Bundle (?url=)'),
    _endpoint('GET', '/CodeSystem/<id>', False,
              'Read the local CodeSystem (id=plan-pdhc-local). codes are Concept.guid (ADR D1).'),
    _endpoint('GET', '/CodeSystem/$lookup', False,
              'Lookup by query params. system=LOCAL → local Concept; system=CanonicalLib URL/name → delegates to termbank.'),
    _endpoint('POST', '/CodeSystem/$lookup', False, 'Lookup by Parameters body'),

    # ConceptMap — the local↔canonical mapping
    _endpoint('GET', '/ConceptMap', False, 'FHIR R5 searchset Bundle (?url=)'),
    _endpoint('GET', '/ConceptMap/<id>', False,
              'Read the platform ConceptMap (id=plan-pdhc-canonical-bindings).'),
    _endpoint('GET', '/ConceptMap/$translate', False,
              'Bidirectional translate. system=LOCAL → canonical code; system=CanonicalLib URL/name → local guid.'),
    _endpoint('POST', '/ConceptMap/$translate', False, 'Translate by Parameters body'),

    # Termbank proxies (§0.2 — pre-existing, here for completeness)
    _endpoint('GET', '/termbank/concept/<system>/<code>', False, 'Same-origin termbank proxy (TTL cache)'),
    _endpoint('GET', '/termbank/search', False, 'Same-origin termbank search proxy'),

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
@limiter.exempt
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
            'me': f'{BASE}/auth/me',
            'note': 'Authentication is delegated to sso.pdhc.se. GET '
                    f'{BASE}/auth/login returns a 302 redirect to sso.pdhc; '
                    'sso.pdhc then redirects back to /auth/callback with a '
                    'code that this service exchanges for an access token '
                    'and validates per-request against sso.pdhc /api/auth/me/service. '
                    'No JWTs are issued by this service. Read endpoints are public; '
                    'write endpoints require the "planning" phase.',
            'service_key_bypass': {
                'description': 'Trusted sibling services may bypass SSO by '
                               'sending the headers below. Each service\'s '
                               'expected key is held in the service\'s env var.',
                'headers': ['X-Source-Service', 'X-Service-Key'],
                'known_sources': ['loader.pdhc', 'sim.pdhc'],
            },
        },
        'rate_limiting': {
            'default': '200 requests/minute per source',
            'exempt': [f'{BASE}/capability-statement', f'{BASE}/metadata',
                       f'{BASE}/endpoints', '/api/health'],
            'service_key_exempt': True,
            'note': 'A global default of 200/min applies via RATELIMIT_DEFAULT. '
                    'Endpoints listed in "exempt" and any request that carries '
                    'a valid X-Source-Service + X-Service-Key bypass the limiter.',
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
@limiter.exempt
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
                    # Text-only CodeableConcept (FHIR R5: text alone is
                    # valid when no coding is provided). The HL7
                    # restful-security-service CodeSystem URL is correct
                    # but its terminology package isn't always in the
                    # validator's offline store, producing a false-positive
                    # error. Text alone validates clean and conveys the
                    # same information.
                    'text': 'OAuth — SSO via sso.pdhc.se (JWT Bearer token)',
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
                        'Two surfaces, both supported. The FHIR R5 surface at /api/v1/ValueSet '
                        '(capital V) is conformant — read, search by url, $expand, and scoped '
                        '$validate-code. The legacy CRUD JSON at /api/v1/lookup/valuesets is '
                        'unchanged and serves the builder UI; canonical URLs emitted from the '
                        'legacy CRUD are accepted by FHIR routes as legacy identifiers (ADR D3.b).'
                    ),
                    'interaction': [
                        {'code': 'read',
                         'documentation': 'GET /api/v1/ValueSet/{guid}'},
                        {'code': 'search-type',
                         'documentation': 'GET /api/v1/ValueSet?url=&_count=&_offset='},
                    ],
                    'searchParam': [
                        {'name': 'url', 'type': 'uri',
                         'documentation': 'Filter by canonical url; accepts FHIR canonical '
                                          'form AND legacy /api/v1/(lookup/)?valuesets/{guid} '
                                          '(ADR D3.b transition rule).'},
                        {'name': '_count', 'type': 'number',
                         'documentation': 'Page size (default 20, max 200)'},
                        {'name': '_offset', 'type': 'number',
                         'documentation': 'Starting offset for pagination'},
                    ],
                    'operation': [
                        {'name': 'expand',
                         'definition': 'http://hl7.org/fhir/OperationDefinition/ValueSet-expand',
                         'documentation': 'GET /ValueSet/{guid}/$expand or POST /ValueSet/$expand '
                                          'with Parameters body (url|valueSet). Returns ValueSet '
                                          'with expansion.contains[].'},
                        {'name': 'validate-code',
                         'definition': 'http://hl7.org/fhir/OperationDefinition/ValueSet-validate-code',
                         'documentation': (
                             'TWO MODES: (1) global — GET /ValueSet/$validate-code?system=&code= '
                             '(no url) answers "is this canonical adopted anywhere in plan.pdhc?" '
                             'This is the cdr.pdhc shim contract (see '
                             'cdr.pdhc/cdr_app/app/services/plan_client.py). Preserved unchanged. '
                             '(2) scoped — same path with ?url=, or GET /ValueSet/{guid}/$validate-code, '
                             'or POST with Parameters body — checks (system, code) against THIS '
                             "ValueSet's expansion."),
                        },
                    ],
                },
                # FormDefinition is a plan.pdhc internal authoring model
                # (the blueprint that produces FHIR Questionnaires); it is
                # NOT itself a FHIR resource type, so it doesn't belong in
                # CapabilityStatement.rest.resource (which is bound to the
                # core FHIR resource-types ValueSet). Its routes remain
                # listed in the flat /api/v1/endpoints inventory. Function-
                # ally, the produce/preview/render-ready operations land
                # output as Questionnaire resources, which ARE declared
                # above.
                {
                    'type': 'CodeSystem',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/CodeSystem',
                    'documentation': (
                        'Single local CodeSystem id=plan-pdhc-local (ADR D2). Each entry uses '
                        'Concept.guid as the code (ADR D1), with concept_display_text as display '
                        'and concept_explain as definition. The canonical_lib binding is surfaced '
                        'as concept[].property. External authorities (LOINC, SNOMED, ICD-10, ATC, …) '
                        'are NOT published here as CodeSystems — they live in termbank.pdhc; '
                        '$lookup with an external system delegates to the cached TermbankClient.'
                    ),
                    'interaction': [
                        {'code': 'read',
                         'documentation': 'GET /api/v1/CodeSystem/plan-pdhc-local'},
                        {'code': 'search-type',
                         'documentation': 'GET /api/v1/CodeSystem?url='},
                    ],
                    'searchParam': [
                        {'name': 'url', 'type': 'uri',
                         'documentation': 'Filter by canonical url'},
                    ],
                    'operation': [
                        {'name': 'lookup',
                         'definition': 'http://hl7.org/fhir/OperationDefinition/CodeSystem-lookup',
                         'documentation': (
                             'GET /CodeSystem/$lookup?system=&code= or POST Parameters body. '
                             'system=LOCAL_CS_URL → local Concept (code is the guid). '
                             'system=CanonicalLib URL or name → delegates to termbank.pdhc '
                             '(TTL-cached). Unknown system → 404 without touching termbank.'),
                        },
                    ],
                },
                {
                    'type': 'ConceptMap',
                    'profile': 'http://hl7.org/fhir/StructureDefinition/ConceptMap',
                    'documentation': (
                        'Single platform ConceptMap id=plan-pdhc-canonical-bindings projecting '
                        "every Concept's canonical_lib + canonical_refnumber binding. Source = "
                        'CodeSystem plan-pdhc-local; targets = each registered CanonicalLib URL. '
                        'Relationship is always "equivalent" (plan.pdhc treats canonical bindings '
                        'as 1:1 equivalences by design). $translate is bidirectional: LOCAL→canonical '
                        'AND canonical→LOCAL.'
                    ),
                    'interaction': [
                        {'code': 'read',
                         'documentation': 'GET /api/v1/ConceptMap/plan-pdhc-canonical-bindings'},
                        {'code': 'search-type',
                         'documentation': 'GET /api/v1/ConceptMap?url='},
                    ],
                    'searchParam': [
                        {'name': 'url', 'type': 'uri',
                         'documentation': 'Filter by canonical url'},
                    ],
                    'operation': [
                        {'name': 'translate',
                         'definition': 'http://hl7.org/fhir/OperationDefinition/ConceptMap-translate',
                         'documentation': (
                             'GET /ConceptMap/$translate?system=&code=&targetsystem= or POST '
                             'Parameters body. Bidirectional. Match shape: repeating FHIR '
                             'Parameters parts named "match" — multi-binding-future-safe '
                             '(Risk §9.5).'),
                        },
                    ],
                },
                {
                    # Documentation block — §7 explicit non-goals.
                    # Surfaced as a non-FHIR-resource entry whose 'type' is a
                    # well-known invented marker, so FHIR clients still parse
                    # the resource list cleanly. This is the truth-telling
                    # required by ADR §7 / spec §7.
                    'type': 'OperationDefinition',
                    'documentation': (
                        'EXPLICITLY UNSUPPORTED operations (per spec §7 — local data model '
                        'is deliberately flat, no inter-concept hierarchy):\n'
                        '  • CodeSystem/$subsumes — no parent/child relationship in the data\n'
                        '  • ValueSet.compose is-a / descendant filters — no hierarchy to walk\n'
                        '  • CodeSystem $lookup hierarchical properties (parent/child) — '
                        'omitted; canonical_lib/canonical_refnumber are the only properties surfaced.\n'
                        'A CapabilityStatement that claimed these and then failed would be worse '
                        'than one that honestly excludes them.'
                    ),
                },
            ],
        }],
    }), 200, {'Content-Type': 'application/fhir+json'}


@capability_bp.route('/endpoints', methods=['GET'])
@limiter.exempt
def list_endpoints():
    return jsonify({
        'total': len(ENDPOINTS),
        'endpoints': ENDPOINTS,
    }), 200


# --- Documentation API ---

DOCS_CATALOG = {
    'api_reference.md': 'Comprehensive REST API reference with examples (includes FHIR R5 terminology profile §6)',
    'db_schema_snapshot.md': 'Database schema — all 17 tables with samples and GUIDs',
    'plan_description.md': 'Domain architecture — concepts, values, valuesets, PlanDefinitions, FHIR terminology profile',
    'readme.md': 'Deployment plan — step-by-step setup and configuration',
    'progress.md': 'Progress log — completed and pending steps (incl. §6 IMPLEMENTATION COMPLETE 2026-06-22)',
    'top_rules.md': 'Project rules (immutable)',
    'repo_css.md': 'Frontend design system — colours, typography, components',
    'pdhc_markdown_layout_standard.md': 'Markdown formatting standard',
    'changed_files.md': 'Registry of all created and edited files',
    'nginx_implement_server19March.md': 'Nginx reverse proxy deployment template',
    'plan_pdhc_fhir_terminology_profile_instruction.md': 'FHIR R5 terminology profile — implementation spec (Status: IMPLEMENTED 2026-06-22)',
    'plan_pdhc_fhir_terminology_profile_DECISIONS.md': 'FHIR R5 terminology profile — ADR for the five locked design decisions',
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
