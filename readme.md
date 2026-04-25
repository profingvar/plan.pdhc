# PDHC PlanDef Builder — Deployment Plan

This document is the authoritative deployment plan for the PDHC Gateway service. It covers every step from environment setup through a fully operational, FHIR R5-compliant application running in Docker on localhost (development) with a path to server deployment (Mac Mini). Numbering follows the `1.a, 1.b` convention required by Rule 3.

---

## 1) Environment and infrastructure setup

### 1.1 Prerequisites and tooling

- **1.a** Verify the development Mac has Docker Desktop installed and running. Confirm Docker Compose is available (`docker compose version`).
- **1.b** Verify Python 3.11+ is available on the host for local tooling and test execution.
- **1.c** Verify PostgreSQL client tools (`psql`) are available on the host for manual inspection.
- **1.d** Confirm ports 9030–9033 are free. Kill any processes on legacy ports 9000–9003.

### 1.2 Project directory structure

- **1.e** Create the application folder structure. All application code, venv, and database configuration live inside a dedicated subfolder (Rule 21). Target layout:

```
plan.pdhc/
├── top_rules.md                          # immutable project rules
├── plan_description.md                   # domain architecture reference
├── pdhc_markdown_layout_standard.md      # markdown style guide (Rule 24)
├── repo_css.md                           # frontend design system
├── readme.md                             # this deployment plan
├── progress.md                           # step-by-step progress log
├── changed_files.md                      # registry of all edited files
├── newtask.txt                           # debugging focus (created when needed)
├── start.sh                              # single entry-point script (Rule 16)
├── _obs_gateway_repo/                    # previous prototype (untouched, Rule 14)
├── results/                              # test output (Rule 11)
│   └── <ISO-8601>_results/
└── planp/                              # ← application root (Rule 21)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt                  # includes Flask-Limiter
    ├── entrypoint.sh                     # runs migrations then starts gunicorn
    ├── .env                              # secrets & config (Rule 23)
    ├── .env.example                      # template (committed)
    ├── db_schema_snapshot.md             # database schema documentation
    ├── venv/
    ├── docs/
    │   └── api_reference.md              # comprehensive API documentation
    ├── app/
    │   ├── __init__.py                   # Flask app factory + Flask-Limiter
    │   ├── config.py                     # incl. rate limit config
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user_models.py
    │   │   ├── concept_models.py
    │   │   ├── activity_models.py
    │   │   └── fhir_models.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── auth.py                   # login, logout, me, refresh + rate limiting
    │   │   ├── concepts.py               # concept CRUD + concept-values
    │   │   ├── lookup_tables.py          # generic CRUD for 6 lookup tables
    │   │   ├── fhir_plandefinitions.py   # FHIR R5 read/search/expand
    │   │   ├── plandefinitions.py        # full CRUD API for PlanDefinitions
    │   │   └── capability.py             # capability statement + docs API
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── main.py                   # dashboard + docs browser
    │   │   ├── concepts.py               # concept management UI
    │   │   ├── values.py                 # value CRUD UI
    │   │   ├── valuesets.py              # valueset CRUD + membership UI
    │   │   ├── lookup_tables.py          # lookup table CRUD UI
    │   │   └── plandefinitions.py        # builder + list/view/edit/delete/export
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── fhir_service.py
    │   │   └── name_uniqueness.py
    │   ├── static/
    │   │   └── css/
    │   │       └── pdhc.css              # design system (12px base)
    │   └── templates/                    # 32 templates
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── docs.html
    │       ├── concepts/                 # create, list, view
    │       ├── values/                   # create, edit, list, view
    │       ├── valuesets/                # create, edit, list, view
    │       ├── lookup/                   # 4 types × 4 templates
    │       └── plandefinitions/          # builder, list, view
    ├── migrations/
    │   └── versions/
    └── tests/
        ├── conftest.py
        ├── test_auth.py
        ├── test_concepts.py
        ├── test_lookup_tables.py
        ├── test_valuesets.py
        ├── test_plandefinitions.py
        └── test_fhir_endpoints.py
```

- **1.f** Create `progress.md` (empty template with header).
- **1.g** Create `changed_files.md` (empty template with header).

### 1.3 Git initialisation

- **1.h** Initialise a Git repository in `plan.pdhc/`. Add a `.gitignore` covering `venv/`, `__pycache__/`, `.env`, `.DS_Store`, `*.pyc`, `results/`, and `_obs_gateway_repo/` (Rule 14).
- **1.i** Make an initial commit with the three source documents and the newly created scaffolding files.

---

## 2) Docker and database setup

### 2.1 Port allocation (Rule 16)

All services use ports 9030–9033 exclusively:

| Port | Service              |
|------|----------------------|
| 9030 | Flask application    |
| 9031 | PostgreSQL database  |
| 9032 | Reserved             |
| 9033 | Reserved             |

### 2.2 PostgreSQL in Docker

- **2.a** Create `planp/docker-compose.yml` defining:
  - A `db` service running PostgreSQL 16, mapped to `localhost:9031`.
  - A named volume `pdhc_pgdata` for persistence.
  - Environment variables sourced from `planp/.env`.
- **2.b** Create `planp/.env` with at minimum:

```
POSTGRES_USER=pdhc_admin
POSTGRES_PASSWORD=<strong-generated-password>
POSTGRES_DB=pdhc_planp
DATABASE_URL=postgresql://pdhc_admin:<password>@localhost:9031/pdhc_planp
FLASK_SECRET_KEY=<generated>
JWT_SECRET_KEY=<generated>
BOOTSTRAP_SU_USERNAME=admin
BOOTSTRAP_SU_PASSWORD=<strong-generated-password>
FLASK_ENV=development
FLASK_PORT=9030
```

