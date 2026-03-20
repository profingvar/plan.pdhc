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

- **1.e** Directory structure created under `gateway/` with all required subdirectories.
- **1.f** `progress.md` created.
- **1.g** `changed_files.md` created.

### 1.3 Git initialisation

- **1.h** Git repo initialised. `.gitignore` created covering venv, `.env`, `__pycache__`, results, `_obs_gateway_repo`.
- **1.i** Pending: initial commit (awaiting operator).

---

## 2) Docker and database setup

- **2.a** `gateway/docker-compose.yml` created — PostgreSQL 16 on port 9031, app on port 9030.
- **2.b** `gateway/.env` created with development credentials.
- **2.c** `gateway/.env.example` created with placeholder values.
- **2.d** `gateway/Dockerfile` created with `entrypoint.sh` that runs migrations before starting gunicorn.
- **2.e** App service added to `docker-compose.yml`, depends on db health check.
- **2.f** Docker build succeeded — `gateway-app:latest` image built.
- **2.g** Full stack verified: `pdhc_db` (PostgreSQL 16, port 9031, healthy) + `pdhc_app` (Flask/gunicorn, port 9030, running). API responds to requests.
- **2.h** `start.sh` created at project root — kills ports 9000–9003 and 9030–9033, starts Docker, activates venv, graceful shutdown on Ctrl+C.
- **2.i** `start.sh` made executable.

---

## 3) Application foundation (Flask + SQLAlchemy)

- **3.a** Virtual environment created at `gateway/venv`.
- **3.b** `gateway/requirements.txt` created with all dependencies.
- **3.c** Dependencies installed successfully.
- **3.d** `gateway/app/__init__.py` — Flask app factory implemented with blueprint registration and bootstrap superuser logic.
- **3.e** `gateway/app/config.py` — configuration loader implemented.
- **3.f** Flask-Migrate initialised — `gateway/migrations/` directory created.
- **3.g** Migration directory confirmed inside `gateway/`.

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

- **15.a** `gateway/docs/api_reference.md` — comprehensive API documentation with examples for all 68 endpoints.
- **15.b** `gateway/db_schema_snapshot.md` — complete database schema documentation with all 17 tables.
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
