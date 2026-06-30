# PDHC PlanDef Builder — Progress Log

This file tracks progress after each step in the deployment plan (`readme.md`). Numbering matches the plan. Per Rule 4, no step advances until all tests are cleared.

---

## 1) Environment and infrastructure setup

### 1.1 Prerequisites and tooling

- **1.a** Docker Compose v5.1.0 — verified.
- **1.b** Python 3.14.3 — verified.
- **1.c** `psql` not installed locally — not blocking (can use `docker exec` for DB inspection).
- **1.d** Ports 9030–9033 all free — verified.

### 1.2 Project directory structure

- **1.e** Directory structure created under `planp/` with all required subdirectories.
- **1.f** `progress.md` created.
- **1.g** `changed_files.md` created.

### 1.3 Git initialisation

- **1.h** Git repo initialised. `.gitignore` created covering venv, `.env`, `__pycache__`, results, `_obs_gateway_repo`.
- **1.i** Pending: initial commit (awaiting operator).

---

## 2) Docker and database setup

- **2.a** `planp/docker-compose.yml` created — PostgreSQL 16 on port 9031, app on port 9030.
- **2.b** `planp/.env` created with development credentials.
- **2.c** `planp/.env.example` created with placeholder values.
- **2.d** `planp/Dockerfile` created with `entrypoint.sh` that runs migrations before starting gunicorn.
- **2.e** App service added to `docker-compose.yml`, depends on db health check.
- **2.f** Docker build succeeded — `planp-app:latest` image built.
- **2.g** Full stack verified: `pdhc_db` (PostgreSQL 16, port 9031, healthy) + `pdhc_app` (Flask/gunicorn, port 9030, running). API responds to requests.
- **2.h** `start.sh` created at project root — kills ports 9000–9003 and 9030–9033, starts Docker, activates venv, graceful shutdown on Ctrl+C.
- **2.i** `start.sh` made executable.

---

## 3) Application foundation (Flask + SQLAlchemy)

- **3.a** Virtual environment created at `planp/venv`.
- **3.b** `planp/requirements.txt` created with all dependencies.
- **3.c** Dependencies installed successfully.
- **3.d** `planp/app/__init__.py` — Flask app factory implemented with blueprint registration and bootstrap superuser logic.
- **3.e** `planp/app/config.py` — configuration loader implemented.
- **3.f** Flask-Migrate initialised — `planp/migrations/` directory created.
- **3.g** Migration directory confirmed inside `planp/`.

### 3.4 Tests

- **3.h–3.j** App factory tests included in broader test suite — all passing.

---

## 4) Data models

- **4.a** `user_models.py` — User model with GUID, password hashing, roles.
- **4.b** `concept_models.py` — All 6 lookup table models (CanonicalLib, ConceptType, ResponseType, Unit, PlanDefType, IntendedUse).
- **4.c** `concept_models.py` — ValueCatalog, ValueSet, ValueSetValue models with junction table and uniqueness constraints.
- **4.d** `concept_models.py` — Concept model with FK refs via GUID, check constraint on range, valueset binding.
- **4.e** `fhir_models.py` — PlanDefinition model with FHIR fields and JSONB `fhir_data`.
- **4.f** `activity_models.py` — Activity, Transaction, PlanDefinitionGoal, PlanDefinitionActivity models.
- **4.g** Migration generated: `c3d87bb08504_initial_models.py` — 16 tables detected.
- **4.h** Migration applied: all 17 tables created in PostgreSQL (16 app + alembic_version). Verified via `\dt`.

### 4.6 Tests

- **4.i–4.j** Model tests covered via integration tests in the full suite.

---

## 5) Authentication and authorisation

- **5.a** `api/auth.py` — login (JWT), logout, me, refresh endpoints implemented. Rate limited: 10/min on login.
- **5.b** Bootstrap superuser logic in app factory + conftest.
- **5.c** `requires_role` decorator implemented with role levels (read_only < read_write < admin).

### 5.3 Tests

- **5.d** `test_auth.py` — 7 tests, all passing:
  - `test_login_valid` — PASSED
  - `test_login_invalid_password` — PASSED
  - `test_login_missing_fields` — PASSED
  - `test_me_authenticated` — PASSED
  - `test_me_unauthenticated` — PASSED
  - `test_logout` — PASSED
  - `test_bootstrap_superuser_created` — PASSED

---

## 6) Lookup table CRUD

- **6.a** `api/lookup_tables.py` — Generic CRUD for all 6 lookup tables via `_crud_routes` factory. Rate limited: 200/min.
- **6.b** Auth enforcement: write endpoints require `read_write` role.
- **6.c** Input sanitisation via `bleach.clean()`.
- **6.d** UUID validation on all GUID fields.

### 6.2 Tests

- **6.e** `test_lookup_tables.py` — 7 tests, all passing:
  - `TestCanonicalLibs::test_crud_cycle` — PASSED
  - `TestCanonicalLibs::test_duplicate_name` — PASSED
  - `TestCanonicalLibs::test_invalid_uuid` — PASSED
  - `TestCanonicalLibs::test_auth_required_for_create` — PASSED
  - `TestConceptTypes::test_crud_cycle` — PASSED
  - `TestResponseTypes::test_crud_cycle` — PASSED
  - `TestUnits::test_crud_cycle` — PASSED

---

## 7) Values and ValueSets CRUD

- **7.a** Values CRUD endpoints implemented (list, create, read, update, delete).
- **7.b** Auto-rename on import via `make_unique_value_name`.
- **7.c** ValueSets CRUD with pagination.
- **7.d** ValueSet membership (add, remove, list with sort order, update sort order, duplicate prevention).

### 7.4 Tests

- **7.e** `test_valuesets.py` — 4 tests, all passing:
  - `TestValues::test_crud_cycle` — PASSED
  - `TestValues::test_requires_canonical_lib` — PASSED
  - `TestValueSets::test_crud_cycle` — PASSED
  - `TestValueSetMembership::test_add_remove_values` — PASSED

---

## 8) Concept CRUD