- **2.c** Create `planp/.env.example` with placeholder values (committed to Git).
- **2.d** Verify the database starts: `docker compose up db -d` and confirm connectivity via `psql -h localhost -p 9031 -U pdhc_admin -d pdhc_planp`.

### 2.3 Flask application container

- **2.e** Create `planp/Dockerfile`:
  - Base image `python:3.11-slim`.
  - Copy `requirements.txt`, install dependencies.
  - Copy application code.
  - Expose port 9030.
  - Entry point: `gunicorn` or `flask run` bound to `0.0.0.0:9030`.
- **2.f** Add the `app` service to `docker-compose.yml`:
  - Depends on `db`.
  - Maps `localhost:9030` to container port 9030.
  - Mounts `planp/.env`.
- **2.g** Verify the full stack starts: `docker compose up -d` — both `db` and `app` healthy.

### 2.4 The `start.sh` entry-point script (Rule 16)

- **2.h** Create `start.sh` at project root. The script must:
  1. Kill any processes on ports 9000–9003 (legacy cleanup).
  2. Kill any processes on ports 9030–9033 (previous run cleanup).
  3. Ensure Docker is running (check and start Docker Desktop if needed).
  4. Activate the Python virtual environment (`planp/venv`).
  5. Start the database and application via `docker compose up -d`.
  6. Tail logs.
  7. On `Ctrl+C`: `docker compose down`, deactivate venv, exit gracefully.
- **2.i** Make `start.sh` executable and test the full lifecycle (start, verify, Ctrl+C, confirm clean shutdown).

---

## 3) Application foundation (Flask + SQLAlchemy)

### 3.1 Virtual environment and dependencies

- **3.a** Create `planp/venv` via `python3 -m venv planp/venv`.
- **3.b** Create `planp/requirements.txt`:

```
Flask>=3.0
Flask-SQLAlchemy>=3.1
Flask-Migrate>=4.0
Flask-Login>=0.6
Flask-JWT-Extended>=4.6
Flask-Limiter>=3.5
psycopg2-binary>=2.9
gunicorn>=21.2
python-dotenv>=1.0
bleach>=6.1
pytest>=8.0
pytest-cov>=4.1
requests>=2.31
```

- **3.c** Install dependencies: `pip install -r planp/requirements.txt`.

### 3.2 Flask app factory

- **3.d** Implement `planp/app/__init__.py` — the application factory (`create_app()`):
  - Load configuration from `config.py` (reads `.env`).
  - Initialise SQLAlchemy, Flask-Migrate, Flask-Login, Flask-JWT-Extended.
  - Register API blueprints (prefix `/api/v1/`).
  - Register web UI route blueprints.
  - Register error handlers (JSON for API, HTML for web).
- **3.e** Implement `planp/app/config.py`:
  - `DATABASE_URL` from env.
  - `SECRET_KEY`, `JWT_SECRET_KEY` from env.
  - `FLASK_ENV`, debug flag.

### 3.3 Database migrations

- **3.f** Initialise Flask-Migrate: `flask db init`.
- **3.g** Confirm migration directory is created inside `planp/`.

### 3.4 Tests for foundation

- **3.h** Write `tests/test_app_factory.py`:
  - App creates without error.
  - Config values loaded correctly.
  - Database connection succeeds.
- **3.i** Run tests via pytest. Store results in `./results/<timestamp>_results/` (Rule 11).
- **3.j** Update `progress.md` with results of 3.h/3.i.

---

## 4) Data models

### 4.1 User and authentication models

- **4.a** Implement `planp/app/models/user_models.py`:
  - `User` model: `id`, `guid` (UUID), `username`, `email`, `password_hash`, `role` (`read_only`, `read_write`, `admin`), `is_active`, timestamps.
  - Password hashing via `werkzeug.security`.
  - Bootstrap superuser creation from `.env` variables (Rule 23).

### 4.2 Lookup table models

- **4.b** Implement in `planp/app/models/concept_models.py`:
  - `CanonicalLib` — `canonical_libs` table.
  - `ConceptType` — `concept_types` table.
  - `ResponseType` — `response_types` table.
  - `Unit` — `units` table.
  - `PlanDefType` — `plandef_types` table.
  - `IntendedUse` — `intended_uses` table.
  - All tables include: `id`, `guid` (UUID, unique), `<name>`, `<display_text>`, `author`, `vers_number`, `date_created`, `date_valid`.
  - `CanonicalLib` additionally has `canonical_lib_url`.

### 4.3 Values and ValueSets models

- **4.c** Add to `concept_models.py`:
  - `ValueCatalog` — `values_catalog` table: `guid`, `canonical_lib` (FK), `canonical_refnumber`, `value_name`, `value_display_text`, `value_explanation`, metadata.
  - `ValueSet` — `valuesets` table: `guid`, `canonical_lib` (FK), `canonical_refnumber`, `valueset_name`, `valueset_display_text`, `valueset_explanation`, metadata.
  - `ValueSetValue` — `valueset_values` junction: `valueset_guid` (FK), `value_guid` (FK), `sort_order`.

### 4.4 Concept model

