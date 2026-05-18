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