- **8.a** Concept CRUD with filtering, pagination, deterministic sort. Rate limited: 200/min.
- **8.b** Concept-values endpoints (through ValueSet).
- **8.c** `name_uniqueness.py` — NameUniquenessService with auto-rename and manual validation.

### 8.4 Tests

- **8.d** `test_concepts.py` — 9 tests, all passing:
  - `test_create_and_read` — PASSED
  - `test_list_with_pagination` — PASSED
  - `test_update` — PASSED
  - `test_delete` — PASSED
  - `test_auth_required` — PASSED
  - `test_invalid_uuid_rejected` — PASSED
  - `test_name_uniqueness_auto_rename` — PASSED
  - `test_concept_values_through_valueset` — PASSED
  - `test_no_valueset_error` — PASSED

---

## 9) FHIR service and PlanDefinition serialization

- **9.a** `fhir_service.py` — `FHIRService.create_fhir_plandefinition()` implemented.

### 9.2 Tests

- **9.c** `test_fhir_endpoints.py` — 5 tests, all passing:
  - `test_basic_serialization` — PASSED
  - `test_defaults` — PASSED
  - `test_goals_and_actions_included` — PASSED
  - `test_identifier_and_url` — PASSED
  - `test_optional_fields_omitted_when_empty` — PASSED

---

## 10) PlanDefinition builder (web UI)

- **10.a** `routes/plandefinitions.py` — All web routes implemented (list, builder, create, view, edit, delete, export).
- **10.b** Builder save flow implemented per plan_description.md section 5.5.
- **10.c** Client-side builder JavaScript implemented inline in `builder.html` template (~400 lines). Includes: `addGoal()`, `addAction()`, `addTransaction()`, `collectGoals()`, `collectActions()`, `buildFhirPreview()`, `updatePreview()`.
- **10.d** All HTML templates implemented:
  - `plandefinitions/builder.html` — 2-column layout (form builder left, live FHIR JSON preview right)
  - `plandefinitions/list.html` — paginated PlanDefinition list
  - `plandefinitions/view.html` — PlanDefinition detail view with FHIR export

---

## 11) FHIR PlanDefinition API endpoints

- **11.a** `api/fhir_plandefinitions.py` — search (Bundle), read, expand. Rate limited: 200/min.
- **11.b** `api/plandefinitions.py` — Full CRUD API for PlanDefinitions (list, create, read, update, delete) with relational goal/activity/transaction persistence and FHIR JSON generation.

### 11.3 Tests

- **11.d** `test_plandefinitions.py` — 4 tests, all passing:
  - `test_search_returns_bundle` — PASSED
  - `test_not_found` — PASSED
  - `test_post_returns_501` — PASSED
  - `test_search_with_filters` — PASSED

---

## 12) API expansion and rate limiting (2026-03-20)

- **12.a** Flask-Limiter integrated (200/min default, 10/min on login, memory storage).
- **12.b** Rate limit headers enabled: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.
- **12.c** Token refresh endpoint added: `POST /api/v1/auth/refresh`.
- **12.d** ValueSet membership sort order update endpoint: `PUT /api/v1/valuesets/<guid>/values/<value_guid>`.
- **12.e** Full CRUD PlanDefinition API with relational persistence (goals, activities, transactions).

---

## 13) Capability statement (2026-03-20)

- **13.a** `api/capability.py` — capability statement endpoint with grouped resource listing.
- **13.b** Flat endpoint list at `GET /api/v1/endpoints`.
- **13.c** 68 total API endpoints documented across 16 resource groups.

---

## 14) Web UI completion (2026-03-20)

- **14.a** Dashboard at `/` with counts for all 8 resource types.
- **14.b** 2-column PlanDefinition builder: form builder (left) + live FHIR JSON preview (right).
- **14.c** Dropdown-based concept/unit/valueset selection with GUID tags displayed.
- **14.d** Complete web CRUD for all entities:
  - Concepts: list, create, view (3 templates)
  - Values: list, create, edit, view (4 templates)
  - ValueSets: list, create, edit, view + membership management (4 templates)
  - Lookup tables: 4 types x 4 templates = 16 templates (canonical libs, units, response types, concept types)
  - PlanDefinitions: builder, list, view (3 templates)
- **14.e** Navigation bar with links to all entity management pages.
- **14.f** Compact UI: 12px base font, all component sizes scaled proportionally.

---

## 15) Documentation and API reference (2026-03-20)

- **15.a** `planp/docs/api_reference.md` — comprehensive API documentation with examples for all 68 endpoints.
- **15.b** `planp/db_schema_snapshot.md` — complete database schema documentation with all 17 tables.
- **15.c** GUID resolution strategy documented (concept_guid as universal anchor).
- **15.d** Documentation browser UI at `/docs` with download links.
- **15.e** API endpoint for document listing and download: `GET /api/v1/docs`, `GET /api/v1/docs/<filename>`.
- **15.f** All project documentation updated to reflect current codebase state.

---

## Architecture note: AUTH_DISABLED mode

Local development runs with `AUTH_DISABLED=true` in `.env`. All API endpoints and web routes work without login/JWT tokens. The auth code remains in place and is tested with `AUTH_DISABLED=false` in the test suite. Production deployment on the Mac Mini will use SSO (to be integrated later).

---

## Test summary (2026-03-19T14-22-21Z)

**36 unit tests — 36 passed, 0 failed**

Results stored in:
- `./results/2026-03-19T12-47-31Z_results/` (initial run)
- `./results/2026-03-19T14-22-21Z_results/` (after Docker + auth-disabled changes)

**Integration test against live PostgreSQL + Docker — ALL PASSED**
Results stored in `./results/2026-03-19T14-22-21Z_results/integration_test.txt`

### Completed steps (1–15)

Steps 1 through 15 are complete. Docker stack runs on ports 9030 (app) and 9031 (db). All 17 database tables created. Bootstrap superuser available. All 68 API endpoints functional. Complete web UI with 32 templates. Documentation browser with download capability.

### Pending items

- 16: Server deployment preparation (nginx reverse proxy, Mac Mini)
- 17: SSO integration (to replace AUTH_DISABLED mode)
- 18: Final validation and sign-off