- **4.d** Add `Concept` to `concept_models.py`:
  - Fields per `plan_description.md` section 2.5.
  - FKs to `canonical_libs`, `concept_types`, `response_types`, `units`, `valuesets`.
  - Check constraint: `range_low <= range_high` when both present.
  - `no_of_values_connected` integer field.
  - All internal references via GUID (Rule 18).

### 4.5 PlanDefinition and activity models

- **4.e** Implement `planp/app/models/fhir_models.py`:
  - `PlanDefinition` — `plan_definitions` table: `id`, `guid`, `fhir_id` (UUID string), metadata (title, name, description, status, type, version, publisher, purpose, usage, copyright, subject_type), contributor fields, timing fields, `goal` (JSON text), `action` (JSON text), `fhir_data` (JSONB), timestamps.
- **4.f** Implement `planp/app/models/activity_models.py`:
  - `Activity` — `activities` table: `id`, `guid`, title, description, performer_type, subject_type, timing fields, notes.
  - `Transaction` — `transactions` table: `id`, `guid`, `activity_guid` (FK), `concept_guid` (FK), expected_value, unit, min, max, requirement_type.
  - `PlanDefinitionGoal` — `plandefinition_goals` table: `id`, `guid`, `plandefinition_guid` (FK), `concept_guid`, `concept_name`, priority, target_type, target fields.
  - `PlanDefinitionActivity` — `plandefinition_activities` junction: `plandefinition_guid`, `activity_guid`, `sort_order`.

### 4.6 Migrations and tests

- **4.g** Generate migration: `flask db migrate -m "initial models"`.
- **4.h** Apply migration: `flask db upgrade`.
- **4.i** Write `tests/test_models.py`:
  - Each model can be instantiated and persisted.
  - FK constraints hold.
  - Check constraint on `range_low`/`range_high` enforced.
  - GUID uniqueness enforced.
- **4.j** Run tests. Store results. Update `progress.md`.

---

## 5) Authentication and authorisation

### 5.1 Auth API endpoints

- **5.a** Implement `planp/app/api/auth.py`:
  - `POST /api/v1/auth/login` — accepts username + password, returns JWT.
  - `POST /api/v1/auth/logout` — invalidates token (blocklist or short expiry).
  - `GET /api/v1/auth/me` — returns current user info.
- **5.b** Implement bootstrap superuser logic:
  - On first startup, if no users exist, create superuser from `BOOTSTRAP_SU_USERNAME` / `BOOTSTRAP_SU_PASSWORD` in `.env` (Rule 23).
  - Log the action; do not recreate if user already exists.

### 5.2 Role-based access control

- **5.c** Implement decorator/middleware for role checks:
  - `@requires_role('read_write')` for write operations.
  - `@requires_role('admin')` for user management.
  - Read-only endpoints require `read_only` or higher.

### 5.3 Tests

- **5.d** Write `tests/test_auth.py`:
  - Login with valid credentials returns JWT.
  - Login with invalid credentials returns 401.
  - Protected endpoint without token returns 401.
  - Protected endpoint with wrong role returns 403.
  - Bootstrap superuser created on first run.
- **5.e** Run tests. Store results. Update `progress.md`.

---

## 6) Lookup table CRUD

### 6.1 API endpoints

- **6.a** Implement `planp/app/api/lookup_tables.py` with full CRUD for each lookup table:
  - **Canonical libraries**: `GET/POST /api/v1/canonical-libs`, `GET/PUT/DELETE /api/v1/canonical-libs/<guid>`.
  - **Concept types**: `GET/POST /api/v1/concept-types`, `GET/PUT/DELETE /api/v1/concept-types/<guid>`.
  - **Response types**: `GET/POST /api/v1/response-types`, `GET/PUT/DELETE /api/v1/response-types/<guid>`.
  - **Units**: `GET/POST /api/v1/units`, `GET/PUT/DELETE /api/v1/units/<guid>`.
  - **PlanDef types**: `GET/POST /api/v1/plandef-types`, `GET/PUT/DELETE /api/v1/plandef-types/<guid>`.
  - **Intended uses**: `GET/POST /api/v1/intended-uses`, `GET/PUT/DELETE /api/v1/intended-uses/<guid>`.
- **6.b** All write endpoints require `read_write` role. All read endpoints require `read_only` or higher.
- **6.c** Input sanitisation on all string fields.
- **6.d** UUID validation on all GUID-referencing fields (Rule 18).

### 6.2 Tests

- **6.e** Write `tests/test_lookup_tables.py`:
  - CRUD cycle for each lookup table.
  - Duplicate name rejection.
  - Invalid UUID rejection.
  - Auth enforcement.
- **6.f** Run tests. Store results. Update `progress.md`.

---

## 7) Values and ValueSets CRUD

### 7.1 Values API

- **7.a** Implement values endpoints:
  - `GET /api/v1/values` — list/search, ordered by `value_name`.
  - `POST /api/v1/values` — create; requires `value_name`, `canonical_lib`.
  - `GET /api/v1/values/<guid>` — read single.
  - `PUT /api/v1/values/<guid>` — update.
  - `DELETE /api/v1/values/<guid>` — delete.
- **7.b** Name uniqueness: API auto-renames on import (`make_unique_value_name`); web UI rejects duplicates.

### 7.2 ValueSets API

- **7.c** Implement:
  - `GET /api/v1/valuesets` — list/search with pagination.
  - `POST /api/v1/valuesets` — create; requires `valueset_name`, `canonical_lib`.
  - `GET /api/v1/valuesets/<guid>` — read single.
  - `PUT /api/v1/valuesets/<guid>` — update.
  - `DELETE /api/v1/valuesets/<guid>` — delete.

