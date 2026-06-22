# PDHC PlanDef Builder — API Reference

**Version:** 1.0.0
**Base URL:** `/api/v1`
**Format:** JSON
**FHIR Version:** R5

---

## Authentication

All write endpoints require a JWT Bearer token. Read endpoints are public.

### Login

```
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "your-password"
}
```

**Response (200):**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "guid": "fbbb5a49-...",
    "username": "admin",
    "role": "admin"
  }
}
```

Access tokens expire after 1 hour. Refresh tokens expire after 30 days.

### Refresh Token

```
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

**Response (200):**

```json
{
  "access_token": "eyJ..."
}
```

### Current User

```
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Logout

```
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

---

## Rate Limiting

- **Default:** 200 requests/minute per IP
- **Login:** 10 requests/minute per IP
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Roles

| Role | Permissions |
|------|------------|
| `read_only` | Read all resources |
| `read_write` | Read and write all resources |
| `admin` | Full access including user management |

---

## GUID Convention

Every entity has a `guid` column (UUID v4, auto-generated). All foreign key references use GUIDs. All API endpoints address resources by GUID.

---

## Canonical Libraries

Terminology authorities (SNOMED CT, LOINC, ICD-10, etc.).

### List All

```
GET /api/v1/lookup/canonical-libs
```

**Response (200):**

```json
[
  {
    "guid": "84ec5c0e-50bd-408e-80a2-3d7a46842742",
    "canonical_lib_name": "SNOMED CT",
    "canonical_lib_display_text": "SNOMED CT",
    "canonical_lib_url": "http://snomed.info/sct",
    "author": null,
    "vers_number": 1,
    "date_created": "2026-03-19T13:14:37",
    "date_valid": "2026-03-19T13:14:37"
  }
]
```

### Create

```
POST /api/v1/lookup/canonical-libs
Authorization: Bearer <token>
Content-Type: application/json

{
  "canonical_lib_name": "LOINC",
  "canonical_lib_display_text": "LOINC",
  "canonical_lib_url": "http://loinc.org"
}
```

**Required:** `canonical_lib_name`

### Read

```
GET /api/v1/lookup/canonical-libs/<guid>
```

### Update

```
PUT /api/v1/lookup/canonical-libs/<guid>
Authorization: Bearer <token>
Content-Type: application/json

{
  "canonical_lib_display_text": "Updated Display"
}
```

### Delete

```
DELETE /api/v1/lookup/canonical-libs/<guid>
Authorization: Bearer <token>
```

**Response (200):** `{"message": "Deleted"}`

---

## Concept Types

Categories of concepts (observation, procedure, diagnosis, etc.).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/lookup/concept-types` | No | List all |
| POST | `/api/v1/lookup/concept-types` | Yes | Create (requires `concept_type_name`) |
| GET | `/api/v1/lookup/concept-types/<guid>` | No | Read one |
| PUT | `/api/v1/lookup/concept-types/<guid>` | Yes | Update |
| DELETE | `/api/v1/lookup/concept-types/<guid>` | Yes | Delete |

**Fields:** `guid`, `concept_type_name`, `concept_type_display_text`, `author`, `vers_number`, `date_created`, `date_valid`

---

## Response Types

Answer shapes (quantity, single choice, text, etc.).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/lookup/response-types` | No | List all |
| POST | `/api/v1/lookup/response-types` | Yes | Create (requires `response_type_name`) |
| GET | `/api/v1/lookup/response-types/<guid>` | No | Read one |
| PUT | `/api/v1/lookup/response-types/<guid>` | Yes | Update |
| DELETE | `/api/v1/lookup/response-types/<guid>` | Yes | Delete |

**Fields:** `guid`, `response_type_name`, `response_type_display_text`, `author`, `vers_number`, `date_created`, `date_valid`

---

## Units

