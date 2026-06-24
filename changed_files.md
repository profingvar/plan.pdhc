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

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docker-compose.yml` — Docker Compose config
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/Dockerfile` — app container definition
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env` — environment variables (not committed)
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env.example` — env template
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/requirements.txt` — Python dependencies
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/entrypoint.sh` — runs migrations then starts gunicorn

## Application

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/__init__.py` — Flask app factory
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/config.py` — configuration

## Models

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/user_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/concept_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/fhir_models.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/activity_models.py`

## API

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/auth.py` — login, logout, me, refresh, rate limiting
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/lookup_tables.py` — generic CRUD for 6 lookup tables + valueset membership sort update
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/concepts.py` — concept CRUD + concept-values endpoints
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_plandefinitions.py` — FHIR R5 read/search/expand
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/plandefinitions.py` — full CRUD API for PlanDefinitions
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/capability.py` — capability statement + endpoint list

## Web Routes

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/main.py` — dashboard + docs browser + docs download
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/concepts.py` — concept management UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/values.py` — value CRUD UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/valuesets.py` — valueset CRUD + membership UI
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/lookup_tables.py` — lookup table CRUD UI (canonical libs, units, response types, concept types)
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/plandefinitions.py` — PlanDefinition builder + list/view/edit/delete/export

## Services

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/fhir_service.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/name_uniqueness.py`

## Templates (32 files)

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/base.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/dashboard.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/docs.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/concepts/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/concepts/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/concepts/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/values/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/values/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/values/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/values/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/valuesets/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/valuesets/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/valuesets/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/valuesets/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/canonical_libs/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/canonical_libs/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/canonical_libs/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/canonical_libs/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/concept_types/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/concept_types/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/concept_types/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/concept_types/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/response_types/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/response_types/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/response_types/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/response_types/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/units/create.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/units/edit.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/units/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/lookup/units/view.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/plandefinitions/builder.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/plandefinitions/list.html`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/plandefinitions/view.html`