### 7.3 ValueSet membership API

- **7.d** Implement:
  - `GET /api/v1/valuesets/<valueset_guid>/values` — list values in set with sort order.
  - `POST /api/v1/valuesets/<valueset_guid>/values` — add value; prevent duplicates; optional `sort_order`.
  - `DELETE /api/v1/valuesets/<valueset_guid>/values/<value_guid>` — remove value from set.

### 7.4 Tests

- **7.e** Write `tests/test_valuesets.py`:
  - CRUD cycle for values and valuesets.
  - Membership add/remove/list.
  - Duplicate membership prevention.
  - Sort order respected.
  - Auth enforcement.
- **7.f** Run tests. Store results. Update `progress.md`.

---

## 8) Concept CRUD

### 8.1 Concept API endpoints

- **8.a** Implement `planp/app/api/concepts.py`:
  - `GET /api/v1/concepts` — list with filtering (text search, concept_type, response_type, canonical_lib, has_values), pagination, deterministic sort by `concept_name` + `guid`.
  - `POST /api/v1/concepts` — create; requires `canonical_lib`, `concept_name`; validate UUID refs; sanitise strings; enforce name uniqueness.
  - `GET /api/v1/concepts/<guid>` — read with embedded ValueSet values if bound.
  - `PUT /api/v1/concepts/<guid>` — update; increment `vers_number`; revalidate refs.
  - `DELETE /api/v1/concepts/<guid>` — delete.

### 8.2 Concept-values endpoints (through ValueSet)

- **8.b** Implement:
  - `GET /api/v1/concepts/<concept_guid>/values` — returns values from bound ValueSet.
  - `POST /api/v1/concepts/<concept_guid>/values` — adds value to bound ValueSet; error if no ValueSet bound.
  - `DELETE /api/v1/concepts/<concept_guid>/values/<value_guid>` — removes from bound ValueSet.

### 8.3 Name uniqueness service

- **8.c** Implement `planp/app/services/name_uniqueness.py`:
  - `make_unique_concept_name(name)` — for API/import (auto-suffix).
  - `validate_name_for_manual_entry(name)` — for web UI (reject duplicates).
  - Same pattern for values and valuesets.

### 8.4 Tests

- **8.d** Write `tests/test_concepts.py`:
  - CRUD cycle.
  - Filtering and pagination.
  - ValueSet binding and concept-values endpoints.
  - Business rule: single-choice response type requires ValueSet.
  - Name uniqueness (auto-rename and rejection paths).
  - Auth enforcement.
- **8.e** Run tests. Store results. Update `progress.md`.

---

## 9) FHIR service and PlanDefinition serialization

### 9.1 FHIR serialization service

- **9.a** Implement `planp/app/services/fhir_service.py`:
  - `FHIRService.create_fhir_plandefinition(plandef)` — builds a FHIR R5 PlanDefinition JSON object per `plan_description.md` section 6.
  - Includes: `resourceType`, `id`, `meta`, `identifier`, `url`, `version`, `name`, `title`, `status`, `type`, `subjectCodeableConcept`, descriptive fields, date fields, contributors, `relatedArtifact`, `library`, `action`, `goal`.
  - Canonical codings (system + code) included when canonical library URL and ref number are available.
- **9.b** Validate output against FHIR R5 PlanDefinition structure (Rule 15).

### 9.2 Tests

- **9.c** Write `tests/test_fhir_service.py`:
  - Serialization produces valid FHIR structure.
  - Required fields present.
  - Canonical codings included when data available.
  - Default values applied correctly (`clinical-protocol`, `Patient`, `1.0.0`).
- **9.d** Run tests. Store results. Update `progress.md`.

---

## 10) PlanDefinition builder (web UI)

### 10.1 Web routes

- **10.a** Implement `planp/app/routes/plandefinitions.py`:
  - `GET /plandefinitions` — list page.
  - `GET /plandefinitions/builder` — builder UI; supports `?plandef_id=<fhir_id>` for edit mode.
  - `POST /plandefinitions/create` — save new PlanDefinition.
  - `GET /plandefinitions/<id>` — view page.
  - `POST /plandefinitions/<id>/edit` — update.
  - `POST /plandefinitions/<id>/delete` — delete.
  - `GET /plandefinitions/<id>/export` — download FHIR JSON.
- **10.b** Builder save flow must (per `plan_description.md` section 5.5):
  1. Validate metadata (title required, JSON valid).
  2. Derive name from title if empty; enforce uniqueness.
  3. Compute effective period from validity duration if provided.
  4. Create `plan_definitions` row.
  5. Persist goals relationally (`plandefinition_goals`).
  6. Persist activities + transactions relationally.
  7. Generate and store FHIR JSON via `FHIRService`.

### 10.2 Client-side builder

- **10.c** Implement `planp/app/static/js/plandef-builder.js`:
  - Concept selection with search.
  - Goal definition with numeric/range/categorical targets.
  - Activity definition with timing (once / repeat frequency).
  - Transaction definition per activity, tied to concepts.
  - JSON payload construction for POST.
- **10.d** All templates follow the PDHC markdown layout standard for documentation pages (Rule 24).

### 10.3 Tests

- **10.e** Write `tests/test_plandefinitions.py`:
  - Create PlanDefinition through builder POST — verify all relational rows created.
  - Edit PlanDefinition — verify relational rows updated.
  - Delete PlanDefinition — verify cascade cleanup.
  - FHIR JSON generated and stored.
  - Name uniqueness enforced.
  - Auth and role enforcement.