---

## 2026-04-11 — Snapshot goal enrichment (local edit, not deployed)

Edited `planp/app/api/plandefinitions.py :: _plandef_full_dict()` so
the `plan_definition_snapshot` JSON column stamped into every
ServiceRequest carries `goal_guid` / `goal_concept_guid` /
`goal_concept_name` on each activity dict and each transaction dict.
Today, with single-goal plans, values are filled in via inference:
if `len(snapshot.goals) == 1`, that goal is applied to every
activity/transaction unless they already have one.

**Why this matters.** Gateway's contract-scope validator compares
each observation's `concept_guid` against the contract's
`return_scope` (obligatory/optional). For CGM that scope authorizes
the *measurement* concept B-glucos (`1c34a590-...`), not the procedure
concept CGM (`22d0f6c6-...`). Gateway needs a way to look up the
"measurement concept this observation is reporting against", which is
the Goal's concept — hence the enrichment.

**Why not deployed yet.** `request.pdhc/gateway/app/services/context_service.py`
already has the same single-goal fallback (deployed earlier today), so
every active SR on miserver currently picks up the right goal concept
even without this plan.pdhc redeploy. Ship this on the next plan.pdhc
release or whenever we need to support multi-goal plans (which will
need an explicit activity→goal FK in the plan model, not just
inference).

## 2026-04-28 — Service-key auth path + 58-concept diabetes set loaded

Driven by sim.pdhc's multi-CDR seed. Two changes shipped to plan.pdhc
production (image rebuild via docker-compose, db volume preserved):

1. `requires_role` accepts an `X-Source-Service` + `X-Service-Key`
   header pair as an alternative to the SSO blob, mapped through a
   new `KNOWN_SERVICES` dict (`loader.pdhc` → `PLAN_LOADER_SERVICE_KEY`,
   `sim.pdhc` → `SIM_PDHC_SERVICE_KEY`). Falls through to existing SSO
   flow if headers absent. Backwards compatible.
2. 58 diabetes Concepts loaded via the new bulk-loader (`sim.pdhc/
   concepts/load_to_plan.py`) using `loader.pdhc` service-key. Plus 1
   added later via API: `inpatient_admit` (SNOMED 32485007). The
   loader auto-created `ATC` canonical_lib + `Medication`
   concept_type which were missing.

Concept registry went from 12 (mostly draft test items) to 71. Browse
via `/api/v1/concepts?per_page=200` (public). The diabetes set covers
~55 distinct clinical variables across observations / diagnoses /
medications / procedures / encounters.

Known follow-up (post_seed_followups.md Block A): plan.pdhc's default
`200/min` limiter triggered HTTP 429s under the parallel canonicaliser
warmup — cdr.pdhc PlanClient mis-treats this as plan_miss and fails
the FHIR write with 422. Needs both a separate higher-tier service-
key limit on plan.pdhc AND a 429-aware retry on the cdr side.

---

## 2026-05-22: Concept catalogue bulk importer (ticket #134)

Provider integration guide vers2 Phase 2–3: a new provider submits a
single .xlsx of concepts to plan.pdhc on onboarding. We needed an
idempotent importer that reports accepted/rejected.

Added:
- `app/services/concept_importer.py` — pure logic: xlsx/csv parser +
  upsert engine. FK fields (`canonical_lib`, `concept_type`,
  `response_type`, `unit`) resolve by human name or GUID.
  `canonical_lib` + `canonical_ref` are append-only identity fields —
  changing either on an existing concept is reported as a conflict
  rather than silently overwritten.
- `POST /api/v1/concepts/import` (admin-only, multipart, returns 207
  on partial success).
- `flask import-concepts <path> [--dry-run] [--json-out]` CLI.
- `/concepts/import` web UI for SU admins.
- `tests/test_concept_import.py` — 8 tests cover happy path,
  idempotent re-import, identity-conflict rejection, range_low > high,
  invalid concept_name, unknown canonical_lib, dry-run rollback, and
  missing-header parse error.
- `docs/concept_import.md` — column spec + response shape.
- `openpyxl>=3.1` added to requirements.txt.

All 8 importer tests pass. Pre-existing failure in
`tests/test_concepts.py::test_create_and_read` (cached stale path)
is unrelated.

## 2026-06-22 — FHIR R5 terminology profile (instruction §4 + §5 + §6.5/§6.6 foundation)

Implementation kicked off per `plan_pdhc_fhir_terminology_profile_instruction.md`
in the parent repo dir. Decision record locked at
`plan_pdhc_fhir_terminology_profile_DECISIONS.md`.

### §4 Prerequisites (now green)

- Audit of 76 pre-existing tests: 22 were red from a stale URL prefix
  (commit `00440b7` moved CRUD blueprints under `/api/v1/lookup/...`
  but tests stayed at `/api/v1/...`). Fixed across `test_auth.py`,
  `test_concepts.py`, `test_lookup_tables.py`, `test_valuesets.py`.
- `test_health_returns_ok` updated to assert the CLAUDE.md §10 canonical
  shape (`status`/`database`/`service`/`version`) instead of the old
  `{'status':'ok'}`.
- Latent flake in `_setup_concept_deps` (CPython recycled
  `id(client)` → duplicate lib_name → 409) fixed to `uuid.uuid4()`.
- New `tests/test_capability.py` — 6 tests: pins `/metadata`,
  `/capability-statement`, `/endpoints` and a CDR cross-service
  `$validate-code` contract mirroring
  `cdr.pdhc/cdr_app/app/services/plan_client.py::PlanClient._parse_parameters`.

### §5 ADR — all five decisions APPROVED 2026-06-22

- **D1**: local CodeSystem code = `Concept.guid` (HARD-reversibility).
- **D2**: single CodeSystem `plan-pdhc-local`.
- **D3**: routes stay at `/api/v1/...`; canonical `url` =
  `{PLAN_BASE}/fhir/{Resource}/{id}` (identifier, may not resolve).
  D3.b: `/api/v1/ValueSet?url=...` accepts both new and legacy forms
  during transition.