Measurement units (kg, mmHg, mmol/L, etc.).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/lookup/units` | No | List all |
| POST | `/api/v1/lookup/units` | Yes | Create (requires `unit_name`) |
| GET | `/api/v1/lookup/units/<guid>` | No | Read one |
| PUT | `/api/v1/lookup/units/<guid>` | Yes | Update |
| DELETE | `/api/v1/lookup/units/<guid>` | Yes | Delete |

**Fields:** `guid`, `unit_name`, `unit_display_text`, `author`, `vers_number`, `date_created`, `date_valid`

---

## PlanDefinition Types

Selectable type values for the PlanDefinition builder.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/lookup/plandef-types` | No | List all |
| POST | `/api/v1/lookup/plandef-types` | Yes | Create (requires `plandef_type_name`) |
| GET | `/api/v1/lookup/plandef-types/<guid>` | No | Read one |
| PUT | `/api/v1/lookup/plandef-types/<guid>` | Yes | Update |
| DELETE | `/api/v1/lookup/plandef-types/<guid>` | Yes | Delete |

**Fields:** `guid`, `plandef_type_name`, `plandef_type_display_text`, `author`, `vers_number`, `date_created`, `date_valid`

---

## Intended Uses

Selectable tags for transaction usage contexts.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/lookup/intended-uses` | No | List all |
| POST | `/api/v1/lookup/intended-uses` | Yes | Create (requires `intended_use_name`) |
| GET | `/api/v1/lookup/intended-uses/<guid>` | No | Read one |
| PUT | `/api/v1/lookup/intended-uses/<guid>` | Yes | Update |
| DELETE | `/api/v1/lookup/intended-uses/<guid>` | Yes | Delete |

**Fields:** `guid`, `intended_use_name`, `intended_use_display_text`, `author`, `vers_number`, `date_created`, `date_valid`

---

## Values (ValueCatalog)

Individual selectable terms (answer options, coded terms).

### List All

```
GET /api/v1/lookup/values
```

### Create

```
POST /api/v1/lookup/values
Authorization: Bearer <token>
Content-Type: application/json

{
  "value_name": "Mild",
  "canonical_lib": "84ec5c0e-50bd-408e-80a2-3d7a46842742",
  "value_display_text": "Mild severity",
  "canonical_refnumber": "255604002"
}
```

**Required:** `value_name`, `canonical_lib` (GUID)

Name uniqueness is enforced. On API import, names are auto-suffixed if duplicates exist.

### Read

```
GET /api/v1/lookup/values/<guid>
```

### Update

```
PUT /api/v1/lookup/values/<guid>
Authorization: Bearer <token>
```

### Delete

```
DELETE /api/v1/lookup/values/<guid>
Authorization: Bearer <token>
```

---

## ValueSets

Named collections of Values, reusable across Concepts.

> **Note:** as of 2026-06-22 ValueSets are also published as **FHIR R5
> `ValueSet` resources** at `/api/v1/ValueSet/<guid>` with `$expand` and
> scoped `$validate-code` operations. The CRUD JSON below is the
> legacy/builder-UI surface and remains unchanged. See
> [FHIR R5 Terminology Profile](#fhir-r5-terminology-profile) below.

### List All (Paginated)

```
GET /api/v1/lookup/valuesets?page=1&per_page=20
```

### Create

```
POST /api/v1/lookup/valuesets
Authorization: Bearer <token>
Content-Type: application/json

{
  "valueset_name": "Severity Scale",
  "canonical_lib": "84ec5c0e-50bd-408e-80a2-3d7a46842742",
  "valueset_display_text": "Pain severity options"
}
```

**Required:** `valueset_name`, `canonical_lib` (GUID)

### Read / Update / Delete

```
GET    /api/v1/lookup/valuesets/<guid>
PUT    /api/v1/lookup/valuesets/<guid>
DELETE /api/v1/lookup/valuesets/<guid>
```

### ValueSet Membership

#### List Values in a ValueSet

```
GET /api/v1/lookup/valuesets/<guid>/values
```

**Response (200):**

```json
{
  "valueset_guid": "a8902e0e-...",
  "values": [
    {
      "value_guid": "0cbbd99f-...",
      "value_name": "Mild",
      "sort_order": 0
    }
  ]
}
```

#### Add a Value

```
POST /api/v1/lookup/valuesets/<guid>/values
Authorization: Bearer <token>
Content-Type: application/json