- **10.f** Run tests. Store results. Update `progress.md`.

---

## 11) FHIR PlanDefinition API endpoints

### 11.1 Read and search

- **11.a** Implement `planp/app/api/fhir_plandefinitions.py`:
  - `GET /api/v1/PlanDefinition` — FHIR searchset Bundle; supports `status`, `title`, `_count`, `_offset`.
  - `GET /api/v1/PlanDefinition/<id>` — returns stored `fhir_data`; enriches with `identifier`/`url` if missing.
  - `GET /api/v1/PlanDefinition/<id>/$expand` — forces regeneration for full nested structure.
- **11.b** `POST /api/v1/PlanDefinition` — returns 501 with instruction to use builder UI (current design per `plan_description.md` section 7.4).

### 11.2 FHIR compliance validation (Rule 15)

- **11.c** Validate that all FHIR endpoints return resources conformant to FHIR R5:
  - Correct `resourceType`.
  - Valid Bundle structure for search results.
  - Proper use of `meta`, `identifier`, `url`.

### 11.3 Tests

- **11.d** Write `tests/test_fhir_endpoints.py`:
  - Search returns valid Bundle.
  - Read returns valid PlanDefinition.
  - Expand regenerates fresh FHIR JSON.
  - 501 on POST.
  - Filtering by status and title works.
  - Pagination via `_count`/`_offset`.
- **11.e** Run tests. Store results. Update `progress.md`.

---

## 12) Comprehensive API endpoint test script (Rules 9 and 20)

- **12.a** Create `planp/tests/test_all_endpoints.py` — a single script exercising every API endpoint per the capability statement:
  - Auth endpoints (login, logout, me).
  - All lookup table CRUD endpoints.
  - Values and ValueSets CRUD + membership.
  - Concepts CRUD + concept-values.
  - FHIR PlanDefinition read/search/expand.
  - PlanDefinition builder create/edit/delete (via web routes).
- **12.b** Script logs results with timestamps and stores in `./results/<timestamp>_results/` (Rule 11).
- **12.c** Run the full endpoint test script. Update `progress.md`.

---

## 13) API key management (Rule 8)

### 13.1 Key storage rules

- **13.a** All API keys and secrets stored exclusively in `planp/.env`. Never committed to Git.
- **13.b** `planp/.env.example` committed with placeholder values as a template.

### 13.2 Key rotation procedure

- **13.c** Rotation steps:
  1. Generate new key/secret values.
  2. Update `planp/.env` on the target environment.
  3. Restart the application (`./start.sh` or `docker compose restart app`).
  4. Verify via `GET /api/v1/auth/me` with a fresh token.
  5. Invalidate old tokens (JWT blocklist flush or short expiry handles this).

### 13.3 Key expiry and revocation

- **13.d** JWT tokens: configurable expiry (default 1 hour access, 30 days refresh).
- **13.e** Token revocation via logout endpoint or blocklist.
- **13.f** Emergency revocation: change `JWT_SECRET_KEY` in `.env` and restart — invalidates all issued tokens.

### 13.4 Maintenance schedule

- **13.g** Recommended rotation cadence:
  - `JWT_SECRET_KEY`: every 90 days or on suspected compromise.
  - `FLASK_SECRET_KEY`: every 90 days.
  - `POSTGRES_PASSWORD`: every 180 days (requires DB user password update + `.env` update + restart).
  - `BOOTSTRAP_SU_PASSWORD`: change immediately after first login; remove from `.env` after bootstrap.

---

## 14) Web UI routes and templates

### 14.1 Terminology management pages

- **14.a** Implement web routes for managing lookup tables, values, valuesets, and concepts via browser forms.
- **14.b** Concept management page must enforce: single-choice response type requires a ValueSet selection.
- **14.c** All web pages follow the PDHC markdown layout standard (Rule 24).

### 14.2 Concept-value management page

- **14.d** Web page for adding/removing values from a concept's bound ValueSet.
- **14.e** Error handling: if concept has no ValueSet, display clear message and link to bind one.

---

## 15) Server deployment preparation

### 15.1 Reverse proxy safety (Rule 22)

- **15.a** Document the reverse proxy configuration for the Mac Mini server:
  - Application listens only on `localhost:9030`.
  - Reverse proxy routes only the designated path prefix to the application.
  - No interference with other services behind the proxy.
- **15.b** Create `safe_restart.sh` for the server instance (Rule 19):
  1. Gracefully stop the application.
  2. Pull latest code/config.
  3. Rebuild containers if needed.
  4. Start application.
  5. Health check.

### 15.2 Transfer procedure (Rule 12)

- **15.c** All web-level changes follow Rule 12:
  1. Download current server state to a temporary local archive.
  2. Compare with local version.
  3. Present comparison results — no code changes until reviewed.
  4. Operator manually applies changes based on instructions.
  5. No SSH/SCP from this plan.

### 15.3 Bootstrap on server (Rule 23)

- **15.d** `.env` must be fully prepared before first server deployment.
- **15.e** On first start, bootstrap superuser is created automatically from `.env` values.
- **15.f** Operator changes the superuser password immediately after first login, then removes `BOOTSTRAP_SU_PASSWORD` from `.env`.

---

## 16) Final validation and sign-off