- **D4**: `version = str(vers_number)`, per-resource.
- **D5**: two-layer validator — `fhir.resources>=8.0` in `pytest` for
  fast shape-check; HL7 Java `validator_cli.jar` via `make conformance`
  for canonical conformance (CI wiring TBD).

### §6.5 + §6.6 foundation (this commit)

- `app/models/concept_models.py`: added `LOCAL_CODESYSTEM_ID`,
  `fhir_canonical_url(resource, id)`, and `fhir_version(model_obj)`
  next to `PLAN_BASE`. Single source of truth for the FHIR canonical
  URL form (ADR D3, Risk §9.3).
- `app/api/fhir_helpers.py` (new): shared `operation_outcome()`,
  `parameters_response()`, `fhir_json_response()`,
  `parse_parameters_body()`. `FHIR_CONTENT_TYPE = 'application/fhir+json'`.
- `app/api/terminology.py` left untouched (existing private helpers
  preserved for backward compat per spec §6.5 "do not retrofit").
- `requirements.txt`: added `fhir.resources>=8.0`.
- `tests/test_fhir_helpers.py` (new): 20 tests covering the URL
  builder, version helper, all four shared helpers, the D5 fast
  validator wiring (round-trip through `fhir.resources` pydantic
  models), and the D3 lint — forbids any file other than the URL
  helper from hardcoding `plan.pdhc.se/fhir/` or `{PLAN_BASE}/fhir/`
  patterns.

Test count: 76 → 102 (+26: 6 capability, 20 fhir_helpers).
All green; 3 consecutive full-suite runs no flakes.

### §6.1 — ValueSet resource + $expand

- `app/api/fhir_valueset.py` (NEW): four routes registered at `/api/v1`:
  - `GET /ValueSet/{guid}` → FHIR R5 ValueSet (url, version, status,
    compose, optional title/description).
  - `GET /ValueSet?url=&_count=&_offset=` → searchset Bundle. `?url=`
    accepts the new canonical form AND the legacy
    `/api/v1/(lookup/)?valuesets/{guid}` forms per D3.b transition rule.
  - `GET /ValueSet/{guid}/$expand` → expansion.contains[] (one entry
    per `(system, code, display)` resolved from
    `ValueSetValue → ValueCatalog → CanonicalLib.canonical_lib_url`).
  - `POST /ValueSet/$expand` with `Parameters` body (`url` or
    `valueSet` parameter; falls back gracefully when both forms supplied).
- All four routes emit `application/fhir+json` and return FHIR
  `OperationOutcome` on errors (400 invalid guid, 404 not found,
  required-parameter missing).
- All output validates against `fhir.resources` R5 pydantic models
  (D5 fast layer).
- ValueSet model unchanged. `ValueSet.to_dict()` (legacy CRUD JSON)
  unchanged. Existing test_valuesets.py membership/CRUD tests still
  pass (§2 regression contract held).
- `tests/test_fhir_valueset.py` (NEW): 22 tests across read/search/
  $expand-GET/$expand-POST/legacy-regression, including D3 canonical
  url pin, D3.b legacy-url acceptance, D5 fast-layer validation.

Test count: 102 → 124 (+22 fhir_valueset).
All green; 5 consecutive full-suite runs no flakes.

### §6.2 — scoped `$validate-code` (keeping the cdr.pdhc shim contract)

Strategy per spec §6.2: the existing global behavior at
`/api/v1/ValueSet/$validate-code` (no url, system+code only) is
unchanged. When the caller supplies a `url` / `valueSet` identifier,
the same route delegates to scoped logic in `fhir_valueset.py`. Two
new dedicated scoped routes also added.

- `app/api/fhir_valueset.py`:
  - `scoped_validate_code(vs, system, code)` public helper — checks
    membership in `vs`'s expansion; `system` may be the CanonicalLib
    URL (FHIR-canonical) OR name (cdr.pdhc form); empty system →
    match by code alone.
  - `resolve_canonical_lib(system_or_url)` — tries URL then name.
  - `GET /api/v1/ValueSet/{guid}/$validate-code?system=&code=` (+
    `%24` escape variant).
  - `POST /api/v1/ValueSet/$validate-code` with Parameters body
    (`url`/`valueSet` + `code` + `system`).
- `app/api/terminology.py`: `validate_code()` adds a branch at the
  top — if `url`/`valueSet` query param present, dispatch to
  `scoped_validate_code` via local import (no startup-time cycle).
  Bare `?system=&code=` path is **byte-identical** to before, so the
  cdr.pdhc shim contract is preserved.
- `tests/test_fhir_valueset.py` extended: +18 §6.2 tests across
  `TestScopedValidateCodeByGuid` (8), `TestScopedValidateCodeByUrl` (5),
  `TestScopedValidateCodeByPost` (3), `TestCDRGlobalContractAfter62` (2
  — re-pinning the exact cdr.pdhc request shape after the new branch).
  D5 round-trip via `fhir.resources.parameters.Parameters` model on
  the scoped responses.

Test count: 124 → 142 (+18 §6.2).
All green; 5 consecutive full-suite runs no flakes.
Existing `test_terminology.py` (global $validate-code, 21 tests) +
`test_capability.py::TestCDRValidateCodeContract` (3 tests) re-verified
green — the cdr.pdhc cross-service contract from §4.2 holds after §6.2.

### §6.4 — ConceptMap + $translate (the highest-value item)

The single platform ConceptMap maps every Concept row's
canonical_lib + canonical_refnumber binding into a FHIR R5 ConceptMap
keyed `plan-pdhc-canonical-bindings`. Source = local CodeSystem
`plan-pdhc-local` (ADR D2). Targets = each registered CanonicalLib's
URL. element.code = `Concept.guid` (ADR D1). Relationship = `equivalent`.

- `app/models/concept_models.py`: added
  `LOCAL_CONCEPTMAP_ID = "plan-pdhc-canonical-bindings"`.
- `app/api/fhir_conceptmap.py` (NEW): 4 routes at `/api/v1`:
  - `GET /ConceptMap/{id}` — read the single ConceptMap.
  - `GET /ConceptMap[?url=]` — searchset Bundle of size 0 or 1.
  - `GET /ConceptMap/$translate?system=&code=&targetsystem=` (+
    `%24` escape).
  - `POST /ConceptMap/$translate` with Parameters body.
