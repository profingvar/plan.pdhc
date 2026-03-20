# PDHC PlanDef Builder — Changed Files Log

Per Rule 17, all edited files are noted here with full path.

---

## Infrastructure

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/readme.md` — deployment plan
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/progress.md` — progress tracking
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/changed_files.md` — this file
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/.gitignore` — git ignore rules
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/start.sh` — startup script (Rule 16)
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/plan_description.md` — domain architecture reference
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/repo_css.md` — frontend design system
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/pdhc_markdown_layout_standard.md` — markdown style guide

## Docker / Config

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/docker-compose.yml` — Docker Compose config
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/Dockerfile` — app container definition
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/.env` — environment variables (not committed)
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/.env.example` — env template
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/requirements.txt` — Python dependencies
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/entrypoint.sh` — runs migrations then starts gunicorn

## Application

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/__init__.py` — Flask app factory
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/config.py` — configuration

## Models

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/models/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/models/user_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/models/concept_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/models/fhir_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/models/activity_models.py`

## API

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/auth.py` — login, logout, me, refresh, rate limiting
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/lookup_tables.py` — generic CRUD for 6 lookup tables + valueset membership sort update
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/concepts.py` — concept CRUD + concept-values endpoints
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/fhir_plandefinitions.py` — FHIR R5 read/search/expand
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/plandefinitions.py` — full CRUD API for PlanDefinitions
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/api/capability.py` — capability statement + endpoint list

## Web Routes

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/main.py` — dashboard + docs browser + docs download
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/concepts.py` — concept management UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/values.py` — value CRUD UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/valuesets.py` — valueset CRUD + membership UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/lookup_tables.py` — lookup table CRUD UI (canonical libs, units, response types, concept types)
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/routes/plandefinitions.py` — PlanDefinition builder + list/view/edit/delete/export

## Services

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/services/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/services/fhir_service.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/services/name_uniqueness.py`

## Templates (32 files)

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/base.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/dashboard.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/docs.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/concepts/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/concepts/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/concepts/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/values/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/values/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/values/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/values/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/valuesets/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/valuesets/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/valuesets/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/valuesets/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/canonical_libs/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/canonical_libs/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/canonical_libs/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/canonical_libs/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/concept_types/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/concept_types/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/concept_types/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/concept_types/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/response_types/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/response_types/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/response_types/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/response_types/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/units/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/units/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/units/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/lookup/units/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/plandefinitions/builder.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/plandefinitions/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/templates/plandefinitions/view.html`

## Static Assets

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/app/static/css/pdhc.css` — design system stylesheet

## Documentation

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/docs/api_reference.md` — comprehensive API documentation
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/db_schema_snapshot.md` — database schema with samples and GUIDs

## Tests

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/conftest.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_auth.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_lookup_tables.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_valuesets.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_concepts.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_plandefinitions.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/tests/test_fhir_endpoints.py`

## Migrations

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/migrations/` — Flask-Migrate directory
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/gateway/migrations/versions/c3d87bb08504_initial_models.py`