- **16.a** Run the full test suite (`pytest planp/tests/ -v`). All tests must pass.
- **16.b** Run the comprehensive endpoint test script (step 12.a).
- **16.c** Verify FHIR compliance: all PlanDefinition responses validate against FHIR R5 structure (Rule 15).
- **16.d** Cross-reference each rule in `top_rules.md` against implementation — verify all satisfied.
- **16.e** Final update to `progress.md` with complete status.
- **16.f** Commit all work. Tag the release.

---

## Appendix A) File tracking requirements

Per Rules 2, 4, 11, and 17:

- **`progress.md`**: Updated after every numbered step with status and test results.
- **`changed_files.md`**: Updated whenever any file is created or edited, with full path.
- **`results/`**: Test outputs stored in `./results/<ISO-8601-UTC>_results/` subdirectories.
- **`newtask.txt`**: Created when entering debugging phase (Rule 13).

## Appendix B) Port allocation summary (Rule 16)

| Port | Service              |
|------|----------------------|
| 9030 | Flask application    |
| 9031 | PostgreSQL database  |
| 9032 | Reserved             |
| 9033 | Reserved             |

Kill targets before startup: ports 9000–9003 (legacy) and 9030–9033 (previous run).

---

## 17) FHIR Form Builder — interactive Questionnaire authoring

### 17.0 Overview and design rationale

The existing "Produce Form" flow (step 16.f / current `/forms/produce`) is a one-shot pipeline: pick concepts or a PlanDefinition → auto-generate a FHIR Questionnaire. That is useful for batch production but does **not** allow an author to:

1. Iteratively build a form question by question.
2. Configure per-question settings (required, display text override, item ordering).
3. Mix concepts from different sources in a single form.
4. Save a draft form definition that can be revised before production.
5. Re-use a form definition across multiple PlanDefinitions or from `request.pdhc.se`.

This section introduces a **Form Builder** — an interactive authoring tool that sits between raw concepts and the final FHIR Questionnaire. The builder produces a **FormDefinition** (the authored blueprint), which is then rendered into a versioned FHIR Questionnaire via the existing production pipeline.

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Concepts    │────▶│  Form Builder     │────▶│  FHIR Questionnaire │
│  Values      │     │  (FormDefinition) │     │  (versioned, stored)│
│  ValueSets   │     └──────────────────┘     └─────────────────────┘
└──────────────┘            │                          │
                            │  referenced by           │  callable from
                    ┌───────▼────────┐         ┌───────▼────────┐
                    │  PlanDefinition │         │ request.pdhc.se│
                    └────────────────┘         └────────────────┘
```

### 17.1 Data model — `form_definitions` and `form_definition_items`

- **17.a** Add `FormDefinition` model to `planp/app/models/forms_models.py`:

```
form_definitions
────────────────────────────────────────────────────────────
Column                  Type           Notes
────────────────────────────────────────────────────────────
id                      Integer        PK, auto
guid                    String(36)     UUID, unique, indexed
name                    String(255)    Machine name, unique
title                   String(500)    Human-readable title
description             Text           Optional long description
status                  String(20)     draft | active | retired (default: draft)
author                  String(255)    Creator identifier
vers_number             Integer        Incremented on update (default: 1)
produced_form_guid      String(36)     FK → questionnaires.form_guid (nullable)
                                       Points to the latest produced FHIR Questionnaire