- $translate is **bidirectional**:
  - When `system` == local CodeSystem URL, source code is a
    `Concept.guid` and target is the canonical binding (filtered by
    `targetsystem` if present).
  - When `system` is a CanonicalLib URL OR name (cdr.pdhc-friendly
    lenience), source code is a `canonical_refnumber` and target is
    the local Concept; `targetsystem`, if present, must equal the
    local CodeSystem URL.
- Risk §9.5 — `match` is shaped as a repeating FHIR Parameters part,
  never collapsed to a singleton. Two dedicated invariant tests pin
  this (zero-match shape + one-match shape).
- `tests/test_fhir_conceptmap.py` (NEW): 27 tests across read (7),
  search (3), local→canonical (5), canonical→local (5), POST (3),
  error paths (2), match-array invariant (2). D5 round-trip
  validation on ConceptMap, Bundle, and Parameters.

Test count: 142 → 169 (+27 §6.4).
All green; 5 consecutive full-suite runs no flakes.

### §6.3 — CodeSystem + $lookup with termbank delegation

The local concept set is now published as the single CodeSystem
`plan-pdhc-local` (ADR D2). Every entry uses `Concept.guid` as the
code (ADR D1) paired with `concept_display_text` as `display` and
`concept_explain` as `definition`. The CanonicalLib binding is
surfaced as `concept[].property` (`canonical-lib` + `canonical-ref`),
with property definitions declared at the top of the resource.

- `app/api/fhir_codesystem.py` (NEW). 4 routes at `/api/v1`:
  - `GET /CodeSystem/{id}` — read the singleton local CodeSystem
    with `content: 'complete'` (small platform; revisit if N>>10k).
  - `GET /CodeSystem[?url=]` — searchset Bundle of size 0 or 1.
  - `GET /CodeSystem/$lookup?system=&code=` (+ `%24` escape).
  - `POST /CodeSystem/$lookup` with Parameters body.
- `$lookup` is a two-branch facade:
  - When `system` matches `LOCAL_CS_URL`, look up Concept by guid
    and return Parameters with name/version/display/definition +
    canonical-lib / canonical-ref / status properties.
  - Otherwise resolve `system` as a CanonicalLib (URL OR name,
    consistent with $validate-code and $translate) and delegate to
    `app.termbank_client.lookup(lib.canonical_lib_name, code)` —
    the existing TTL-cached client that also backs
    `/api/v1/termbank/concept/...`. Pass-through return on hit;
    OperationOutcome 404 on miss (text mentions "unreachable" so the
    cdr.pdhc-style callers see the transient hint).
  - Unregistered `system` returns 404 **without calling termbank**.
- `tests/test_fhir_codesystem.py` (NEW): 20 tests across read (5
  — D1 guid-as-code, display, property, R5 validation), search
  Bundle (3), local $lookup (5), termbank-delegation (4 — URL form,
  name form, miss-with-unreachable-hint, unregistered-skips-termbank),
  POST (3). Termbank delegation tested via `patch.object` on
  `app.termbank_client.lookup` — no live network.

Test count: 169 → 189 (+20 §6.3).
All green; 5 consecutive full-suite runs no flakes.

### §6.7 + §6.8 — CapabilityStatement truth-up + conformance scaffolding

- `app/api/capability.py`:
  - **ENDPOINTS** list extended with all 15 new FHIR routes (ValueSet,
    CodeSystem, ConceptMap reads/searches/operations). PlanDefinition
    `$expand` description now explicitly says "NOT the FHIR ValueSet
    $expand — see /ValueSet/<guid>/$expand below" so future readers
    can't conflate the two.
  - **ValueSet** resource entry rewritten: declares both surfaces (the
    legacy CRUD AND the FHIR routes), `?url=` searchParam with D3.b
    note, `$expand` and `$validate-code` operations. `$validate-code`
    documentation explicitly calls out the global cdr.pdhc shim mode
    vs the new scoped mode.
  - **CodeSystem** resource entry rewritten: describes the single
    local CodeSystem `plan-pdhc-local` (ADR D2) with `Concept.guid` as
    code (ADR D1). `$lookup` operation calls out the termbank
    delegation rule.
  - **ConceptMap** resource entry added: single platform
    `plan-pdhc-canonical-bindings`, `$translate` operation,
    bidirectional, Risk §9.5 match-shape note.
  - **§7 explicit non-goals** declared as an OperationDefinition
    documentation block — `$subsumes`, is-a / descendant filters, and
    hierarchical properties are all named as deliberately unsupported.
- `tests/test_capability.py` extended with 6 §6.7 assertions: ValueSet
  declares expand+validate-code (with cdr.pdhc+scoped doc-strings);
  CodeSystem declares lookup with termbank-delegation doc; ConceptMap
  exists with translate; §7 non-goals are documented; new FHIR routes
  appear in `/endpoints`; PlanDefinition `$expand` doc warns it isn't
  terminology.
- `Makefile` (NEW): `make test`, `make corpus`, `make conformance`,
  `make check-jar`. `conformance` is the HL7 Java validator path
  (`VALIDATOR_JAR` env var); `corpus` emits the corpus into
  `tests/fhir_corpus/`. The Java jar is NOT vendored — `check-jar`
  tells the operator where to download it.
- `tests/conformance_corpus_emit.py` (NEW): boots a self-contained
  test app, seeds the minimum, calls every new §6 endpoint, and
  writes JSON files. End-to-end-tested in this session — 13 files
  emitted cleanly.
- `tests/fhir_corpus/README.md` (NEW): how to run conformance, where
  to download the jar, two-layer validation rationale.

§6.8 fast layer (`fhir.resources` pydantic R5 models) was wired
across §6.1-§6.4 test files as those landed. §6.8 slow layer (Java
`validator_cli.jar`) is scaffolded but the JAR download + CI job is
the "TBD devops" item called out in Risk §9.4.

Test count: 189 → 195 (+6 §6.7).
All green; 5 consecutive full-suite runs no flakes.

