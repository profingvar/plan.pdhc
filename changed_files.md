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

## 2026-06-30 — Rollup #325 surgical pass

| File | Ticket | Note |
|------|--------|------|
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/static/src/agentation-loader.jsx` | #335 | Moved from repo-root `planp/agentation-loader.jsx`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/static/src/BUILD.md` | #335 | Three-line esbuild rebuild note for the moved jsx. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_plandefinitions.py` | #333 | Deleted `POST /api/v1/PlanDefinition` 501 stub. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_plandefinitions.py` | #333 | `test_post_returns_501` → `test_post_returns_405` (Flask's default). |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/config.py` | #327 + #337 | Dropped JWT_SECRET_KEY / JWT_ACCESS_TOKEN_EXPIRES / JWT_REFRESH_TOKEN_EXPIRES + `from datetime import timedelta`; fixed SSO_CALLBACK_URL default to `…/api/v1/auth/callback`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/__init__.py` | #327 | Removed `flask_jwt_extended` import, `jwt = JWTManager()`, and conditional `jwt.init_app(app)` block. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/requirements.txt` | #327 | Dropped `Flask-JWT-Extended>=4.6`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env.example` | #327 + #337 | Removed `JWT_SECRET_KEY=`; appended SSO_BASE_URL / SSO_CLIENT_ID / SSO_CLIENT_SECRET / SSO_CALLBACK_URL block with AUTH_DISABLED note. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/concept_models.py` | #329 | `ValueSet.to_dict` and `Concept.to_dict.valueset_url` now emit `/api/v1/lookup/valuesets/{guid}`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_lookup_url_consistency.py` | #329 | NEW. Two tests asserting both serializers emit `/api/v1/lookup/`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/concepts.py` | #330 | `update_concept` now bumps `date_valid` alongside `vers_number`. Added `from datetime import datetime, timezone`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_concepts.py` | #330 | NEW test `test_update_bumps_date_valid` asserting strict-greater on `date_valid`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/README.md` | #339 | "Running locally" rewritten to `./start.sh` + curl health; added "How loopback-only exposure works" paragraph. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/DEPLOY_2026-06-22_FHIR_TERMINOLOGY.md` | #340 | "What was NOT done" items #2 and #3 marked RESOLVED 2026-06-23 with commit refs. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/.github/workflows/conformance.yml` | #340 | `paths:` broadened to include `fhir_service.py`, `app/__init__.py` (for both push and PR triggers). |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/plan_pdhc_fhir_terminology_profile_instruction.md` | #340 | §2 "no automated tests" + §4 "unenforced" framing replaced with the live 222-test pytest reality. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/.github/workflows/test.yml` | #341 | NEW. pytest CI on every push + PR, Python 3.14, `pytest tests -x -q --maxfail=3`. |

## 2026-06-30 — Rollup #325 design pass

| File | Ticket | Note |
|------|--------|------|
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/__init__.py` | #328 | `Limiter(default_limits=['200/minute'])`, `RATELIMIT_DEFAULT` set, `@limiter.exempt` on `/api/health`, global `request_filter` for service-key bypass. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/auth.py` | #328 | Removed blueprint-level `limiter.limit("200/minute")(auth_bp)` no-op. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/dispatch.py` | #328 | Removed blueprint-level limiter.limit no-op. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/form_definitions.py` | #328 | Removed blueprint-level limiter.limit no-op. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/forms.py` | #328 | Removed blueprint-level limiter.limit no-op. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_plandefinitions.py` | #328 + #332 | Removed limiter.limit no-op; imported `fhir_canonical_url` and switched bundle `fullUrl` + read-handler `url` defaults to it. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/plandefinitions.py` | #328 | Removed blueprint-level limiter.limit no-op. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/lookup_tables.py` | #328 | Removed blueprint-level `limiter.limit(..., exempt_when=_service_caller)`; the exempt-when semantics are now global. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/concepts.py` | #328 | Removed blueprint-level `limiter.limit(..., exempt_when=_service_caller)`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_rate_limit.py` | #328 | NEW. Asserts 201st request to `/api/v1/lookup/units` returns 429 and the exempt endpoints don't. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/capability.py` | #326 + #328 | Auth block rewritten to advertise the real GET routes + service-key bypass description; rate-limit advertisement rewritten to reflect global default + exempts; `@limiter.exempt` on `/capability-statement`, `/metadata`, `/endpoints`; all lookup-bucket endpoint paths corrected to `/lookup/...` prefix. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_capability_truth.py` | #326 | NEW. Walks /capability-statement response and asserts every advertised endpoint resolves; checks SSO model + truthful rate-limit block. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_codesystem.py` | #331 | New `_codesystem_version()` helper using `max(Concept.vers_number)`; CodeSystem `version` + $lookup `version` derive from it. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_conceptmap.py` | #331 | New `_conceptmap_version()` helper using `max(Concept.vers_number)` filtered to bound rows; ConceptMap `version` derives from it. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/plan_pdhc_fhir_terminology_profile_DECISIONS.md` | #331 | D4 "TBD" carve-out replaced with the RESOLVED 2026-06-30 derivation rule for CodeSystem and ConceptMap. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_version_uniform.py` | #331 | NEW. 6 tests: CodeSystem version from max(vers_number); ConceptMap version from max bound vers_number; both never empty. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/fhir_service.py` | #332 | `url` builder uses `fhir_canonical_url('PlanDefinition', fhir_id)`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_plandefinition_canonical_url.py` | #332 | NEW. 3 tests asserting PlanDefinition URL uses `{PLAN_BASE}/fhir/PlanDefinition/<id>` shape, never the legacy `pdhc.se/PlanDefinition/<id>`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env.example` | #336 | `POSTGRES_DB`/`DATABASE_URL` default now `pdhc_gateway` with explanatory comment about legacy name retention. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/config.py` | #336 | `SQLALCHEMY_DATABASE_URI` default DB renamed to `pdhc_gateway` with explanatory comment. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/db_schema_snapshot.md` | #336 | `**Database:** pdhc_planp` → `pdhc_gateway (legacy name)`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/DEPLOYMENT_PLAN.md` | #338 | Full rewrite — container-based deploy, pdhc_gateway DB, SSO model, no JWT, no ghost scripts. ~140 lines. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/SSO_INTEGRATION_PLAN.md` | #338 | Full rewrite — H1-H4 handshake, per-request revalidation, service-key bypass, config keys. ~110 lines. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/plan_description.md` | #338 | §6 key order corrected; §7.1 auth rewritten to SSO model + global 200/min default; §7.2 paths now use `/api/v1/lookup/`. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docs/api_reference.md` | #338 | Auth section rewritten: SSO redirect handshake, per-request revalidation, service-key bypass; rate-limit block updated. |
| `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_docs_serving.py` | #338 | NEW. Asserts `DEPLOYMENT_PLAN.md` is NOT in `DOCS_CATALOG` (already true) — pins the contract going forward. |