{
  "value_guid": "0cbbd99f-d4d5-41db-b9d8-4fd7d6beee16",
  "sort_order": 0
}
```

Duplicate prevention is enforced.

#### Update Sort Order

```
PUT /api/v1/lookup/valuesets/<guid>/values/<value_guid>
Authorization: Bearer <token>
Content-Type: application/json

{
  "sort_order": 2
}
```

#### Remove a Value

```
DELETE /api/v1/lookup/valuesets/<guid>/values/<value_guid>
Authorization: Bearer <token>
```

---

## Concepts

The central terminology object — "things you can ask/measure/record" in care plan transactions and goals.

### List/Search (Paginated)

```
GET /api/v1/concepts?page=1&per_page=20
```

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number (default 1) |
| `per_page` | int | Items per page (default 20, max 200) |
| `search` | string | Text search across name, display text, explanation |
| `concept_type` | GUID | Filter by concept type |
| `response_type` | GUID | Filter by response type |
| `canonical_lib` | GUID | Filter by canonical library |
| `has_values` | bool | Filter concepts with bound values |

**Response (200):**

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "per_page": 20
}
```

### Create

```
POST /api/v1/concepts
Authorization: Bearer <token>
Content-Type: application/json

{
  "concept_name": "systolic_blood_pressure",
  "concept_display_text": "Systolic Blood Pressure",
  "canonical_lib": "84ec5c0e-50bd-408e-80a2-3d7a46842742",
  "canonical_refnumber": "271649006",
  "concept_type": "28b3d058-f646-40c4-a703-7b6e64dcb02d",
  "response_type": "e869b3d0-2f89-4769-a894-ab4015c3f4cb",
  "unit": "c358aa14-9266-44ab-90e3-126d8eb1d85f",
  "range_low": 60,
  "range_high": 250,
  "status": "draft"
}
```

**Required:** `concept_name`, `canonical_lib` (GUID)

All FK references are validated as UUID format. Name uniqueness is enforced (API auto-renames on import). If `response_type` implies single-choice, a `valueset` binding is expected.

### Read (Includes ValueSet Values)

```
GET /api/v1/concepts/<guid>
```

If the concept has a bound ValueSet, the response includes `valueset_values` with the ordered list of values.

### Update

```
PUT /api/v1/concepts/<guid>
Authorization: Bearer <token>
```

Increments `vers_number` and updates `date_valid`.

### Delete

```
DELETE /api/v1/concepts/<guid>
Authorization: Bearer <token>
```

### Concept Values (Through ValueSet)

#### List Values for a Concept

```
GET /api/v1/concepts/<guid>/values
```

Returns the values from the concept's bound ValueSet. Returns 400 if no ValueSet is bound.

#### Add a Value to Concept's ValueSet

```
POST /api/v1/concepts/<guid>/values
Authorization: Bearer <token>
Content-Type: application/json

{
  "value_guid": "0cbbd99f-d4d5-41db-b9d8-4fd7d6beee16"
}
```

#### Remove a Value

```
DELETE /api/v1/concepts/<guid>/values/<value_guid>
Authorization: Bearer <token>
```

---

## PlanDefinitions (CRUD API)

Full CRUD for PlanDefinitions with relational goals, activities, and transactions.

### List/Search (Paginated)

```
GET /api/v1/plandefinitions?page=1&per_page=20&status=draft&search=blood
```

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | int | Page number (default 1) |
| `per_page` | int | Items per page (default 20, max 200) |
| `status` | string | Filter by status (draft, active, retired) |
| `search` | string | Search by title |

### Create