---

## §6 IMPLEMENTATION COMPLETE.

All seven work items shipped:
- §6.1 ValueSet + $expand (22 tests)
- §6.2 scoped $validate-code (18 tests)
- §6.3 CodeSystem + $lookup with termbank delegation (20 tests)
- §6.4 ConceptMap + $translate (27 tests)
- §6.5 cross-cutting I/O conventions (in fhir_helpers.py, 18 tests)
- §6.6 canonical URLs + versioning (2 fields in concept_models.py)
- §6.7 CapabilityStatement truth-up (6 tests)
- §6.8 fast layer (D5 fhir.resources, exercised in every §6.x test);
  slow layer scaffolded (Makefile + corpus emitter)

Plus prerequisites:
- §4 Prerequisites — 22-test URL fix + capability/CDR contract pin
- §5 ADR (all five decisions approved 2026-06-22)

Total tests: 76 → 195 (+119). Green-baseline stable across all 5
consecutive full-suite runs. §2 regression contract (DO NOT BREAK)
holds: cdr.pdhc plan_client global `$validate-code` shape is
identical, verified by `TestCDRValidateCodeContract` (§4) and
`TestCDRGlobalContractAfter62` (§6.2 explicit pin).

**Outstanding** (not blocking ship):
1. CI job that runs `make conformance` against PRs (Risk §9.4
   long-tail).
2. The 3 open questions at the bottom of the DECISIONS ADR
   (CodeSystem.property URI scheme, ConceptMap multi-group future,
   POST validate-code body shape if external consumers ask) — none
   block §6 deployment.

### Documentation review 2026-06-22

Audited every doc in the repo for §6-staleness; fixed the following:

- `plan_pdhc_fhir_terminology_profile_instruction.md` — status line
  updated from "Specification for implementation. Nothing here is
  built yet." → "**IMPLEMENTED 2026-06-22.** All §6 work items
  shipped..."
- `readme.md` — added a bullet describing the new FHIR R5 terminology
  profile (with links to spec + ADR).
- `planp/docs/api_reference.md` — TWO categories of fix:
  (a) the same stale URL-prefix bug we caught in tests was in here
      too: 44 substitutions across canonical-libs/concept-types/
      response-types/units/plandef-types/intended-uses/valuesets/
      values from `/api/v1/X` → `/api/v1/lookup/X`. Same root cause
      as the tests (commit `00440b7` moved blueprint but didn't
      update either tests or docs).
  (b) added a new top-level "FHIR R5 Terminology Profile" section
      (~140 lines) covering ValueSet/CodeSystem/ConceptMap routes,
      $expand/$validate-code/$lookup/$translate, D3 canonical URL
      convention, D3.b legacy URL transition rule, termbank
      delegation rule, dual-mode $validate-code, explicit §7
      non-goals, and the conformance toolchain. Added a forward-link
      callout in the existing ValueSets section. Added a "NOT the
      FHIR ValueSet $expand" warning on the PlanDefinition $expand
      doc to prevent future confusion.
- `plan_description.md` — added a new "§9 FHIR R5 terminology profile"
  section + listed the four new modules in the source-files preamble.
- `DEPLOYMENT_PLAN.md` — added `Flask-Cors`, `openpyxl`,
  `fhir.resources>=8.0` to the requirements example block (was
  missing the latest two from previous landings as well as the new
  one), plus an upgrade callout for existing deployments.
- `newtask.txt` (NEW) — Rule 2 required this file; it didn't exist.
  Captures current focus (§6 done) and the next-up triage list.
- `app/api/capability.py` `DOCS_CATALOG` — registered both the spec
  and the ADR so `/api/v1/docs` and `/api/v1/docs/{name}` find them.
  Verified end-to-end (`Docs found: 11; both new docs FOUND`).

Test count unchanged (docs only): 195. All green; 3 consecutive
post-doc runs no flakes.

### Deploy to miserver 2026-06-22T12:24Z

Tarball-based deploy (30 files) followed by `docker-compose build app`
and `docker-compose up -d app` swap. ~5s outage. All five new FHIR
routes verified 200 externally via Cloudflare; cdr.pdhc `$validate-code`
contract shape byte-identical to pre-deploy.

Full log with what-was-NOT-done section:
[`DEPLOY_2026-06-22_FHIR_TERMINOLOGY.md`](DEPLOY_2026-06-22_FHIR_TERMINOLOGY.md).

## 2026-06-23 — post-deploy work (conformance fixes + CI + ADR D6-D8 + reconciliation + forms tests)

After the 2026-06-22 §6 deploy, six more commits landed on `main`:

| Commit | What | Ticket |
|---|---|---|
| `bb52910` | **Conformance fixes**: bdl-18 self link on all 3 searchset Bundles, ConceptMap.sourceScope dropped (FHIR R5 requires it to reference a ValueSet, not a CodeSystem), FormDefinition removed from CapabilityStatement.rest.resource[] (not a real FHIR resource type), security.service simplified to text-only CodeableConcept. **Conformance run: 13/13 corpus files PASS, 0 errors.** Redeployed to miserver. | (in-session) |
| `090cc8b` | **CI conformance workflow** (`.github/workflows/conformance.yml`): triggers on push/PR to main + paths-filtered to terminology surface; caches `validator_cli.jar` v6.9.10; runs `make corpus && make conformance`. | #253 |
| `1710546` | **CI tilde-expansion fix**: dropped literal `~` from `VALIDATOR_JAR` env (Makefile default `$(HOME)/.local/share/fhir/...` works correctly). | (follow-up) |
| `ccbbf15` | **ADR D6/D7/D8 resolution**: locked the three deferred open questions. D6 wires `concept[].property.uri` as `{LOCAL_CS_URL}#{property-code}` (canonical-lib / canonical-ref / status). D7 confirmed multi-group ConceptMap. D8 confirmed POST $validate-code body shape. Redeployed; URIs visible at `https://plan.pdhc.se/api/v1/CodeSystem/plan-pdhc-local`. | #256 |
| `57b239d` | **3 prod-only edits reconciled** into the canonical source: PlanDefinition archived-filter in `/api/v1/plandefinitions`; `to_dict()` exposes the `archived` boolean on PlanDefinition; pdhc_db port mapping changed from `9031:5432` (binds 0.0.0.0) to `127.0.0.1:9031:5432` (CLAUDE.md §3 loopback). | #254 |
| `f57020b` | **Characterization tests** for `/api/v1/forms*` and `/form-definitions*` — orthogonal to §6 but in §2's DO-NOT-BREAK list. 22 tests pinning auth gates + broad response shape across 8 forms routes + 10 form-definitions routes. Suite 195 → 217. | #255 |