production_key          String(255)    Tracks origin (e.g. "builder:<guid>")
date_created            DateTime       UTC timestamp
date_updated            DateTime       UTC timestamp, auto-update
```

- **17.b** Add `FormDefinitionItem` model to `planp/app/models/forms_models.py`:

```
form_definition_items
────────────────────────────────────────────────────────────
Column                  Type           Notes
────────────────────────────────────────────────────────────
id                      Integer        PK, auto
guid                    String(36)     UUID, unique
form_definition_guid    String(36)     FK → form_definitions.guid, indexed
concept_guid            String(36)     FK → concepts.guid
sort_order              Integer        Display ordering (default: 0)
display_text_override   String(500)    Optional override of concept_display_text
required                Boolean        Whether this question is mandatory (default: false)
enabled                 Boolean        Include in production (default: true)
item_type_override      String(50)     Override the auto-detected FHIR type (nullable)
group_label             String(255)    Optional group heading for sectioned forms
notes                   Text           Author notes (not rendered in FHIR)
date_created            DateTime       UTC timestamp
```

- **17.c** Junction constraint: `UNIQUE(form_definition_guid, concept_guid)` — a concept appears at most once per form definition.
- **17.d** Cascade delete: deleting a `FormDefinition` deletes its items.

### 17.2 Form Builder service — `planp/app/services/form_builder_service.py`

- **17.e** Implement `FormBuilderService` with the following operations:

| Function                          | Purpose                                                            |
|-----------------------------------|--------------------------------------------------------------------|
| `create_form_definition(data)`    | Create a new FormDefinition with metadata; return dict             |
| `update_form_definition(guid, data)` | Update metadata (title, description, status); increment vers_number |
| `delete_form_definition(guid)`    | Delete draft-only definition (reject if active/retired or has produced forms with responses) |
| `get_form_definition(guid)`       | Return definition with all items (concepts resolved)               |
| `list_form_definitions(filters)`  | Paginated list with status/search filters                          |
| `add_item(form_guid, data)`       | Add a concept to the definition; validate concept exists; enforce uniqueness |
| `update_item(item_guid, data)`    | Update sort_order, required, display_text_override, enabled, group_label |
| `remove_item(item_guid)`          | Remove a concept from the definition                               |
| `reorder_items(form_guid, ordered_guids)` | Bulk reorder items by accepting an ordered list of item GUIDs |
| `produce(form_guid)`              | Run the production pipeline: resolve items → build FHIR → validate → persist as Questionnaire |
| `get_resolved_preview(form_guid)` | Resolve items to question set without persisting (for live preview) |

- **17.f** The `produce()` function must:
  1. Load the FormDefinition and all enabled items (ordered by `sort_order`).
  2. Resolve each item's concept via the existing `_concept_to_question_item()` from `forms_service.py`.
  3. Apply per-item overrides (`display_text_override`, `required`, `item_type_override`).
  4. Group items under `group_label` headings using FHIR `group` items where applicable.
  5. Pass through `build_fhir_questionnaire()` → `validate_fhir_questionnaire()` → `create_or_append_form_version()`.
  6. Store the resulting `form_guid` back on `FormDefinition.produced_form_guid`.
  7. Set `production_key = "builder:<form_definition_guid>"`.

### 17.3 API endpoints — `planp/app/api/form_builder.py`

- **17.g** Register blueprint with prefix `/api/v1/form-definitions`. All write endpoints require `read_write` role. All read endpoints require `read_only`.

| Method | Path                                    | Description                                      |
|--------|-----------------------------------------|--------------------------------------------------|
| GET    | `/form-definitions`                     | List definitions (filters: status, search, limit, offset) |
| POST   | `/form-definitions`                     | Create definition (body: name, title, description) |
| GET    | `/form-definitions/<guid>`              | Get definition with resolved items                |
| PUT    | `/form-definitions/<guid>`              | Update metadata                                   |
| DELETE | `/form-definitions/<guid>`              | Delete draft definition                           |
| GET    | `/form-definitions/<guid>/items`        | List items for a definition                       |
| POST   | `/form-definitions/<guid>/items`        | Add concept to definition                         |
| PUT    | `/form-definitions/<guid>/items/<item_guid>` | Update item settings                         |
| DELETE | `/form-definitions/<guid>/items/<item_guid>` | Remove item from definition                  |
| POST   | `/form-definitions/<guid>/reorder`      | Bulk reorder items (body: `[item_guid, ...]`)     |
| POST   | `/form-definitions/<guid>/produce`      | Run production pipeline → returns FHIR Questionnaire |
| GET    | `/form-definitions/<guid>/preview`      | Resolve items without persisting (live preview)   |

- **17.h** The `produce` endpoint returns the produced Questionnaire dict (same shape as `POST /api/v1/forms/produce`) and links the FormDefinition to the produced form.

### 17.4 Web UI — Form Builder page

- **17.i** Add web routes to `planp/app/routes/form_builder.py`:

| Route                                      | Method    | Template / Action                          |
|--------------------------------------------|-----------|--------------------------------------------|
| `/form-builder`                            | GET       | List all form definitions                  |
| `/form-builder/create`                     | GET, POST | Create new form definition                 |
| `/form-builder/<guid>`                     | GET       | View definition detail + items             |
| `/form-builder/<guid>/edit`                | GET, POST | Edit metadata + manage items               |
| `/form-builder/<guid>/delete`              | POST      | Delete draft definition                    |
| `/form-builder/<guid>/produce`             | POST      | Produce FHIR Questionnaire → redirect to form detail |

- **17.j** The **builder/edit page** (`form-builder/<guid>/edit`) is the core interactive experience. It must provide:

1. **Metadata section** — editable title, description, name (auto-derived from title if empty).
2. **Item list** — a sortable table of added concepts showing:
   - Sort handle (drag or up/down arrows)
   - Concept name + canonical code
   - Response type (auto-detected)
   - Display text override (inline editable)
   - Required toggle (checkbox)
   - Enabled toggle (checkbox)
   - Group label (inline editable)
   - Remove button
3. **Concept picker** — reuse the concept filter/search pattern from `produce.html`:
   - Searchable list of all active concepts
   - "Add" button per concept (greyed out if already added)
   - Show response type and canonical code for each concept
4. **Live preview panel** — calls `/api/v1/form-definitions/<guid>/preview` and renders a read-only preview of the form as it would appear (question text, type indicator, options for choice questions).
5. **Produce button** — triggers production pipeline; redirects to the produced Questionnaire detail page on success.

- **17.k** Templates to create:

```
templates/form_builder/
├── list.html              # Definition catalogue with status filters
├── create.html            # New definition form (name, title, description)
├── view.html              # Read-only definition detail with items and production history
└── edit.html              # Interactive builder (metadata + item management + preview)
```

- **17.l** Add "Form Builder" link to the navbar in `base.html` (between "Forms" and "Docs").

### 17.5 Integration with PlanDefinitions

- **17.m** Add optional `form_definition_guid` column to `plan_definitions` table (nullable FK → `form_definitions.guid`). This allows a PlanDefinition to reference a specific authored form.

- **17.n** In the PlanDefinition builder (`/plandefinitions/builder`), add a "Linked Form" dropdown that lists active FormDefinitions. When selected, the form's concepts are displayed read-only in the builder for reference.

- **17.o** When a PlanDefinition with a linked FormDefinition is used in `request.pdhc.se`, the integration endpoint returns:
  - The PlanDefinition FHIR JSON (existing behavior)
  - The produced Questionnaire FHIR JSON (from the linked FormDefinition's `produced_form_guid`)

### 17.6 External access — callable from `request.pdhc.se`

- **17.p** Add endpoint `GET /api/v1/form-definitions/<guid>/questionnaire` that returns the latest produced FHIR Questionnaire JSON for a FormDefinition. This is the primary integration point for `request.pdhc.se`:
  - If the FormDefinition has a `produced_form_guid`, return that Questionnaire's `fhir_json`.
  - If not yet produced, return 404 with instruction to produce first.
  - Accepts `?version=N` to retrieve a specific Questionnaire version.
  - Authentication: API key (`X-API-Key`) or SSO session.

- **17.q** Add endpoint `GET /api/v1/form-definitions/<guid>/render-ready` that returns a simplified, render-ready JSON format optimized for frontend rendering in `request.pdhc.se`:

```json
{
  "form_guid": "<uuid>",
  "title": "Blood Pressure Monitoring",
  "description": "...",
  "version": 3,
  "status": "active",
  "items": [
    {
      "link_id": "<concept-guid>",
      "text": "Systolic blood pressure",
      "type": "numeric",
      "required": true,
      "unit": "mmHg",
      "min_value": 60,
      "max_value": 300,
      "group": "Vitals"
    },
    {
      "link_id": "<concept-guid>",
      "text": "Pain severity",
      "type": "single_choice",
      "required": true,
      "options": [
        {"value": "<guid>", "label": "Mild", "code": "1"},
        {"value": "<guid>", "label": "Moderate", "code": "2"},
        {"value": "<guid>", "label": "Severe", "code": "3"}
      ],
      "group": "Assessment"
    }
  ]
}
```

### 17.7 Database migration

- **17.r** Generate migration: `flask db migrate -m "add form_definitions and form_definition_items tables"`.
- **17.s** Apply migration: `flask db upgrade`.
- **17.t** Add `form_definition_guid` column to `plan_definitions` via a separate migration: `flask db migrate -m "add form_definition_guid to plan_definitions"`.

### 17.8 Tests

- **17.u** Write `tests/test_form_builder.py`:
  - CRUD cycle for FormDefinition (create, read, update, delete).
  - Item management (add, update, remove, reorder).
  - Duplicate concept rejection (unique constraint).
  - Production pipeline (produce from definition → verify Questionnaire created).
  - Preview endpoint returns resolved items without persisting.
  - Status lifecycle: draft → active → retired.
  - Delete rejection for active/retired definitions.
  - Auth enforcement on all endpoints.

- **17.v** Write `tests/test_form_builder_integration.py`:
  - PlanDefinition with linked FormDefinition produces correct Questionnaire.
  - `/questionnaire` endpoint returns produced FHIR JSON.
  - `/render-ready` endpoint returns simplified format.
  - Version pinning works correctly.

- **17.w** Run tests. Store results in `./results/<timestamp>_results/`. Update `progress.md`.

### 17.9 Capability statement update

- **17.x** Add FormDefinition endpoints to the capability statement in `planp/app/api/capability.py`:

```json
{
  "type": "FormDefinition",
  "profile": "custom:form-definition",
  "interaction": [
    {"code": "read"},
    {"code": "search-type"},
    {"code": "create"},
    {"code": "update"},
    {"code": "delete"}
  ],
  "operation": [
    {"name": "produce", "definition": "Produce FHIR Questionnaire from definition"},
    {"name": "preview", "definition": "Preview resolved form without persisting"},
    {"name": "render-ready", "definition": "Render-ready JSON for frontend integration"}
  ]
}
```

### 17.10 File summary

New files:

| File                                            | Purpose                                |
|-------------------------------------------------|----------------------------------------|
| `planp/app/services/form_builder_service.py`    | Form builder business logic            |
| `planp/app/api/form_builder.py`                 | API endpoints blueprint                |
| `planp/app/routes/form_builder.py`              | Web UI routes                          |
| `planp/app/templates/form_builder/list.html`    | Definition catalogue                   |
| `planp/app/templates/form_builder/create.html`  | New definition form                    |
| `planp/app/templates/form_builder/view.html`    | Definition detail                      |
| `planp/app/templates/form_builder/edit.html`    | Interactive builder                    |
| `planp/tests/test_form_builder.py`              | Unit + integration tests               |
| `planp/tests/test_form_builder_integration.py`  | Cross-system integration tests         |

Modified files:

| File                                            | Change                                 |
|-------------------------------------------------|----------------------------------------|
| `planp/app/models/forms_models.py`              | Add FormDefinition, FormDefinitionItem |
| `planp/app/__init__.py`                         | Register new blueprints                |
| `planp/app/templates/base.html`                 | Add Form Builder nav link              |
| `planp/app/models/fhir_models.py`               | Add form_definition_guid column        |
| `planp/app/api/capability.py`                   | Add FormDefinition to capability       |
| `planp/migrations/versions/`                    | Two new migration files                |

### 17.11 Implementation order

| Step | Task                                              | Depends on |
|------|---------------------------------------------------|------------|
| 1    | Add models (17.a–17.d) + migration (17.r–17.s)   | —          |
| 2    | Implement service layer (17.e–17.f)               | Step 1     |
| 3    | Implement API blueprint (17.g–17.h)               | Step 2     |
| 4    | Register blueprint in `__init__.py`               | Step 3     |
| 5    | Implement web routes (17.i)                       | Step 2     |
| 6    | Create templates (17.j–17.l)                      | Step 5     |
| 7    | Add PlanDefinition integration (17.m–17.o, 17.t)  | Step 4     |
| 8    | Add external access endpoints (17.p–17.q)         | Step 4     |
| 9    | Update capability statement (17.x)                | Step 4     |
| 10   | Write and run tests (17.u–17.w)                   | Steps 1–8  |