```
POST /api/v1/plandefinitions
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Hypertension Management Plan",
  "description": "Standard care plan for stage 1 hypertension",
  "status": "draft",
  "type": "clinical-protocol",
  "version": "1.0.0",
  "subject_type": "Patient",
  "publisher": "PDHC",
  "validity_duration": "12 mo",
  "goals": [
    {
      "concept_guid": "59013287-07a0-458d-adf4-57f09b93e899",
      "concept_name": "Systolic BP",
      "priority": "high-priority",
      "target_type": "quantity",
      "target_quantity": 130,
      "target_operator": "<=",
      "target_unit": "mmHg"
    }
  ],
  "actions": [
    {
      "title": "Measure Blood Pressure",
      "description": "Standard BP measurement procedure",
      "performer_type": "Practitioner",
      "timing_type": "repeat",
      "timing_frequency": 1,
      "timing_period": 1,
      "timing_period_unit": "wk",
      "transactions": [
        {
          "concept_guid": "59013287-07a0-458d-adf4-57f09b93e899",
          "requirement_type": "required",
          "unit": "mmHg",
          "range_min": 60,
          "range_max": 250
        }
      ]
    }
  ]
}
```

**Required:** `title`

The backend automatically:
- Derives `name` from `title` if not provided
- Computes `effective_period_start/end` from `validity_duration`
- Persists goals, activities, and transactions relationally
- Generates and stores FHIR R5 JSON (`fhir_data`)

**Response (201):** Full PlanDefinition with goals and activities.

### Read (Full Detail)

```
GET /api/v1/plandefinitions/<guid>
```

**Response (200):**

```json
{
  "guid": "8b7ccde6-bed9-4446-ac0b-403716bfd69e",
  "fhir_id": "f2dd13b0-299e-4fdb-bbd2-7da370aadebe",
  "title": "Hypertension Management Plan",
  "name": "hypertension_management_plan",
  "status": "draft",
  "goals": [
    {
      "guid": "a0dc4866-...",
      "concept_guid": "59013287-...",
      "concept_name": "Systolic BP",
      "priority": "high-priority",
      "target_type": "quantity",
      "target_quantity": 130.0,
      "target_operator": "<="
    }
  ],
  "activities": [
    {
      "guid": "8527db52-...",
      "title": "Measure Blood Pressure",
      "sort_order": 0,
      "transactions": [
        {
          "guid": "97dc6b75-...",
          "concept_guid": "59013287-...",
          "requirement_type": "required"
        }
      ]
    }
  ]
}
```

### Update

```
PUT /api/v1/plandefinitions/<guid>
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "active",
  "goals": [...],
  "actions": [...]
}
```

Partial updates are supported. If `goals` or `actions` are provided, existing relational rows are replaced. Orphaned activities (not referenced by any PlanDefinition) are cleaned up.

### Delete

```
DELETE /api/v1/plandefinitions/<guid>
Authorization: Bearer <token>
```

Cascade deletes goals, activity links, transactions, and orphaned activities.

---

## FHIR PlanDefinition (Read-Only)

FHIR R5-compliant read endpoints. These return stored `fhir_data` enriched with identifiers.

### Questionnaire References (definitionCanonical)

When a Questionnaire has been produced from a PlanDefinition (via `/api/v1/forms/produce` with `plandefinition_guid`) and published to `active` status, the FHIR output automatically includes `collect-information` actions with `definitionCanonical` references:

```json
{
  "resourceType": "PlanDefinition",
  "id": "f2dd13b0-...",
  "action": [
    {
      "title": "Daily Vitals Check",
      "type": {
        "coding": [{
          "system": "http://terminology.hl7.org/CodeSystem/action-type",
          "code": "collect-information",
          "display": "Collect information"
        }]
      },
      "definitionCanonical": "Questionnaire/a1b2c3d4-..."
    }
  ]
}
```

This allows downstream consumers (request.pdhc, 1177.pdhc) to discover which Questionnaires to issue to a patient as part of a care plan. Only the latest active version of each linked Questionnaire is included. These actions are appended after any manually authored actions.

### Search (FHIR Bundle)

```
GET /api/v1/PlanDefinition?status=active&title=blood&_count=10&_offset=0
```