Tests across this work: 195 → 217. CI gated on conformance going forward. All
six commits deployed via the same tarball+`docker-compose build`+`up -d` swap
pattern as the 2026-06-22 ship.


## 2026-06-24 — /api/v1/docs serving fix (ticket #273)

User-facing symptom: `GET /api/v1/docs` listed only 2 of 12 cataloged
documents; `GET /api/v1/docs/<filename>` returned 404 for the missing 10.

Root cause: two compounding bugs.

1. **Dockerfile build context was too narrow.** `COPY docs/ ./docs/`
   only covered the 4 files inside `planp/docs/`. The other 10
   cataloged docs live at the **repo root** (`progress.md`,
   `top_rules.md`, `plan_pdhc_fhir_terminology_profile_*.md`, …),
   outside the build context.
2. **Intended fallback — the `../:/project-docs:ro` volume mount in
   `docker-compose.yml` — silently failed in prod.** Confirmed live on
   miserver: the bind mount sources `/usr/local/www/plan.pdhc` (which
   exists, populated with the .md files), but Colima's `default`
   profile only virtiofs-mounts `/Users/miserver` — `/usr/local/www`
   is invisible inside the VM, so the bind mount destination is
   empty inside the container.

Fix (Option C from the audit options I surfaced): bake the docs into
the image. Concretely:

- `planp/docker-compose.yml`: `context: .` → `context: ..`,
  `dockerfile: Dockerfile` → `dockerfile: planp/Dockerfile`. Dropped
  the now-redundant `../:/project-docs:ro` volume.
- `planp/Dockerfile`: prefixed existing COPYs with `planp/`; added an
  explicit `COPY <root-docs…> ./docs/` block listing the 10 root
  docs by name (no glob — a stray root-level .md will NOT silently end
  up in the image); plus a `COPY readme.md ./docs/readme.md` for the
  case-mismatch between `README.md` (Git tracked) and the lowercase
  on-disk variant on miserver.
- `.dockerignore` (new at repo root): keeps the build context small
  now that it covers the whole repo — excludes `venv/`,
  `node_modules/`, `.git/`, `db_backups/`, `*.docx`, `*.pdf`, secrets,
  IDE/macOS noise, etc.
- `planp/app/routes/main.py`: deduplicated the second `DOCS_CATALOG`
  dict here (was drifting — referenced sso_* docs that the API
  catalog didn't, and missed the two terminology-profile docs the API
  catalog adds) by importing the single source of truth from
  `app/api/capability.py`. Same dict serves both the `/docs/` UI and
  `/api/v1/docs` API.

Live verification post-deploy: 12/12 cataloged docs serve `200` on
`https://plan.pdhc.se/api/v1/docs/<filename>`, and the docs index lists
all 12. Tagged the prior image as `planp-app:rollback` before rebuild
for fast revert.

---

## 2026-06-30 — rollup #325 surgical pass

Audit-driven hardening pass triggered by `Divergencies_code_vs_docs.md` (2026-06-30). Nine surgical tickets from rollup #325 landed in one session; seven design-flavoured tickets (#326 #328 #331 #332 #334 #336 #338) are deferred until the user makes the design choices.

Test suite: 222 → **225 passed** in 1.75s (3 new tests). No regressions.

### #335 — Delete or relocate orphan `planp/agentation-loader.jsx` — DONE — Relocated to `planp/app/static/src/agentation-loader.jsx` (it imports `agentation` from package.json deps, so it's the legitimate source of `static/js/agentation.bundle.js`). Added `static/src/BUILD.md` with the esbuild rebuild command.
### #333 — Delete `POST /api/v1/PlanDefinition` 501 stub — DONE — Handler at `fhir_plandefinitions.py:86-92` removed; test updated to assert 405 (Flask's default for unbound method on registered route).
### #327 — Delete dead JWT machinery — DONE — Dropped JWT_* config keys, `JWTManager` import/init, `Flask-JWT-Extended` dep, `JWT_SECRET_KEY` from `.env.example`. App boots clean; all 225 tests pass.
### #329 — Fix `/api/v1/lookup` serializer URLs — DONE — `ValueSet.to_dict` (line 245) and `Concept.to_dict.valueset_url` (line 380) now emit `/api/v1/lookup/valuesets/{guid}`. New test file `test_lookup_url_consistency.py` covers both.
### #330 — `Concept.update_concept` should bump `date_valid` — DONE — Added `concept.date_valid = datetime.now(timezone.utc)` before commit. New `test_update_bumps_date_valid` (1.05s sleep + strict-greater assertion) added to `test_concepts.py::TestConceptCRUD`.
### #337 — Fix `SSO_CALLBACK_URL` default + add SSO_* vars to `.env.example` — DONE — `config.py:30` default now `http://localhost:9030/api/v1/auth/callback`. `.env.example` gained SSO_BASE_URL/SSO_CLIENT_ID/SSO_CLIENT_SECRET/SSO_CALLBACK_URL block with note that `AUTH_DISABLED=true` skips SSO entirely for local dev.
### #339 — Fix `README.md` "Running locally" — DONE — Three-step `./start.sh`-based flow; new "How loopback-only exposure works" paragraph explains the compose port map is the gate, not the gunicorn flag.
### #340 — Update FHIR deploy doc + broaden conformance `paths:` filter + drop "no automated tests" framing — DONE — `DEPLOY_2026-06-22_FHIR_TERMINOLOGY.md` items #2/#3 marked RESOLVED 2026-06-23; `.github/workflows/conformance.yml` `paths:` broadened to include `fhir_service.py` + `app/__init__.py` for both `push:` and `pull_request:`; FHIR instruction §2 and §4 updated to cite the live 222-test suite.
### #341 — Add a pytest CI job — DONE — `.github/workflows/test.yml` runs `pytest tests -x -q --maxfail=3` on every push + PR. Python 3.14, pip-cached, 10-min timeout.