## 2026-07-07 — M0 #421: plan adopts reform session_phases (consistency)
- planp/app/api/auth.py — _phases() helper (session_phases w/ effective_phases
  fallback) at the planning gate. No org filter (Plan is orthogonal).
- planp/app/tests/test_reform_phases.py — NEW, 4 tests.

## 2026-07-31 — epic #516 Guided PlanDef authoring assistant (opt-in, Claude-assisted)
- planp/app/config.py — EDIT. AUTHORING_ASSISTANT_ENABLED (default false), ANTHROPIC_API_KEY, ANTHROPIC_API_BASE, AUTHORING_ASSISTANT_MODELS allowlist + DEFAULT_MODEL + MAX_TOKENS + TIMEOUT.
- planp/.env.example — EDIT. Documented the opt-in assistant block (default off, blank key).
- planp/app/__init__.py — EDIT. Register authoring_bp at /api/v1 (before the termbank client init).
- planp/app/services/plandef_validation.py — NEW (#517 GA-1). Deterministic Layer-1 validators (validate_concept / validate_plandef / summarise); 9 invariant codes; termbank optional/injected; no LLM, no required network.
- planp/app/services/plandef_assistant.py — NEW (#518 GA-2). Claude Messages API wrapper; selectable model allowlist; search-first reuse candidates; self-check via GA-1; graceful degradation (never raises); no PHI sent.
- planp/app/api/authoring.py — NEW (#519 GA-3). Opt-in blueprint: GET /authoring/models, POST /authoring/validate, POST /authoring/assist; @requires_role('read_write'); disabled -> {"enabled": false}.
- planp/tests/test_plandef_validation.py — NEW. 16 tests, one per invariant incl. the API-bypass (choice-without-valueset) case.
- planp/tests/test_plandef_assistant.py — NEW. 7 tests; HTTP mocked (disabled/no-key/bad-model/happy/malformed/http-error/unknown-unit).
- planp/tests/test_authoring_api.py — NEW. 6 tests; blueprint wiring + disabled-flag + auth gate.
- planp/docs/plandef_authoring_assistant_design.md (+ .docx) — NEW (#522 GA-6). Offline design rationale.
- plan_description.md — EDIT. New §10 "Guided authoring assistant (optional, #516)" — user-facing manual section.
- planp/docs/api_reference.md — EDIT. New "Authoring Assistant" endpoint section (models/validate/assist) + summary total 82->85.
- planp/app/api/capability.py — EDIT. DOCS_CATALOG: registered plandef_authoring_assistant_design.md so it's served via /api/v1/docs.
- planp/app/services/plandef_validation.py — EDIT (post-deploy fix). Recognise prod response-type names absent from RESPONSE_TYPE_MAP ('numerical'->numeric, 'Free text'->text) so they aren't wrongly flagged E-RESPONSE-TYPE-UNKNOWN; require a unit only for numeric (quantity), not slider/integer (dimensionless).
- planp/tests/test_plandef_validation.py — EDIT. +3 tests for the prod vocabulary aliases + slider-no-unit.
- planp/docs/plandef_authoring_assistant_design.md (+ .docx) — EDIT. §4 table wording for the unit rule + alias handling.
- planp/app/static/js/authoring_assistant.js — NEW (#520 GA-4). Self-contained opt-in Check/Assist panel; calls /api/v1/authoring/{models,validate,assist}; renders only when enabled; Assist hidden without a key; "Apply to form" = reviewed draft.
- planp/app/templates/concepts/create.html — EDIT. Mount div + script include.
- planp/app/templates/concepts/edit.html — EDIT. Mount div + script include.
- planp/app/templates/plandefinitions/builder.html — EDIT. Plandef Check mount + script include.
- planp/tests/test_authoring_ui.py — NEW. Renders the 3 templates; asserts mount + script present.
- planp/app/config.py — EDIT (#523). ROSETTA_BASE_URL + ROSETTA_SERVICE_KEY (both unset = button degrades to rosetta_not_configured).
- planp/app/api/authoring.py — EDIT (#523). POST /authoring/openehr-realisable proxy to rosetta; graceful degradation.
- planp/app/static/js/authoring_assistant.js — EDIT (#523). "Check openEHR export" button + realisable/pending/unmapped renderer in the builder panel.
- planp/tests/test_authoring_api.py — EDIT (#523). +4 proxy tests (disabled/not-configured/forwards/unreachable).

## 2026-08-01 — #521 GA-5 fail-closed enforcement
- planp/app/services/save_guard.py — NEW. SaveBlocked + guard_concept/guard_plandef; errors block, warnings pass, admin override_validation (audited to log), PLANDEF_VALIDATION_ENFORCED kill-switch.
- planp/app/config.py — EDIT. PLANDEF_VALIDATION_ENFORCED (default true).
- planp/app/api/concepts.py — EDIT. guard_concept on create + update (422 on block).
- planp/app/routes/concepts.py — EDIT. guard_concept on web create + edit (supersedes the single-choice-only check; flashes issues).
- planp/app/api/plandefinitions.py — EDIT. guard_plandef on create + update (422 on block) + _plandef_validate_payload helper.
- planp/app/routes/plandefinitions.py — EDIT. guard_plandef on web builder create.
- planp/tests/test_save_guard.py — NEW. 7 tests (block/valid/admin-override/nonadmin/kill-switch/warning/plandef-dangling).
- planp/tests/conftest.py — EDIT. PLANDEF_VALIDATION_ENFORCED off by default in tests (enforcement suite opts in).
- planp/.env.example, planp/docs/plandef_authoring_assistant_design.md — EDIT. Document the flag + status.

## 2026-08-06 — #526 response_type vocabulary hardening (audit follow-up)
- planp/app/services/forms_service.py  (RESPONSE_TYPE_MAP: explicit 'numerical'->numeric, 'free text'->text; no output change — heuristic fallback already resolved both)
- planp/tests/test_response_type_map.py (new — pins response_type->question_type->FHIR item for prod vocab; regression guard "free text is never numeric")

## 2026-08-06 — #530 Transfer page (promote synthetic cdr_6 → working CDR; thin proxy to cdr_6 #529)
- planp/app/config.py — add CDR6_BASE_URL / CDR6_SERVICE_KEY / CDR6_TIMEOUT / CDR_TRANSFER_TARGETS.
- planp/app/api/transfer.py (new) — transfer_bp under /api/v1: GET /transfer/targets, POST /transfer/preview (dry_run), POST /transfer/execute. @requires_role('read_write'). _call_cdr6() proxies cdr_6 POST /api/v1/transfer as X-Source-Service: sim.pdhc (cdr_6 sim-only, Rule 2); degrades gracefully (503 not-configured / 502 unreachable). execute audit-logged (user/to/run/purge/outcome).
- planp/app/routes/transfer.py (new) — transfer_web_bp: GET /transfer @sso_login_required → render transfer.html.
- planp/app/templates/transfer.html (new) — read-only cdr_6 source, to-CDR select (loaded from /targets), run-id, Preview(dry-run)→count, Execute (disabled until preview for the current selection), purge checkbox + confirm(), results panel. Vanilla JS, same-origin fetch.
- planp/app/templates/base.html — nav: add Transfer link (before Docs).
- planp/app/__init__.py — register transfer_bp (/api/v1) + transfer_web_bp.
- planp/.env.example — document CDR6_* + CDR_TRANSFER_TARGETS.
- planp/tests/test_transfer.py (new) — 12 tests: auth gate (unauth 401/403, analysis-only 403, SU allowed), targets configured/unconfigured, preview proxies dry_run + sim.pdhc headers, unknown-dest/missing-to 400, execute proxies real + purge/batch passthrough, unconfigured 503, unreachable 502, page renders. Full suite 320 passed.

## 2026-08-06 — #525 doc currency
- README.md — health path /api/v1/health -> /api/health (v1 404s; matches CLAUDE.md port table).
- progress.md — #516 block: mark GA-4/GA-5 DEPLOYED (supersede the stale "Not deployed — local build only"); note ANTHROPIC_API_KEY unset (Layer-2 dormant, #527). newtask.txt already current (rewritten for #530).
- plan.pdhc/planp/docs/technical.md (Port Allocation section)
- plan.pdhc/tools/load_catalogue.py (NEW — one-file bulk loader: concepts + valuesets + values)
- plan.pdhc/tools/example_catalogue.yaml (NEW — example manifest)
- plan.pdhc/tools/README.md (NEW — loader usage)
- plan.pdhc/tools/concept_import_template.csv (NEW — flat concept CSV + optional valueset column)
- plan.pdhc/tools/valueset_import_template.csv (NEW — one row per choice option)
- plan.pdhc/tools/load_catalogue.py (--from-csv mode added)
- plan.pdhc/tools/eq5d5l_concepts.csv (NEW — EQ-5D-5L 5 dimensions + VAS slider)
- plan.pdhc/tools/eq5d5l_valuesets.csv (NEW — 25 response levels, 5 valuesets)
- plan.pdhc/tools/asthma_home_monitoring_concepts.csv (NEW — 9 asthma monitoring concepts; FEV1 reused; applied prod)
- plan.pdhc/tools/asthma_baseline_characteristics_concepts.csv (NEW — 11 baseline concepts; reuse height/weight/bmi/smoking_status; built, not yet applied)
- plan.pdhc/tools/asthma_baseline_characteristics_concepts.csv (gina-step + inhaler-device -> coded Single choice; feno unit=ppb; APPLIED prod)
- plan.pdhc/tools/asthma_baseline_valuesets.csv (NEW — GINA 1-5 + 6 inhaler device types)
- plan.pdhc/tools/asthma_home_monitoring_plandef.json (NEW — reproducible spec; PlanDefinition applied active to prod guid febf8ec1)

- planp/app/api/concepts.py — accept `limit` as alias for `per_page` (silent-50 default fix). Deployed 2026-08-15 (pdhc_app rebuild).
- .env APP_VERSION=98bf711 — populate health `version` (was "dev"). 2026-08-15.

## 2026-10-05 — retire loader.pdhc
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/auth.py — loader.pdhc removed from KNOWN_SERVICES.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/config.py — PLAN_LOADER_SERVICE_KEY no longer read into config.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/capability.py — known_sources no longer advertises it.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/concepts.py — comment updated.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docs/technical.md — three references marked retired.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/tools/load_catalogue.py — marked RETIRED; kept for the wire format.
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_loader_identity_retired.py — NEW, 3 tests.
- planp/app/services/dispatch_service.py (#771 — match a contract topic under either identifier)
- planp/tests/test_dispatch_both_ids.py (#771)

## 2026-10-07 — #786 plan.pdhc reform
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/dashboard.html
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/static/css/pdhc.css
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/canonical_libs.py   (NEW)
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/routes/concepts.py
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/concepts.py
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/services/concept_importer.py
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/concepts/create.html
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/templates/concepts/edit.html
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/capability.py
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/db_schema_snapshot.md   (REGENERATED)
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/scripts/gen_db_schema_snapshot.py   (NEW)
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_assume_local_786.py   (NEW)
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_docs_serving.py

## 2026-10-07 — #786 item 4: /transfer retired
| 2026-10-07 | planp/app/api/transfer.py | DELETED — the cdr_6 proxy |
| 2026-10-07 | planp/app/routes/transfer.py | DELETED — the page route |
| 2026-10-07 | planp/app/templates/transfer.html | DELETED |
| 2026-10-07 | planp/app/__init__.py | both transfer blueprints unregistered |
| 2026-10-07 | planp/app/config.py | CDR6_* + CDR_TRANSFER_TARGETS removed, tombstoned |
| 2026-10-07 | planp/app/templates/base.html | Transfer nav link removed |
| 2026-10-07 | planp/.env.example | CDR6 block tombstoned (ROSETTA_SERVICE_KEY over-deleted and restored) |
| 2026-10-07 | planp/tests/test_transfer.py | DELETED (12 tests asserting the feature worked) |
| 2026-10-07 | planp/tests/test_transfer_retired.py | NEW — 8 guards, incl. a stale-env reload check |
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docs/user_manual.md
/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docs/technical.md
- 2026-10-12 (DATA, not code) concepts.FEV1 range_low=0.3 range_high=7.0 — applied via guard_concept in-container
- 2026-10-13 planp/app/config.py — _require_secret_key(): required in production, random in dev, never 'change-me'
- 2026-10-13 planp/tests/test_secret_key_required.py (NEW)
- 2026-10-13 planp/app/config.py — _require_database_url() (refuses the published dev URL AND an empty password); _session_cookie_secure() + HttpOnly/SameSite=Lax
- 2026-10-13 planp/tests/test_database_url_and_cookies.py (NEW)
- 2026-10-13 planp/.env.example — DATABASE_URL/FLASK_SECRET_KEY marked required; SESSION_COOKIE_SECURE escape hatch documented
- 2026-10-13 planp/migrations/versions/e5a6b7c8d901_add_missing_guid_fks.py (NEW) — #787.1: FKs on 3 of the 4 unenforced GUID columns; 4th recorded as deliberately unenforced
- 2026-10-13 planp/tests/test_plandefinition_two_guids.py (NEW) — #771: pins the 1:1 invariant behind the decision NOT to merge guid and fhir_id

## 2026-10-15 — #708 sibling smoke
- planp/deploy/smoke_siblings.py  (NEW: 10 read-only checks against sso, contract, termbank, rosetta)

## #839 — derive the FHIR publication status; constrain Concept.status (2026-10-19)

- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_helpers.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_codesystem.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_conceptmap.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/fhir_valueset.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/migrations/versions/a1b2c3d4e5f6_839_concept_status_check.py (new)
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_publication_status.py (new)
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_codesystem.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_conceptmap.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_fhir_valueset.py
- planp/app/api/fhir_helpers.py + fhir_codesystem.py + fhir_valueset.py + fhir_conceptmap.py + api/concepts.py + models/concept_models.py + migrations/versions/b2c3d4e5f6a7_841_drop_concept_status_check.py + tests/test_fhir_publication_status.py + tests/test_fhir_{codesystem,conceptmap,valueset}.py — Ticket #841, operator decision 2026-10-20: **Concept.status is not meant to gate adoption**, i.e. the ticket's answer (2), status is vestigial. So it is retired rather than promoted. `derive_publication_status` and `CONCEPT_STATUSES` deleted from fhir_helpers and replaced by `RESOURCE_PUBLICATION_STATUS = 'active'`, documented as a property of the RESOURCE (published, served, and validating every CDR write through the canonicaliser's plan-Concept tier, with ten concepts behind ~41,000 observations on cdr1/cdr2/cdr3) rather than a fold over per-concept editorial state. This reverts #839's derivation, which was the wrong fix: it made a required FHIR field depend on a column nothing could change, so CodeSystem + 12 ValueSets + ConceptMap all advertised `draft` permanently — worse than the constant it replaced, because a permanent value looks like information. Also removed: the per-concept `status` property from the CodeSystem property list and from both concept-property builders (it advertised "Concept editorial status (draft, active, retired)", an editorial lifecycle that does not exist); `status` from the POST constructor and from the PUT `direct_fields` tuple, so the field is no longer writable; `'status'` from `Concept.to_dict()`. The COLUMN IS DELIBERATELY KEPT — it holds one distinct value so dropping it loses no information, and keeping it avoids an irreversible migration on the platform's semantic authority; it carries a comment saying it is retired and must not be read. New migration drops only the #839 CHECK constraint, since a constraint on a field nothing reads or writes is machinery guarding nothing; reversible in both directions. `fhir_valueset.py` also lost its now-unused `db` and `Concept` imports, and its module docstring (which still described the pre-#839 constant) was corrected to say why the constant is back. Tests: `test_fhir_publication_status.py` rewritten from pinning the derivation to pinning the inverse — each resource reports `active`, the status does NOT move when a Concept's status is driven through draft/active/retired/junk (the test that distinguishes this from the pre-#839 hardcoded literal), the CodeSystem advertises no `status` property, no concept emits one, `to_dict()` has no `status` key, and POST/PUT cannot set it. 399 tests green. NOT DEPLOYED at the operator's request.

## 2026-10-21 — #851 whole_system_answer_space (icd11.pdhc option B)
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/models/concept_models.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/terminology.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/migrations/versions/c3d4e5f6a7b8_whole_system_answer_space.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_terminology.py

## 2026-10-30 — #854: the bare DSN, and a test for the files we actually deploy

Edited:

- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/docker-compose.yml` — line
  39, `DATABASE_URL=postgresql://` → `postgresql+psycopg2://`. Safe today only
  because `requirements.txt:52` pins `SQLAlchemy==2.0.52`; from 2.1 a bare
  scheme resolves to psycopg v3, which is not installed, and the service
  crash-loops on `ModuleNotFoundError: No module named 'psycopg'`. cdr.pdhc
  walked into this on 2026-10-21 (#853) by bumping the pin with bare DSNs.
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env.example` —
  `COMPOSE_PROJECT_NAME=planp` added, with why. Production already pins it;
  only the repo lacked it. The value is **not** free: the live volume is
  `planp_pdhc_pgdata`, so any other value would orphan the data.
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_database_url_and_cookies.py`
  — three tests on the files this repo would DEPLOY, which is where #854 lived.
  Every existing test in that file checks what `_require_database_url()` does
  with a value it is handed; none looked at the compose file or the example.
- `/Users/martiningvar/T7_sidewinder/plan.pdhc/planp/.env` (gitignored, local
  dev only) — same scheme fix.

Verified: 409 passed. The new test was proved to FAIL — the defect was
reintroduced, `test_the_COMPOSE_file_names_the_postgres_DRIVER` went red with
an actionable message, then the file was restored and it went green again.

NOT changed, and worth knowing why:

- **Production was already correct**, as in #858. The deployed
  `/usr/local/www/plan.pdhc/planp/docker-compose.yml:39` has `+psycopg2` and
  the deployed `.env:28` pins `COMPOSE_PROJECT_NAME=planp`. The repo was the
  divergence, and the repo is what a fresh deploy would use.
- **The ticket's item 3 is disproved.** It worried the deployed container might
  publish on `0.0.0.0:9030`. It does not: `127.0.0.1:9030`.
- **Three of the four bare `postgresql://` hits in this repo are not defects.**
  `app/config.py:106` is a docstring describing a URL;
  `scripts/gen_db_schema_snapshot.py:30` strips `+driver` deliberately, because
  `psycopg2.connect()` cannot parse a SQLAlchemy scheme;
  `tests/test_database_url_and_cookies.py` uses the bare form as test input.
  Only the compose line was real.

DEPLOYED `.env:4` — **done 2026-10-30**, after the above was written as an
operator item. It held the last bare DSN on the box for this service. Inert at
the time, because compose `environment:` overrides `env_file` — which is
exactly what made it a two-step trap: delete that compose line as a
"duplicate" and the bare DSN becomes live, then the next SQLAlchemy bump
crash-loops plan.

Done surgically, since the file is 600 and holds a credential: backup first to
`~/backups/predeploy/plan.pdhc/2026-10-30T20-41-55Z/env.before` (600, parent
700), then a single counted replacement. Asserted afterwards — exactly line 4
differed, 46 lines before and after, mode 600 unchanged, zero bare DSNs left.
Written through the same file rather than with `sed -i`, which would replace a
symlink with a regular file (it is a regular file here, but the habit is the
point).

Nothing restarted, and nothing needed to be: `pdhc_app` still shows
`StartedAt 2026-10-30T16:42:42Z`, its own `DATABASE_URL` is unchanged, and
`/api/health` is 200.

The proof that the trap is closed is a dry run, not the file itself —
`docker-compose config` now resolves **both** DSNs with the driver named:

```
DATABASE_URL: postgresql+psycopg2://...@db:5432/pdhc_gateway    (environment)
DATABASE_URL: postgresql+psycopg2://...@localhost:9031/...      (env_file)
```

## 2026-10-31 — #857 (c): a whole-system TRUE is an ADOPTION statement, not existence

Edited:

- `planp/app/api/terminology.py` — the `whole_system` TRUE branch's message now
  says outright that it is an adoption statement and **NOT** a membership test,
  that it does not assert the code exists, who does check existence
  (icd11.pdhc, against WHO's `codeinfo` at entry), and where to read why
  (#857). The `validate_code` docstring carries the same with the measurement
  (`icd11-mms&code=ZZ-nonsense` → true; `icd10&code=A00.9` → false as the
  control) and names the exposure it leaves open.
- `plan_pdhc_fhir_terminology_profile_instruction.md` — §2.2 gained the same,
  as a table, because that section is what a caller reads before wiring to this
  endpoint.
- `planp/tests/test_terminology.py` — two tests. One pins the message wording;
  until #857's option (a) exists the message **is** the compensating control,
  so it should not survive the next edit on goodwill. The other is its control:
  a measurement library's message must not pick up the new wording, because
  there a False answer really is a membership result.

Verified: 411 passed (was 409). The new test was proved to FAIL — the old
message was restored, `test_the_message_says_it_is_NOT_a_membership_test` went
red, the file was put back and it went green.

The hole itself is closed on the cdr side, not here: see cdr.pdhc for #857
option (b).

## 2026-11-01 — #872: the adoption rule is now readable, and ICD-10 is decided
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/app/api/capability.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/migrations/versions/d4e5f6a7b8c9_icd10_whole_system.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_adoption_granularity_872.py
- /Users/martiningvar/T7_sidewinder/plan.pdhc/planp/tests/test_terminology.py

Two halves of the operator decision #872 asked for.

**1. The rule was not discoverable.** The semantics have been right since
c3d4e5f6a7b8 and the message has been honest since #857, but measured
2026-11-01 **nothing outside this service read the `whole_system` boolean** —
zero readers in the whole workspace. A contract nobody can discover is a
contract nobody follows. It is now stated on BOTH capability surfaces, because
they have different readers: the FHIR CapabilityStatement at
`/api/v1/metadata` (what cdr.pdhc parses) and the human-readable index at
`/api/v1/capability-statement`. Documenting one would leave the other
advertising less than the truth.

The advertisement says three things on purpose: the rule, the REASON (~85 000
codes picked at the point of care — a rule without its reason gets
"simplified" away by the next reader), and what a caller should DO about it
("Read whole_system"). Each is a separate test.

**2. ICD-10 was deferred on a premise that is empty.** c3d4e5f6a7b8 left
`icd10` FALSE because it "is also used for non-diagnosis purposes in existing
plans, so flipping it is a separate editorial decision with its own blast
radius". Measured against PRODUCTION 2026-11-01:

    canonical_lib_name | concepts | values
    -------------------+----------+-------
    icd10              |        0 |      0

Nine libs exist; `local` (34/48), `loinc` (35/3), `snomed` (21/0) and `atc`
(9/0) carry everything. Nothing references icd10 at all. The concern was
reasonable as a category and false in fact.

Flipped rather than split. A second canonical lib for diagnoses only would
give the same ICD-10 code two possible canonical URIs depending on which lib
it came through, and cdr.pdhc deduplicates on `code_canonical` — so a
diagnosis would stop deduplicating against itself. One identifier per code
system is worth more here than purpose-purity.

**What this does NOT solve, recorded so nobody assumes it did:** the flag is
per-LIBRARY, so it accepts any ICD-10 code for any purpose. And that cannot be
fixed in the scoped path either — `scoped_validate_code` walks enumerated
`values_catalog` rows, so a ValueSet can say "one of these twelve codes" but
never "any code of this classification". Purpose-scoping a whole
classification is an open problem. Per-release acceptance is likewise
untouched (icd11.pdhc open item 19b).

**Two existing tests had to be rewritten, not deleted.**
`test_icd10_is_deliberately_NOT_whole_system` pinned the old decision; it is
now `test_icd10_IS_whole_system_per_872`, asserted against the MIGRATION FILE
because this suite runs on SQLite with `create_all` and never applies
migrations — so the fixture's flag value says nothing about what a deploy
does. And `test_a_MEASUREMENT_library_message_is_unchanged` used `icd10` as
its per-code example, which was always slightly wrong: ICD-10-SE is a
classification and faces exactly the mismatch the flag exists for. It now uses
`loinc`, which is what "MEASUREMENT library" means. A new
`test_a_MEASUREMENT_library_is_never_flagged` replaces the lost pin with the
drift that would actually hurt: flagging LOINC would accept any code ever
minted.

**A fixture of mine leaked and it looked like a code defect.** Flipping icd10's
flag in a session-scoped SQLite database changed the answer two tests in
test_terminology.py got, depending on file order. Both fixtures now restore the
previous value — and the test that inserts an icd10 Concept deletes it again,
because SQLite leaves foreign keys unenforced and an orphan row would survive
into other tests instead of failing loudly.

Controls proven by disabling the whole-system branch (`if False:`): 6 red
across the two files, including the new ICD-10 test. Restored: 42/42 for the
two files, **421/421** for the whole suite.

Migration applied, reverted and re-applied against real Postgres (local
`pdhc_db`): `icd10` f → t → f → t, `loinc` untouched at f throughout, head
`d4e5f6a7b8c9`. It prints its own premise when it runs
(`icd10 at upgrade: 0 concepts, 0 values_catalog rows`) rather than trusting
the measurement in its docstring — this database may not be the one that was
measured. **NOT deployed to production.**

## 2026-11-02 — #912: the service-key path is no longer role-blind
- planp/app/api/auth.py — KNOWN_SERVICES values become
  (config_var, granted_role); _service_key_outcome returns the ROLE, not True;
  requires_role compares it against min_role on BOTH branches, on the same
  scale (ROLE_LEVELS, now shared). hmac.compare_digest replaces `!=`.
  The docstring's `admin → is_su_admin` promise now holds on both paths.
- planp/tests/test_loader_identity_retired.py — the shape assertion updated;
  its intent (loader.pdhc retired, one entry) preserved.
- planp/tests/test_service_key_role_912.py (new) — 17 checks. 420 -> 438.

## 2026-11-03 — alert.pdhc added to KNOWN_SERVICES with read_write
- planp/app/api/auth.py — `'alert.pdhc': ('ALERT_PDHC_SERVICE_KEY',
  'read_write')`. Measured: all 12 write routes in lookup_tables.py are
  read_write, none is admin, and level 2 covers #913's read_only reads, so
  ONE grant suffices.
- planp/tests/test_loader_identity_retired.py — shape assertion updated.
- planp/tests/test_service_key_role_912.py — 4 checks on alert's grant,
  including that an UNSET key admits nobody (it will be unset until minted).

## 2026-11-03 — DEPLOYED (no local file changed by this entry)
- Deployed #912 + #913 + alert's grant in one rebuild of `pdhc_app`.
  Server path `/usr/local/www/plan.pdhc/planp`; only these three files copied:
  `app/api/auth.py`, `app/api/fhir_valueset.py`, `app/api/lookup_tables.py`.
  Image `31c64d407af7` → `6625c142138f`. Rollback tgz in
  `~/backups/predeploy/plan.pdhc/planp_2026-11-03T07-11-03Z.tgz`.
  Live probe: `GET /ValueSet` 200→401, `$validate-code` still 400 (not 401).

## 2026-11-03 — the allowlist entry had no wire to config
- planp/app/config.py — `ALERT_PDHC_SERVICE_KEY = os.environ.get(...)`.
  `api/auth.py:98` resolves the expected key through `current_app.config`,
  and config.py maps every variable BY HAND. Without this line the operator's
  `.env` entry would have had NO effect and alert would have been refused
  forever, with a correct-looking `.env`.
- planp/tests/test_service_key_config_wire.py — asserts every KNOWN_SERVICES
  variable reaches app.config, with sim.pdhc as the control. Proven to fail
  without the config.py line.
- DEPLOYED the same day: single-file scp + rebuild. Image
  `6625c142138f` → `4cf5c7341d59`. Per-file rollback at
  `~/backups/predeploy/plan.pdhc/config.py.2026-11-03T07-30Z.bak`.

## #875 — canonical_lib_url is unique, and the resolver refuses to guess (2026-11-04)

Step 1 (correct icd10's URL) was applied in production 2026-11-04 and closed
as #919. These are steps 2-4: the half that stops it recurring.

- planp/app/api/fhir_valueset.py — `resolve_canonical_lib` no longer does
  `.first()` on a non-unique column. It collects matches and RAISES the new
  `AmbiguousCanonicalLib` on more than one, for url and for name alike. The
  defect's shape is why: it answered CONFIDENTLY with the wrong library and
  nothing in the response said "ambiguous" — `$validate-code` returned FALSE
  for 89 correctly-stored ICD-10 codes, and `_build_compose` served them
  under the SNOMED CT system URI.
- planp/app/api/fhir_conceptmap.py — its byte-identical COPY of the resolver
  is DELETED; it now imports the original. The copy's own docstring said it
  "mirrors the lenience of" `fhir_valueset`'s, and it mirrored the defect
  too, so fixing one would have left the other silent. `fhir_codesystem`
  already imported the original, so conceptmap was the only duplicate.
- planp/app/models/concept_models.py — `canonical_lib_url` is now
  `unique=True`. Needed on the MODEL, not only in the migration, because the
  tests build their schema with `create_all()`.
- planp/migrations/versions/e5f6a7b8c9d0_unique_canonical_lib_url.py — NEW.
  Normalises `''` to NULL first (two empty strings collide under a UNIQUE
  where two NULLs do not), then REFUSES with both library names if any
  duplicate remains, rather than failing on a raw IntegrityError or picking
  — picking by row order is the defect itself. Head is now e5f6a7b8c9d0,
  verified a single head.
- planp/app/services/canonical_libs.py — `normalise_lib_url` and
  `url_conflict`. In this module because its own docstring is about being
  "the ONE place that decides it" so callers cannot drift; the same argument
  applies to the URL rule.
- planp/app/api/lookup_tables.py (create + update) and
  planp/app/routes/lookup_tables.py (create + update) — all FOUR write paths
  now check. This is where the production duplicate came from: every one of
  them already guarded `canonical_lib_name` for uniqueness, so the name was
  protected in two layers and the URL in none. No migration in the
  directory writes this column, so the value did not come from the
  migration history.
- planp/app/__init__.py — an app-level errorhandler returning 409 +
  OperationOutcome. Registered on the app rather than at each of the three
  resolver call sites, because #875's own lesson is that the resolver existed
  in two places and one would be forgotten. 409 and not 500: the server is
  working and refusing because its terminology data contradicts itself.
- planp/tests/test_canonical_lib_url_unique_875.py — NEW, 23 tests across
  all four layers, each refusal paired with an acceptance control.
  MUTATION-TESTED: reverting the resolver to `.first()`, dropping
  `unique=True`, dropping the blank normalisation, dropping `exclude_guid`,
  and giving conceptmap its own copy each fail exactly one test, and always
  the right one.

Two things the tests deliberately record rather than hide. The ambiguous
state is unreachable through the database once the constraint exists, so the
resolver's raise is exercised by injecting two rows at the query boundary —
honest about testing "if handed this, does it refuse" rather than "can the
database hold this". And the first injectivity test read whatever the
database happened to hold and failed with "no library has a URL" because it
ran after its fixtures; it now seeds its own four shapes, since a test whose
outcome depends on execution order is not evidence.

Suite: 491 passed. Migration branches verified on real Postgres in an
isolated scratch database (created and dropped): the healthy path normalises
one blank, finds zero duplicates, applies the constraint and keeps two NULLs
coexisting under it; the abort path finds the duplicate and names both
libraries.

### DEPLOYED 2026-11-04, and verified by behaviour rather than by status

Gated before anything was written. My git HEAD, the server disk and the
running container agreed on all seven files — so there was no server-side
edit to overwrite, AND the image was built from the current disk, which is
the "container can be ahead of the release dir" trap. `requirements.txt` is
16/16 pinned, so the `--build` was not also a dependency upgrade (#785).

Dump first: `~/backups/predeploy/plan.pdhc/pdhc_gateway.2026-11-04T13-4212Z.pgdump`
(131 481 bytes, mode 600, verified with `pg_restore -l`: 212 TOC entries, 44
tables, 22 with data). Per-file rollback pulled straight from the container
into `~/backups/predeploy/plan.pdhc/files.2026-11-04T13-4212Z/`.

Order was forced and happened to be the safe one: the migration file has to
be in the image, so the CODE went first. The constraint therefore never
existed without the 409 checks in front of it — the reverse order would have
left a window where a duplicate write 500'd.

    image 4cf5c7341d59 -> 67a6cd00670a   (docker-compose up -d --build --no-deps app)
    8 of 8 files hash-identical in the NEW image
    entrypoint.sh ran `flask db upgrade` on recreate; the migration logged its
      own premise: "[e5f6a7b8c9d0] no duplicates; adding uq_..."
    alembic d4e5f6a7b8c9 -> e5f6a7b8c9d0

Verified:

  - the constraint EXISTS: `uq_canonical_libs_canonical_lib_url UNIQUE
    (canonical_lib_url)`
  - it BITES. Reproducing #875 exactly — `UPDATE canonical_libs SET
    canonical_lib_url = <snomed's> WHERE canonical_lib_name='icd10'` — is now
    refused by Postgres. Run inside a transaction and rolled back; icd10's URL
    re-read afterwards and intact. That is the decisive test: the original
    defect is no longer expressible.
  - state preserved: 31 valuesets / 269 values / 270 memberships / 9 libraries,
    unchanged across the deploy.
  - `$validate-code` over ALL 219 memberships: 219/219, same as before the
    deploy, with non-member codes still refused on all three libraries.
  - `$translate` — the path whose resolver was rewired — answers
    "no plan.pdhc Concept binds ('icd10', 'Z94.0')". It names ICD-10, which is
    the behavioural proof the resolver no longer returns snomed for that URL.
  - `$lookup` 200; an unknown system still reads as "not registered as a
    CanonicalLib", not as an ambiguity.
  - `/api/health` 200 database connected; sibling smoke 10/10.

The 409 conflict path was NOT exercised in production, deliberately: proving
it would mean creating a junk canonical library in live terminology data. It
is mutation-tested in the suite instead.

Two findings filed from this work rather than folded in: #922 (renaming a
lookup row to a taken name is an unhandled IntegrityError — a 500, the #875
shape one field over) and #923 (#875 step 3: snomed's URL is a BROWSER link
with query parameters, not an identifier, and loinc/atc are not the registered
URIs either — measured against 39/23/6 files platform-wide that do use the
registered forms).