**Response (200):** FHIR R5 `searchset` Bundle:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [
    {
      "resource": {
        "resourceType": "PlanDefinition",
        "id": "f2dd13b0-299e-4fdb-bbd2-7da370aadebe",
        "meta": { "versionId": "1", "lastUpdated": "..." },
        "status": "draft",
        "title": "Test Blood Pressure Plan",
        ...
      }
    }
  ]
}
```

### Read Single Resource

```
GET /api/v1/PlanDefinition/<fhir_id>
```

Returns the stored FHIR R5 PlanDefinition resource.

### Expand (Force Regenerate)

```
GET /api/v1/PlanDefinition/<fhir_id>/$expand
```

Forces regeneration of the FHIR JSON from current relational data. Use this to ensure the resource reflects the latest state.

> ⚠️ This `$expand` is **NOT** the FHIR ValueSet `$expand` operation — it
> is a PlanDefinition-specific regen helper that long predates the
> terminology profile. The FHIR ValueSet expansion lives at
> `/api/v1/ValueSet/<guid>/$expand`.

---

## FHIR R5 Terminology Profile

Added 2026-06-22. See
[`plan_pdhc_fhir_terminology_profile_instruction.md`](../../plan_pdhc_fhir_terminology_profile_instruction.md)
for the spec and
[`plan_pdhc_fhir_terminology_profile_DECISIONS.md`](../../plan_pdhc_fhir_terminology_profile_DECISIONS.md)
for the locked design decisions.

Generic FHIR R5 terminology clients can be pointed at this server and
will get conformant ValueSet/CodeSystem/ConceptMap resources plus the
four canonical operations: `$expand`, `$validate-code`, `$lookup`, and
`$translate`.

The legacy CRUD JSON at `/api/v1/lookup/valuesets` and friends remains
unchanged — the new FHIR routes are **additive** and live at
capital-V/C paths.

**Canonical URL convention (ADR D3):** the `url` field on each FHIR
resource is `{base}/fhir/{Resource}/{id}` — an identifier, not a
resolvable route. The routes themselves stay at `/api/v1/...` for
backward compatibility. Search by `?url=` accepts both the new
canonical form and legacy `/api/v1/(lookup/)?valuesets/{guid}` forms
during the transition (D3.b).

### FHIR ValueSet

```
GET  /api/v1/ValueSet                      # searchset Bundle
GET  /api/v1/ValueSet?url=&_count=&_offset=
GET  /api/v1/ValueSet/<guid>               # read
GET  /api/v1/ValueSet/<guid>/$expand       # expand by id
POST /api/v1/ValueSet/$expand              # expand by Parameters body (url|valueSet)
```

The `$expand` response includes `expansion.contains[]` with one entry
per `(system, code, display)` tuple — `system` resolves to the bound
`CanonicalLib.canonical_lib_url`.

### Scoped `$validate-code` (and the global cdr.pdhc shim)

```
# Global / cdr.pdhc shim (UNCHANGED — adoption check):
GET  /api/v1/ValueSet/$validate-code?system=&code=