### Not yet closed in ticket queue
Each child ticket is still open on `ticket.mitidbok.se` so the operator can manually `/respond` (which auto-closes) after a code review. No `/respond` was posted automatically.

## 2026-06-30 — rollup #325 design pass

Follow-on session — the 7 design-flavoured tickets the surgical pass deferred. User made 4 explicit design choices via AskUserQuestion before this pass ran:

| Ticket | User decision |
|--------|---------------|
| #328 rate-limit | Global default + exempt the free routes |
| #331 D4 carve-out | Lift both CodeSystem + ConceptMap to fhir_version() |
| #332 PlanDef URL | Hard cutover to {PLAN_BASE}/fhir/PlanDefinition/<id> |
| #338 doc rewrite | Rewrite in place + drop DEPLOYMENT_PLAN from /api/v1/docs |

Test suite: 225 → **244 passed** (19 new tests across the 7 tickets). No regressions.

### #328 — Rate-limit redesign: RATELIMIT_DEFAULT + exempt — DONE — `Limiter(default_limits=['200/minute'])` in `app/__init__.py`; `RATELIMIT_DEFAULT` set; `@limiter.exempt` on `/api/health` + `/capability-statement` + `/metadata` + `/endpoints`; service-key callers globally exempted via `@limiter.request_filter`. Eight blueprint-level `limiter.limit("200/minute")(<bp>)` no-ops removed across `auth.py`, `capability.py`, `dispatch.py`, `form_definitions.py`, `forms.py`, `fhir_plandefinitions.py`, `plandefinitions.py`, `lookup_tables.py`, `concepts.py`. New `test_rate_limit.py` (3 tests) asserts 201st request returns 429 and exempt endpoints never 429.

### #326 — Capability rewrite — DONE — Auth block lists only the real GET routes + service-key bypass; rate-limit block reflects the actual 200/min + exempts; all lookup endpoints corrected to `/api/v1/lookup/...` prefix (the test surfaced ~40 endpoints had wrong paths!). New `test_capability_truth.py` (4 tests) walks every advertised endpoint and asserts it resolves to a real route via `app.url_map`.

### #331 — D4 carve-out: lift BOTH CodeSystem + ConceptMap to fhir_version() — DONE — Added `_codesystem_version()` (returns `str(max(Concept.vers_number))`) in `fhir_codesystem.py` and `_conceptmap_version()` (filtered to rows where `canonical_lib IS NOT NULL`) in `fhir_conceptmap.py`. Both replace hardcoded `'1'` on the read endpoint AND on the $lookup `version` reply. DECISIONS.md D4 "TBD" carve-out replaced with RESOLVED text. New `test_fhir_version_uniform.py` (6 tests) asserts version derives correctly and never empty.

### #332 — PlanDefinition canonical URL hard cutover — DONE — `fhir_service.py:31` and three more spots in `fhir_plandefinitions.py` (bundle `fullUrl`, bundle resource `url`, single-read `url`) all switched to `fhir_canonical_url('PlanDefinition', fhir_id)`. New `test_plandefinition_canonical_url.py` (3 tests) pins the new shape and asserts the legacy `pdhc.se/PlanDefinition/` form is no longer emitted.

### #334 — Drop legacy `/CarePlan/<guid>/dispatch` alias — DEFERRED — Gunicorn in `pdhc_app` is not configured with `--access-logfile`, so docker logs only capture migration + startup INFO. There is no way to count `/CarePlan/...` hits in the last 7 days without first enabling access logging on the production container. Per the ticket's stop rule the deprecated handler stays in place. Follow-up: enable gunicorn access logging in `entrypoint.sh` (add `--access-logfile -`), redeploy, wait ≥7 days, then revisit #334.

### #336 — DB-name docs sweep — DONE — Set `pdhc_gateway` as the default in `.env.example` and `config.py` (both with a comment explaining the legacy-name retention and pointing to memory `feedback_db_safety.md`); patched `planp/db_schema_snapshot.md`. `DEPLOYMENT_PLAN.md` + `SSO_INTEGRATION_PLAN.md` were rewritten under #338 and pick up `pdhc_gateway` there. The running database was NOT renamed.

### #338 — Rewrite-in-place + drop DEPLOYMENT_PLAN from /api/v1/docs — DONE —
- `DEPLOYMENT_PLAN.md`: 966 → ~140 lines. Container-based deploy model, SSO model, no JWT, no ghost scripts, no `_obs_gateway_repo`, `pdhc_gateway` DB name.
- `SSO_INTEGRATION_PLAN.md`: 223 → ~110 lines. H1-H4 handshake + per-request revalidation + service-key bypass. No `safe_restart.sh`/`server_deploy.sh`/JWT refresh.
- `plan_description.md` §6: key order corrected to match `services/fhir_service.py:19-30`.
- `plan_description.md` §7.1: SSO model + 200/min global default; no JWT login/refresh; no 10/min claim.
- `plan_description.md` §7.2: all paths under `/api/v1/lookup/` with explanatory note.
- `planp/docs/api_reference.md` lines 10-77: auth section rewritten (SSO redirect handshake, per-request revalidation, service-key bypass, ghost-route note); rate-limit block updated. The rest of `api_reference.md` was untouched.
- Confirmed `DEPLOYMENT_PLAN.md` is NOT in `DOCS_CATALOG` so it's already not served via `/api/v1/docs`. New `test_docs_serving.py` (3 tests) pins this contract.

### Not yet closed in ticket queue
Each child ticket (#326 #328 #331 #332 #336 #338) and the still-deferred #334 remain open on `ticket.mitidbok.se` so the operator can manually `/respond` (auto-closes) after reviewing the diff. No `/respond` was posted automatically.