## Static Assets

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/static/css/pdhc.css` — design system stylesheet

## Documentation

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docs/api_reference.md` — comprehensive API documentation
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/db_schema_snapshot.md` — database schema with samples and GUIDs

## Tests

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/__init__.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/conftest.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_auth.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_lookup_tables.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_valuesets.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_concepts.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_plandefinitions.py`
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_endpoints.py`

## Migrations

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/migrations/` — Flask-Migrate directory
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/migrations/versions/c3d87bb08504_initial_models.py`

## 2026-04-11 — Snapshot goal enrichment (SCOPE_VIOLATION root-cause fix)

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/plandefinitions.py` — Modified `_plandef_full_dict()` so the snapshot emits `goal_guid` / `goal_concept_guid` / `goal_concept_name` on every activity and every transaction. For now, populated via **single-goal inference** (if `len(goals) == 1`, all activities/transactions inherit that goal's concept). This is the data path that lets gateway tag observations with the *measurement* concept (B-glucos) rather than the transaction's *procedure* concept (CGM), so contract-scope validation passes. NOT YET DEPLOYED to miserver — `request.pdhc/gateway/app/services/context_service.py` already has the same single-goal fallback in `_extract_transactions`, so today's live SR (523d1227-132b-4d2a-8129-fdbb1519b039) works without a plan.pdhc redeploy. Deploy on the next plan.pdhc release or if we need to support multi-goal plans (which will need an explicit activity→goal FK instead of the inference).

## 2026-04-15 — Health endpoint standardisation (ticket #39)

| File | Change |
|------|--------|
| `planp/app/__init__.py` | `/api/health` upgraded to CLAUDE.md §10 shape: returns `{status, database, service}` with HTTP 200/503 based on a live `SELECT 1`. Adds `Access-Control-Allow-Origin: *` and `Cache-Control: no-store` headers. |
| `miserver:/usr/local/www/plan.pdhc/planp/app/__init__.py` | Same file replaced on server; `docker cp` into `pdhc_app:/app/app/__init__.py`; `docker restart pdhc_app`. |

| 2026-04-15 | planp/app/api/auth.py | Ticket #49. Stopped trusting `session['sso_user']` for authorization. New `_refresh_blob_or_clear()` helper calls `validate_token(session['sso_token'])` on every protected request; on failure, wipes the session. `requires_role`, `sso_login_required`, and `/me` all route through it. Session copy of the blob is kept only as a display cache for `base.html` and refreshed from each fresh response. New `must_change_password` handling: API routes return 403 with `change_password_url`; HTML routes + the callback redirect to `{SSO_BASE_URL}/change-password`. Closes the Rule 11 / CLAUDE.md §11 caching violation and makes SSO ticket #44's session flush take effect immediately (stale tokens → 401 from /me/service → cleared session → re-login). |
| 2026-04-15 | planp/tests/conftest.py | Added autouse `mock_sso_validate_per_request` fixture that short-circuits `app.services.sso_service.validate_token` in tests to return the blob stashed by `set_sso_session()`. Skipped for `TestSSOCallback` which already exercises the real validation flow with a `requests.get` patch. Preserves existing test ergonomics while the decorators now make per-request validation calls. |
| 2026-04-15 | plan.pdhc docker image | Rebuilt `planp-app:latest` on macmini (docker-compose up -d --build app) — pdhc_app recreated, /api/health green, database:connected. Ticket #49 deployed. |
| `planp/app/__init__.py` | Ticket #70 / CLAUDE.md §10: tightened CORS on `/api/health` from `Access-Control-Allow-Origin: *` to `https://www.pdhc.se`, added `Access-Control-Allow-Methods: GET`. Used `resp.headers.add('Vary', 'Origin')` (append, not overwrite) to preserve the existing `Vary: Cookie` from the session middleware → final `vary: Origin, Cookie`. Note: Flask-CORS is also active on `/api/*` with `origins="*"` — worried it would override my handler-level ACO, but it did not (handler-set value wins). Verified via `curl -I -H 'Origin: https://www.pdhc.se'`: all three headers + `vary: Origin, Cookie`, body `{"database":"connected","service":"plan.pdhc","status":"ok"}`. Server backup at `/tmp/plan_init.py.bak.20260416T185418Z`. |

# 2026-04-28 — Service-key auth path + 58 diabetes Concepts loaded

Driven by sim.pdhc multi-CDR seed needing to bulk-register clinical
concepts in plan.pdhc without an SSO session per request.

| File | Change |
|------|--------|
| `planp/app/api/auth.py` | Added `KNOWN_SERVICES` dict (`loader.pdhc` → `PLAN_LOADER_SERVICE_KEY`, `sim.pdhc` → `SIM_PDHC_SERVICE_KEY`). New `_service_key_outcome()` helper inspects `X-Source-Service` + `X-Service-Key` headers and returns None / True / False. `requires_role` now checks the service-key path FIRST: if valid → bypass SSO; if invalid → 403; if absent → fall through to existing SSO flow. AUTH_DISABLED branch unchanged. Backwards-compatible: human SSO sessions still work identically. |
| `planp/app/config.py` | `Config` reads `PLAN_LOADER_SERVICE_KEY` and `SIM_PDHC_SERVICE_KEY` from env (empty string default). |
| `miserver:/usr/local/www/plan.pdhc/planp/app/api/auth.py + config.py` | Same files replaced on server. `docker-compose up -d --build app` rebuilt `planp-app:latest` and recreated `pdhc_app` container. Volume `pdhc_pgdata` preserved (canonical_libs / units / etc. all intact). Smoke verified: GET /api/v1/concepts (public) 200; POST /api/v1/concept-types unauth 401; POST with wrong key 403; POST with valid key 201; DELETE 200. |
| `miserver:/usr/local/www/plan.pdhc/planp/.env` | Added `PLAN_LOADER_SERVICE_KEY=<43-char token>`. Backup at `.env.bak.20260428-loader`. Operator owns the key (also on local Mac at `/tmp/plan_loader_key`, mode 600). |
| plan.pdhc DB (via API) | Loaded 58 diabetes Concepts via `sim.pdhc/concepts/load_to_plan.py` running with `PLAN_LOADER_SERVICE_KEY`. Auto-created `ATC` canonical_lib (was missing — only LOINC / Snomed CT / ICD10 / KVÅ / local existed) and `Medication` concept_type. Total Concepts went from 12 (draft test items pre-existing) to 70. The 58 cover: 8 anthro/vitals (weight/height/BMI/waist/BP sys+dia/HR/temp), 8 glycemic (HbA1c, FPG, RPG, CGM mean/TIR/TBR/TAR/CV), 5 lipids (LDL/HDL/TC/TG/non-HDL), 3 renal (creat/eGFR/urine ACR), 3 liver (ALT/AST/GGT), 3 heme (Hb/WBC/Plt), 2 thyroid (TSH/FT4), 1 lifestyle (smoking_status), 11 diagnoses (T1/T2DM, hypertension, dyslipidemia, CKD, retinopathy, neuropathy, foot ulcer, MI history, stroke history, heart failure — all SNOMED-CT primary with ICD-10-SE in `icd10_alt` for dual coding on the FHIR side), 9 medications (insulin / metformin / SGLT2 / GLP-1 / statin / ACEi / ARB / aspirin / thiazide — ATC), 3 procedures (HbA1c sampling, retinal screening, foot screening), 2 encounter types (primary care, diabetes nurse). |
| plan.pdhc DB (via API, post-loader) | Added one extra Concept `inpatient_admit` (SNOMED 32485007 "Hospital admission") on 2026-04-28T15:39Z so cdr.pdhc canonicaliser stops returning plan_miss for sim's inpatient encounters. Brought total to 71 Concepts. |

Backup of plan.pdhc planp/.env on miserver: `.env.bak.20260428-loader`.


| 2026-04-30 | (DB) canonical_libs alignment with termbank | Renamed 4 plan.pdhc `canonical_libs` rows so `canonical_lib_name` matches termbank's `concepts.system` exactly: ATC→atc, ICD10→icd10, LOINC→loinc, "Snomed CT"→snomed. Pre-existing rows from migration `b3a1f7c9d401` had drifted from the convention; the later seed migration `c2d6ef39a1f0` was idempotent and skipped them. Added two new rows: icf and socialstyrelsen. Fixes: search-widget system filter on plan.pdhc/concepts/new returned 0 results when the user picked any specific lib, because the JS sends the `canonical_lib_name` text directly to termbank's `/search?system=`, and termbank's filter is exact-match. |

## 2026-04-30 — Termbank wiring + canonical_libs alignment + system-filter UI

| File | Change |
|------|--------|
| `planp/app/templates/concepts/create.html` | Each canonical_lib `<option>` gains `data-name="{{ lib.canonical_lib_name }}"` and renders `canonical_lib_display_text` as the visible label (falls back to `canonical_lib_name`). Result: dropdown shows "ATC (Anatomical Therapeutic Chemical)" / "Socialstyrelsens termbank" / etc. while behind the scenes `data-name` carries the lowercase short ID (`atc`, `socialstyrelsen`, ...) that gets sent to termbank's `/search?system=` filter. Friendly UX, no breakage. |
| `planp/app/static/js/termbank_search_picker.js` | `buildSystemSelect` now reads `opt.getAttribute("data-name")` first, falling back to `textContent` for compatibility. Each option carries `value` = canonical short name; visible text = display label. Lets the same widget render either friendly or short labels depending on whether the underlying form sets `data-name`. |
| (DB) miserver pdhc_db / `canonical_libs` | Six canonical_libs aligned with termbank's `concepts.system` exact-match: ATC→atc, ICD10→icd10, LOINC→loinc, "Snomed CT"→snomed; added new rows `icf` and `socialstyrelsen`. Pre-existing rows from migration `b3a1f7c9d401` had drifted from the seed convention; the later seed migration `c2d6ef39a1f0` was idempotent and skipped them. Same rename + ICF insert applied to local Mac DB on :9031. |
| `pdhc_app` env | Added `TERMBANK_BASE_URL=http://host.docker.internal:9012` to `/usr/local/www/plan.pdhc/planp/.env`. Container recreated via `docker compose -p planp up -d app` so the env actually loads (docker restart keeps create-time env). Plan.pdhc's New Concept widget now reaches termbank.pdhc and returns real results across all 6 systems. |

## 2026-04-30 — Multi-select "prechosen libs" in termbank picker

| File | Change |
|------|--------|
| `planp/app/static/js/termbank_search_picker.js` | Replaced the single `<select data-termbank-system>` dropdown with a checkbox group (`<div data-termbank-systems>`) — one checkbox per canonical_lib. JS collects all checked boxes and sends repeated `?system=loinc&system=snomed` query params (which termbank's new ranked `/search` honours via `request.args.getlist`). Legacy `data-termbank-system` `<select>` still honoured if any template hasn't been migrated. `FALLBACK_SYSTEMS` extended with `icf`. |
| `planp/app/templates/concepts/create.html`, `planp/app/templates/concepts/edit.html`, `planp/app/templates/values/create.html`, `planp/app/templates/values/edit.html` | Picker block restructured: query input on its own row, "Limit to libraries (none = all)" checkbox row underneath. |
| `pdhc_app` (live container) | New JS + 4 templates copied via `colima ssh -- docker cp` from `/Users/miserver/tmp_plan_deploy/...` (image-baked code, not bind-mounted). pdhc_app restarted; /api/health 200. |

## 2026-05-16 — Bounded recurrence on PlanDefinition actions (Option A)

| File | Change |
|------|--------|
| `planp/app/models/activity_models.py` | Added four nullable columns to `Activity`: `timing_bounds_mode` ('count' / 'duration' / NULL), `timing_bounds_count`, `timing_bounds_duration_value`, `timing_bounds_duration_unit`. NULL = unbounded (backward compatible). `to_dict` extended. |
| `planp/migrations/versions/d4f5a6b71208_add_activity_timing_bounds.py` | New migration. `down_revision = c2d6ef39a1f0` (current head). Adds the four columns, all nullable. |
| `planp/app/templates/plandefinitions/builder.html` | New "Ends" row rendered by `boundsRowHtml()` — segmented select (Never / After N occurrences / After a period) with conditional inputs. Visible only when Timing = Repeat (toggled by `onTimingTypeChange`). `collectActions()` serializes the new fields; `buildFhirPreview()` emits `repeat.count` or `repeat.boundsDuration` (UCUM). |
| `planp/app/routes/plandefinitions.py` | `create_plandef` and `edit_plandef` persist the four new fields on both new and existing Activity rows. |
| `planp/app/api/plandefinitions.py` | `create_plandefinition` and `update_plandefinition` persist the four new fields on both new and existing Activity rows. |
| `planp/app/services/fhir_service.py` | Form-action FHIR emission now includes `count` or `boundsDuration` on `Timing.repeat` when bounds_mode is set. Regular actions inherit the new fields automatically via the raw JSON pass-through. |

## 2026-05-18 — Full canonical URL refs in FHIR emission

| File | Change |
|------|--------|
| `planp/app/templates/plandefinitions/builder.html` | Added `PLAN_BASE = 'https://plan.pdhc.se'` const. `definitionCanonical` for form actions and concept-bound transaction sub-actions now emits full URL (`{PLAN_BASE}/api/v1/forms/<guid>` and `/api/v1/concepts/<guid>`) instead of relative `Questionnaire/<guid>` / `Concept/<guid>`. Goal Quantity/Range targets now include UCUM `system` (`http://unitsofmeasure.org`) + `code` on every `Quantity` (helper `qty()`); categorical targets emit `coding` array with `system = {PLAN_BASE}/api/v1/valuesets/<vs_guid>` so providers can validate against the bound valueset. |
| `planp/app/services/fhir_service.py` | Added `PLAN_BASE = "https://plan.pdhc.se"` const. Server-side form-action emission updated to full canonical URL for `definitionCanonical`. (Regular actions inherit changes via the raw JSON pass-through that's already populated by the JS preview.) |

## 2026-05-18 — Snapshot enrichment so CarePlan can emit fully-coded goal targets

| File | Change |
|------|--------|
| `planp/app/templates/plandefinitions/builder.html` | `collectGoals()` now enriches the goal JSON with `target_unit_name` (resolved from UNITS lookup; plan.pdhc unit_name == UCUM code), and for categorical targets `target_categorical_valueset` + `target_categorical_code` + `target_categorical_display` (resolved from CONCEPTS → VALUESETS lookup). The snapshot is now self-contained — downstream consumers (request.pdhc CarePlan, providers) can emit fully-coded FHIR Quantity / CodeableConcept without resolving GUIDs back through plan.pdhc's API. |

## 2026-06-22 — FHIR R5 terminology profile: §4 Prerequisites + §5 ADR + §6.5/§6.6 foundation

| File | Change |
|------|--------|
| `plan_pdhc_fhir_terminology_profile_instruction.md` (parent dir) | Rewritten earlier in this session: added §4 Prerequisites, §5 Decisions, §9 Risks; renumbered work items to §6.x; sequencing updated to step 0 = characterization tests. |
| `plan_pdhc_fhir_terminology_profile_DECISIONS.md` (parent dir, NEW) | ADR sibling. Five decisions (D1–D5) each with rationale, alternatives, consequences, reversibility. ALL APPROVED 2026-06-22. D1 expanded with deep rationale (cdr.pdhc cross-service identity argument, four-candidate comparison table, failure modes, migration playbook). |
| `planp/tests/test_auth.py` | `/api/v1/canonical-libs` → `/api/v1/lookup/canonical-libs` (5 occurrences); `test_health_returns_ok` updated to assert CLAUDE.md §10 canonical shape (status/database/service/version). |
| `planp/tests/test_valuesets.py` | URL prefix fix: canonical-libs, values, valuesets → /api/v1/lookup/... |
| `planp/tests/test_concepts.py` | URL prefix fix (same); `_setup_concept_deps` lib_name switched from `id(client)` (CPython memory recycling caused collisions) to `uuid.uuid4()`. |
| `planp/tests/test_lookup_tables.py` | URL prefix fix: canonical-libs, concept-types, response-types, units → /api/v1/lookup/... |
| `planp/tests/test_capability.py` (NEW) | 6 tests pinning §2 capability surface (`/metadata`, `/capability-statement`, `/endpoints`) and the CDR cross-service `$validate-code` contract — URL shape + Parameters body fields consumed by `cdr.pdhc/cdr_app/app/services/plan_client.py::PlanClient._parse_parameters`. |
| `planp/app/models/concept_models.py` | Added FHIR canonical URL helpers next to `PLAN_BASE`: `LOCAL_CODESYSTEM_ID = "plan-pdhc-local"`, `fhir_canonical_url(resource, id)`, `fhir_version(model_obj)`. Single source of truth for `{PLAN_BASE}/fhir/{Resource}/{id}` per ADR D3. No other model changes. |
| `planp/app/api/fhir_helpers.py` (NEW) | Shared §6.5 cross-cutting helpers: `operation_outcome()`, `parameters_response()`, `fhir_json_response()`, `parse_parameters_body()`. `FHIR_CONTENT_TYPE = 'application/fhir+json'`. Existing `terminology.py` private helpers left in place for backward compat. |
| `planp/tests/test_fhir_helpers.py` (NEW) | 20 tests: URL builder + version helper (D3/D4), all four shared helpers, D5 fast-validator wiring (round-trip via `fhir.resources` pydantic models), and the D3 lint forbidding any file other than the URL helper from hardcoding plan.pdhc `/fhir/` URLs. |
| `planp/requirements.txt` | Added `fhir.resources>=8.0` (D5 fast-layer FHIR R5 validator). Pulls in `pydantic>=2.13`, `fhir-core`. |
| `planp/progress.md` | Appended a "2026-06-22 — FHIR R5 terminology profile" section summarizing §4/§5/§6.5+§6.6 completion. |

## 2026-06-22 — FHIR R5 terminology profile §6.1: ValueSet resource + $expand

| File | Change |
|------|--------|
| `planp/app/api/fhir_valueset.py` (NEW) | New blueprint `fhir_valueset_bp` registered at `/api/v1`. Four routes: `GET /ValueSet/{guid}` (read), `GET /ValueSet` (searchset Bundle with `?url=&_count=&_offset=`), `GET /ValueSet/{guid}/$expand` (and `%24expand` escape variant), `POST /ValueSet/$expand` (Parameters body). Helpers: `_extract_guid_from_url` (D3 + D3.b — accepts canonical and legacy URL forms), `_value_rows`, `_build_compose` (groups by `canonical_lib_url`), `_build_expansion` (flat contains[]), `_to_fhir_valueset`. All output via `fhir_helpers.fhir_json_response` (Content-Type: application/fhir+json) and errors via `operation_outcome`. |
| `planp/app/__init__.py` | Registered `fhir_valueset_bp` at `/api/v1` alongside `terminology_bp`. Additive; doesn't replace the existing `/api/v1/lookup/valuesets` CRUD blueprint. |
| `planp/tests/test_fhir_valueset.py` (NEW) | 22 tests: read shape (FHIR R5 fields, D3 canonical url, D4 version), search Bundle, D3.b legacy URL acceptance in `?url=`, paging, `$expand` GET (populated + empty), `$expand` POST with Parameters body, escaped `%24expand`, D5 round-trip validation via `fhir.resources` R5 pydantic models, and a §2 regression assertion that the legacy `/api/v1/lookup/valuesets/{guid}` CRUD JSON still returns its non-FHIR shape. |
| `planp/progress.md` | §6.1 section appended. Test count 102 → 124. |

## 2026-06-22 — FHIR R5 terminology profile §6.2: scoped $validate-code

| File | Change |
|------|--------|
| `planp/app/api/fhir_valueset.py` | Added `resolve_canonical_lib(system_or_url)` and `scoped_validate_code(vs, system, code)` (public, called from terminology.py too). Two new routes: `GET /ValueSet/<guid>/$validate-code` (and `%24` escape variant) for path-scoped validation; `POST /ValueSet/$validate-code` for Parameters-body scoped validation (url/valueSet + code). |
| `planp/app/api/terminology.py` | Imported `ValueSet`. `validate_code()` adds a top branch: if `?url=` or `?valueSet=` present, dispatch to `scoped_validate_code` via local import (avoids startup cycle). Bare `?system=&code=` path is byte-identical to before — preserves the cdr.pdhc plan_client shim contract. |
| `planp/tests/test_fhir_valueset.py` | +18 tests: `TestScopedValidateCodeByGuid` (8), `TestScopedValidateCodeByUrl` (5 — incl D3.b legacy url), `TestScopedValidateCodeByPost` (3), `TestCDRGlobalContractAfter62` (2 — explicit cdr.pdhc request-shape pin to catch any future drift). D5 round-trip validation on scoped responses via `fhir.resources.parameters.Parameters`. |
| `planp/progress.md` | §6.2 section appended. Test count 124 → 142. |

## 2026-06-22 — FHIR R5 terminology profile §6.4: ConceptMap + $translate

| File | Change |
|------|--------|
| `planp/app/models/concept_models.py` | Added `LOCAL_CONCEPTMAP_ID = "plan-pdhc-canonical-bindings"` next to `LOCAL_CODESYSTEM_ID`. |
| `planp/app/api/fhir_conceptmap.py` (NEW) | New blueprint `fhir_conceptmap_bp` registered at `/api/v1`. Four routes: `GET /ConceptMap/{id}`, `GET /ConceptMap[?url=]` (searchset Bundle, size 0 or 1), `GET /ConceptMap/$translate` (and `%24translate`), `POST /ConceptMap/$translate`. Helpers: `_build_conceptmap` (groups Concepts by canonical_lib target URL, source = LOCAL_CS_URL, relationship = `equivalent`), `_translate` (bidirectional — accepts LOCAL_CS_URL system for local→canonical, OR CanonicalLib URL/name for canonical→local), `_build_match_parameter` (Risk §9.5 — match always shaped as repeating FHIR Parameters parts), `_resolve_lib_for_input`. |
| `planp/app/__init__.py` | Registered `fhir_conceptmap_bp` at `/api/v1` after the ValueSet blueprint. |
| `planp/tests/test_fhir_conceptmap.py` (NEW) | 27 tests across: read (7 — shape, D1 guid-as-source-code, orphan exclusion, relationship=equivalent, R5 model validation), search Bundle (3), local→canonical translate (5 — incl. targetsystem filter, unknown concept, orphan-no-binding), canonical→local translate (5 — URL form, name form for cdr.pdhc lenience, unknown system non-404), POST Parameters (3), error paths (2), and the Risk §9.5 match-array invariant (2 — zero matches doesn't collapse the response, single match emits one repeating parameter). |
| `planp/progress.md` | §6.4 section appended. Test count 142 → 169. |

## 2026-06-22 — FHIR R5 terminology profile §6.3: CodeSystem + $lookup (termbank delegation)

| File | Change |
|------|--------|
| `planp/app/api/fhir_codesystem.py` (NEW) | New blueprint `fhir_codesystem_bp` registered at `/api/v1`. Four routes: `GET /CodeSystem/{id}` (read with `content: 'complete'`), `GET /CodeSystem[?url=]` (searchset Bundle), `GET /CodeSystem/$lookup` (and `%24lookup` escape), `POST /CodeSystem/$lookup`. Builds the local CodeSystem from `Concept.query` with `concept[].code = Concept.guid` (ADR D1), `display = concept_display_text || concept_name`, `definition = concept_explain`, plus `canonical-lib` / `canonical-ref` / `status` properties declared at the top. `$lookup` branches: LOCAL_CS_URL → local Concept lookup; CanonicalLib URL/name → delegate to `app.termbank_client.lookup(lib_name, code)`; unknown system → 404 without touching termbank. Imports `resolve_canonical_lib` from `fhir_valueset` for consistency. |
| `planp/app/__init__.py` | Registered `fhir_codesystem_bp` at `/api/v1` after the ConceptMap blueprint. |
| `planp/tests/test_fhir_codesystem.py` (NEW) | 20 tests: read (5 — shape + D1 guid-as-code + display + canonical-property + R5 model validation), search Bundle (3), local $lookup (5 — guid hit, property shape, 404 unknown, missing-params, escaped `%24`), termbank delegation (4 — URL-form delegates with lib NAME, name-form delegates, miss returns 404 with "unreachable" hint, unregistered system 404 WITHOUT calling termbank), POST (3). Termbank tested via `patch.object(app.termbank_client, 'lookup', ...)`. |
| `planp/progress.md` | §6.3 section appended. Test count 169 → 189. |

## 2026-06-22 — FHIR R5 terminology profile §6.7 + §6.8: CapabilityStatement truth-up + conformance scaffolding

| File | Change |
|------|--------|
| `planp/app/api/capability.py` | ENDPOINTS list extended with the 15 new FHIR routes (ValueSet/CodeSystem/ConceptMap reads/searches/operations). PlanDefinition `$expand` description clarified ("NOT the FHIR ValueSet $expand"). FHIR CapabilityStatement `resource[]`: rewrote ValueSet entry (two surfaces, $expand + $validate-code with cdr.pdhc/scoped dual-mode doc), rewrote CodeSystem entry (single local `plan-pdhc-local`, $lookup with termbank delegation doc), ADDED ConceptMap entry (single platform `plan-pdhc-canonical-bindings`, $translate, Risk §9.5 match-shape note). Added an explicit §7 non-goals documentation block declaring `$subsumes`, is-a / descendant filters, and hierarchical properties as deliberately unsupported. |
| `planp/tests/test_capability.py` | +6 §6.7 tests: ValueSet declares expand + validate-code with both mode docstrings; CodeSystem declares lookup with termbank-delegation doc; ConceptMap exists with translate; §7 non-goals documented; new FHIR routes appear in `/endpoints`; PlanDefinition `$expand` doc warns it's NOT terminology. |
| `planp/Makefile` (NEW) | `test`, `corpus`, `conformance`, `check-jar` targets. `conformance` runs HL7 R5 `validator_cli.jar` against the emitted corpus; jar location via `VALIDATOR_JAR` env (default `~/.local/share/fhir/validator_cli.jar`); `check-jar` points the operator to the release download. |
| `planp/tests/conformance_corpus_emit.py` (NEW) | Boots a self-contained Flask test app, seeds a minimal dataset (CanonicalLib + Concept + ValueSet + ValueCatalogs), and calls every §6 FHIR endpoint to dump 13 representative JSON resources to `tests/fhir_corpus/`. End-to-end smoke-tested in this session. |
| `planp/tests/fhir_corpus/README.md` (NEW) | How to run `make corpus` / `make conformance`, where to download the jar, two-layer validation rationale (D5 fast pydantic + D5 slow Java). |
| `planp/progress.md` | §6.7+§6.8 section appended; §6 implementation marked COMPLETE. Test count 189 → 195. |

## 2026-06-22 — Documentation review (post-§6)

| File | Change |
|------|--------|
| `plan_pdhc_fhir_terminology_profile_instruction.md` | Status line updated: Specification → **IMPLEMENTED 2026-06-22**. Added pointers to ADR and progress.md for landing details. |
| `readme.md` | Added a bullet to "What this service does" describing the conformant FHIR R5 terminology profile with links to the spec + ADR. |
| `planp/docs/api_reference.md` | 44 URL-prefix fixes (`/api/v1/X` → `/api/v1/lookup/X`) across canonical-libs / concept-types / response-types / units / plandef-types / intended-uses / valuesets / values — same stale-prefix bug we caught in tests, root cause is commit `00440b7`. Added a forward-link note at the top of the ValueSets section. Added a "NOT the FHIR ValueSet $expand" warning on the PlanDefinition $expand block. Added a new ~140-line "FHIR R5 Terminology Profile" top-level section covering all new routes, D3 canonical URL convention, D3.b legacy URL acceptance, termbank delegation, dual-mode $validate-code, explicit §7 non-goals, and conformance toolchain. |
| `plan_description.md` | Added `app/api/fhir_valueset.py` + `fhir_codesystem.py` + `fhir_conceptmap.py` + `fhir_helpers.py` to the source-files preamble. Added a new "§9) FHIR R5 terminology profile (added 2026-06-22)" section summarising the three new resources, the two preserved regression contracts (legacy CRUD + cdr.pdhc shim), and links to the spec + ADR. |
| `DEPLOYMENT_PLAN.md` | Requirements example block extended with `Flask-Cors>=4.0`, `openpyxl>=3.1`, `fhir.resources>=8.0` (the latter is the new §6.8 D5 dep). Added an upgrade callout for existing deployments noting that no migration is needed. |
| `newtask.txt` (NEW) | Required per Rule 2 but absent. Captures: §6 done; next-up = CI conformance job + 3 ADR open questions + server pip-install refresh. |
| `planp/app/api/capability.py` | `DOCS_CATALOG` extended with `plan_pdhc_fhir_terminology_profile_instruction.md` and `plan_pdhc_fhir_terminology_profile_DECISIONS.md` so both are discoverable via `GET /api/v1/docs` and downloadable via `GET /api/v1/docs/<filename>` (the existing `_resolve_doc_path` already searches the project root, so no path-resolution change needed). Verified end-to-end. |
| `planp/progress.md` | Documentation-review section appended. |

## 2026-06-23 — post-deploy work (6 commits after the §6 ship)

| File | Change | Commit |
|------|--------|--------|
| `planp/app/api/capability.py` | FormDefinition resource block removed (not a real FHIR resource type — failed conformance binding); security.service simplified to text-only CodeableConcept (HL7 restful-security-service URL unresolvable offline by HL7 validator). | bb52910 |
| `planp/app/api/fhir_codesystem.py` + `planp/app/api/fhir_conceptmap.py` + `planp/app/api/fhir_valueset.py` | bdl-18 self link added to all 3 searchset Bundle responses; ConceptMap.sourceScopeUri dropped (R5 requires it to reference a ValueSet, plan.pdhc has no covering ValueSet — `group[].source` already identifies the source CodeSystem per group). | bb52910 |
| `planp/Makefile` | `make conformance` target uses HL7 validator_cli.jar with `-tx=https://tx.fhir.org/r5`. | bb52910 |
| `planp/tests/test_fhir_conceptmap.py` | `TestReadConceptMap::test_resource_shape` inverted to assert `sourceScopeUri NOT in body`. | bb52910 |
| `.github/workflows/conformance.yml` (NEW) | CI workflow: triggers on push/PR to main + paths-filtered to terminology surface; caches `validator_cli.jar` v6.9.10; runs `make corpus && make conformance` against the corpus. Drops literal `~` from `VALIDATOR_JAR` env (Makefile's `$(HOME)/...` is correct). | 090cc8b + 1710546 |
| `plan_pdhc_fhir_terminology_profile_DECISIONS.md` | ADR D6/D7/D8 resolved (the three previously-deferred open questions). D6 locks the `concept[].property.uri` scheme as `{LOCAL_CS_URL}#{property-code}`. D7 confirms multi-group ConceptMap is the design. D8 confirms POST $validate-code body shape is FHIR-clean (no cdr.pdhc legacy constraints). | ccbbf15 |
| `planp/app/api/fhir_codesystem.py` | `CODESYSTEM_PROPERTY_DEFS` now carries `uri` per property (D6 wired). The 3 properties — canonical-lib, canonical-ref, status — get URIs at `{LOCAL_CS_URL}#{code}`. Verified live at `https://plan.pdhc.se/api/v1/CodeSystem/plan-pdhc-local`. | ccbbf15 |
| `planp/app/api/plandefinitions.py` | `list_plandefinitions` filters out archived plandefs by default; `?include_archived=1` opts back in. Was a prod-only edit before, now reconciled. | 57b239d |
| `planp/app/models/fhir_models.py` | `PlanDefinition.to_dict()` emits the `archived` boolean. Was prod-only before, now reconciled. | 57b239d |
| `planp/docker-compose.yml` | `pdhc_db` port mapping `9031:5432` → `127.0.0.1:9031:5432` (CLAUDE.md §3 loopback bind). Was prod-only before, now reconciled. | 57b239d |
| `planp/tests/test_forms.py` (NEW) | 8 characterization tests for `/api/v1/forms*` (catalogue, versions, produce, publish, immutability — auth gates + broad shape). | f57020b |
| `planp/tests/test_form_definitions.py` (NEW) | 14 characterization tests for `/api/v1/form-definitions*` (all 10 routes auth-gated; SSO happy paths). | f57020b |

## 2026-06-24 — /api/v1/docs serving fix (ticket #273)

| File | Change |
|------|--------|
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/.dockerignore` | NEW. Keeps the build context small now that it covers the whole repo: excludes venvs, node_modules, .git/, db_backups, *.docx, *.pdf, secrets, IDE/macOS noise. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/Dockerfile` | Build context moved to repo root. All previous COPYs re-prefixed with `planp/`. Added explicit COPY for the 10 root-level cataloged .md files into `./docs/` so `/api/v1/docs/<filename>` resolves inside the image. Plus `COPY readme.md ./docs/readme.md` for the case mismatch between Git-tracked `README.md` and on-disk lowercase. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docker-compose.yml` | `context: .` → `context: ..`, `dockerfile: Dockerfile` → `dockerfile: planp/Dockerfile`. Dropped the `../:/project-docs:ro` volume mount (silently empty in prod because Colima's `default` profile virtiofs-mounts only `/Users/miserver`). |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/main.py` | Deduplicated the second `DOCS_CATALOG` dict by importing from `app.api.capability`. The drifted local copy listed sso_* docs the API didn't and missed the two terminology-profile docs the API added. Single source of truth. |