# Scoped (FHIR ValueSet/$validate-code semantics):
GET  /api/v1/ValueSet/$validate-code?url=&system=&code=
GET  /api/v1/ValueSet/<guid>/$validate-code?system=&code=
POST /api/v1/ValueSet/$validate-code   # Parameters body with url|valueSet + code [+ system]
```

The same path serves both modes. With no `url`/`valueSet`, the
existing global "is this canonical adopted anywhere in plan.pdhc?"
question is answered — preserved byte-for-byte for the cdr.pdhc shim
contract at `cdr.pdhc/cdr_app/app/services/plan_client.py`. With a
ValueSet identifier, FHIR-conformant scoped membership check.

`system` may be either the `CanonicalLib.canonical_lib_url` (FHIR
canonical form) or its name (cdr.pdhc-friendly form). Empty `system`
in the scoped path matches by code alone.

### FHIR CodeSystem + `$lookup`

```
GET  /api/v1/CodeSystem                    # searchset Bundle (the singleton)
GET  /api/v1/CodeSystem/plan-pdhc-local    # read
GET  /api/v1/CodeSystem/$lookup?system=&code=
POST /api/v1/CodeSystem/$lookup            # Parameters body
```

A single local CodeSystem `plan-pdhc-local` (ADR D2). Each
`concept[].code` is the **`Concept.guid`** (ADR D1); `display`
is `concept_display_text || concept_name`; `definition` is
`concept_explain`. The `canonical_lib` binding is surfaced as a
`concept[].property` (`canonical-lib` + `canonical-ref`).

`$lookup` is a two-branch facade:
- `system = {base}/fhir/CodeSystem/plan-pdhc-local` → local Concept
  lookup by guid.
- `system =` (any registered `CanonicalLib` URL or name) → delegates
  to the cached `TermbankClient.lookup(lib_name, code)`, the same
  client that backs `/api/v1/termbank/concept/...`.
- `system =` unregistered → HTTP 404 OperationOutcome **without**
  calling termbank.

### FHIR ConceptMap + `$translate`

```
GET  /api/v1/ConceptMap                              # searchset Bundle
GET  /api/v1/ConceptMap/plan-pdhc-canonical-bindings # read
GET  /api/v1/ConceptMap/$translate?system=&code=&targetsystem=
POST /api/v1/ConceptMap/$translate                   # Parameters body
```

A single platform ConceptMap projecting every Concept's
`canonical_lib + canonical_refnumber` binding. Source = the local
CodeSystem. Targets = one group per registered CanonicalLib URL.
Relationship is always `equivalent`.

`$translate` is **bidirectional**:

| `system` | `code` | Behaviour |
|---|---|---|
| local CS URL | a `Concept.guid` | returns the canonical binding (LOINC code, SNOMED code, etc.) |
| CanonicalLib URL | a `canonical_refnumber` | returns the local Concept guid |
| CanonicalLib name | a `canonical_refnumber` | as above (cdr.pdhc-friendly) |

`match[]` is always shaped as a repeating FHIR Parameters part —
zero matches emit zero `match` parameters; a single match emits one;
future multi-binding additions are additive and don't break the
contract (Risk §9.5 of the spec).

### Explicitly NOT supported (declared in CapabilityStatement)

The local data model is deliberately flat — no inter-concept
hierarchy. The following FHIR terminology operations are out of
scope by design and are declared as such in `GET /api/v1/metadata`:

- `CodeSystem/$subsumes`
- `is-a` / descendant filters in `ValueSet.compose` and `$expand`
- hierarchical `$lookup` properties (parent/child)

### Conformance

- Every test run validates outputs against `fhir.resources` R5
  pydantic models (D5 fast layer).
- For the canonical HL7 R5 validator: `make corpus && make conformance`
  in `planp/`. Requires `VALIDATOR_JAR` pointing to a downloaded copy
  of `validator_cli.jar` (`make check-jar` shows the download URL).
- The cdr.pdhc cross-service `$validate-code` shim contract is
  re-pinned by two regression tests:
  `test_capability.py::TestCDRValidateCodeContract` and
  `test_fhir_valueset.py::TestCDRGlobalContractAfter62`.

---

## Capability Statement

### Full Capability Statement

```
GET /api/v1/capability-statement
```

Returns grouped endpoint listing with auth, rate limiting, and role information.

### Flat Endpoint List

```
GET /api/v1/endpoints
```

Returns all 64 endpoints with method, path, auth requirement, and description.

---

## Documentation

### List Available Documents

```
GET /api/v1/docs
```

Returns a list of all available documentation files with download URLs.

### Download a Document

```
GET /api/v1/docs/<filename>
```

Returns the document as a downloadable file.

---

## Form Definitions

Authored form blueprints — the intermediate layer between clinical concepts and FHIR Questionnaires. Build a definition by selecting concepts, configuring per-question overrides, then produce a validated FHIR Questionnaire.

### List Definitions

```
GET /api/v1/form-definitions?status=draft&search=vitals&limit=100&offset=0
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status (draft, active, retired) |
| `search` | string | Search by title |
| `limit` | int | Max results (default 100) |
| `offset` | int | Pagination offset (default 0) |

### Create Definition

```
POST /api/v1/form-definitions
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Daily Vitals Check",
  "name": "daily_vitals_check",
  "description": "Standard vitals capture form"
}
```

**Required:** `title`, `name`

### Read Definition (With Resolved Items)

```
GET /api/v1/form-definitions/<guid>
```

Returns the definition with all items resolved against their concepts (names, response types, canonical references).

### Update Definition

```
PUT /api/v1/form-definitions/<guid>
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

### Delete Definition

```
DELETE /api/v1/form-definitions/<guid>
Authorization: Bearer <token>
```

Only draft definitions can be deleted.

### List Items

```
GET /api/v1/form-definitions/<guid>/items
```

### Add Item (Concept)

```
POST /api/v1/form-definitions/<guid>/items
Authorization: Bearer <token>
Content-Type: application/json

{
  "concept_guid": "59013287-07a0-458d-adf4-57f09b93e899",
  "required": true,
  "display_text_override": "Blood Pressure (systolic)",
  "group_label": "Vitals"
}
```

**Required:** `concept_guid`

### Update Item

```
PUT /api/v1/form-definitions/<guid>/items/<item_guid>
Authorization: Bearer <token>
Content-Type: application/json

{
  "required": true,
  "enabled": true,
  "display_text_override": "Custom label",
  "group_label": "Assessment"
}
```

### Remove Item

```
DELETE /api/v1/form-definitions/<guid>/items/<item_guid>
Authorization: Bearer <token>
```

### Reorder Items

```
POST /api/v1/form-definitions/<guid>/reorder
Authorization: Bearer <token>
Content-Type: application/json

{
  "ordered_guids": ["guid-1", "guid-2", "guid-3"]
}
```

### Produce FHIR Questionnaire

```
POST /api/v1/form-definitions/<guid>/produce
Authorization: Bearer <token>
```

Resolves all enabled items against concepts, builds a validated FHIR R5 Questionnaire, and persists it. Returns the produced form GUID and version.

### Preview (Without Persisting)

```
GET /api/v1/form-definitions/<guid>/preview
```

Returns resolved items without producing a Questionnaire.

### Get Produced Questionnaire

```
GET /api/v1/form-definitions/<guid>/questionnaire?version=1
```

Returns the FHIR Questionnaire JSON. Supports API key or SSO authentication.

### Get Render-Ready Output

```
GET /api/v1/form-definitions/<guid>/render-ready?version=1
```

Returns a simplified representation suitable for UI rendering. Supports API key or SSO authentication.

---

## Error Responses

All errors follow a consistent format:

```json
{
  "error": "Description of what went wrong"
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad request (missing fields, invalid UUID) |
| 401 | Unauthorized (missing or invalid token) |
| 403 | Forbidden (insufficient role) |
| 404 | Resource not found |
| 409 | Conflict (duplicate name) |
| 429 | Rate limit exceeded |

---

## Endpoint Summary

| # | Resource | Endpoints | Auth (Write) |
|---|----------|-----------|-------------|
| 1 | Auth | 4 | Mixed |
| 2 | Canonical Libraries | 5 | read_write |
| 3 | Concept Types | 5 | read_write |
| 4 | Response Types | 5 | read_write |
| 5 | Units | 5 | read_write |
| 6 | PlanDef Types | 5 | read_write |
| 7 | Intended Uses | 5 | read_write |
| 8 | Values | 5 | read_write |
| 9 | ValueSets | 5 | read_write |
| 10 | ValueSet Membership | 4 | read_write |
| 11 | Concepts | 5 | read_write |
| 12 | Concept Values | 3 | read_write |
| 13 | PlanDefinitions (CRUD) | 5 | read_write |
| 14 | FHIR PlanDefinition | 3 | Public |
| 15 | Form Definitions | 14 | Mixed |
| 16 | Capability | 2 | Public |
| 17 | Documentation | 2 | Public |
| | **Total** | **82** | |
