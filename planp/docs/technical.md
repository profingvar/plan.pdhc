# plan.pdhc — Technical Manual

*Audience: integrators and operators. Grounded in the code under
`planp/` (Flask app factory `app/__init__.py`, `app/config.py`, the
`app/api/*` blueprints, `app/models/*`, and `migrations/`). For the
authoring/product overview see `user_manual.md`; for endpoint payload
detail see `api_reference.md`.*

---

## 1. What the service is

plan.pdhc is the **PlanDefinition authoring service** of the PDHC platform: a
Flask + SQLAlchemy + Postgres app that lets authors create clinical **Concepts**,
**PlanDefinitions** (goals + activities + transactions), **Questionnaires/Forms**,
and **ValueSets**, and publishes all of it as a conformant **FHIR R5 terminology
service**. It also hosts an opt-in, feature-flagged **guided-authoring assistant**
(epic #516).

It is a Flask app built by `create_app()` in `app/__init__.py` (blueprints
registered there), configured by `app/config.py`, migrated by Flask-Migrate
(Alembic) under `migrations/versions/`.

- **App port:** `9030` (gunicorn binds `127.0.0.1:9030`)
- **DB port:** `9031` (Postgres, loopback-only `127.0.0.1:9031:5432`)
- **Containers:** `pdhc_app` (Flask/gunicorn) and `pdhc_db` (postgres:16), per
  `docker-compose.yml`
- **Database name:** `pdhc_gateway` — a **legacy** name retained for data
  continuity (rollup #325 / #336); do not rename the volume.
- **Health:** `GET /api/health` → `{status, database, service, version}`,
  HTTP 200 when the DB is reachable and **503** when `degraded`. Rate-limit
  exempt; emits `Access-Control-Allow-Origin: https://www.pdhc.se` so
  `services.html` can read the real DB dot.

All API blueprints are mounted under `/api/v1`. Web (server-rendered) blueprints
are mounted at root.

---

## 2. Data model (~21 tables)

Confirmed from `app/models/*` and `migrations/`. GUID rule (Rule 18): every
entity has a `guid` (UUID v4); **all** cross-references are by GUID, never
integer id.

**Core terminology / concepts** (`concept_models.py`)
- `concepts` — the central resource: `response_type`, `unit`, `valueset`,
  `canonical_lib` + `canonical_refnumber` (terminology binding), `range_low/high`,
  `anchor_*`, `status` (default `draft`). One CHECK constraint `ck_concept_range`
  (`range_low ≤ range_high`).
- `values_catalog` — reusable coded values.
- `valuesets` — bound answer sets.
- `valueset_values` — valueset↔value membership (with `sort_order`; unique
  `(valueset_guid, value_guid)`).

**Lookup tables** (`concept_models.py`) — author-editable, GUID-keyed:
- `canonical_libs`, `concept_types`, `response_types`, `units`, `plandef_types`,
  `intended_uses`.

**PlanDefinition** (`fhir_models.py` + `activity_models.py`)
- `plan_definitions` — FHIR R5 PlanDefinition (has `fhir_id`, `fhir_data` JSON,
  plus `goal`/`action` JSON columns).
- `plandefinition_goals` — goal rows (concept ref + target range/operator/value).
- `activities`, `plandefinition_activities` (join), `transactions` — the data
  points an activity collects (`concept_guid` + optional `unit`, ranges).

**Forms / Questionnaires** (`forms_models.py`)
- `questionnaires`, `questionnaire_items`, `questionnaire_responses`,
  `form_definitions`, `form_definition_items`.

**Auth** (`user_models.py`)
- `users` — local bootstrap/superuser row (used by `AUTH_DISABLED` auto-login and
  first-run SU bootstrap).

That is 21 tables. `concept_guid` is the universal anchor: one concept GUID
resolves canonical lib, concept type, response type, unit, and value set — none
of which is duplicated into a plan (see `db_schema_snapshot.md`).

### The unit-lives-on-concept invariant

The canonical measurement unit is stored on `concepts.unit`. Downstream code and
plans resolve the unit **via the concept**, not via `Transaction.unit` /
`Goal.target_unit` (those free-string columns exist but are duplicates). The
validator flags divergence with `W-UNIT-CONTRADICTS`. Do not treat a
transaction-level unit as authoritative.

---

## 3. Authoring / CRUD API (`/api/v1`)

Server-rendered web routes exist for all of these; the JSON API is what
integrators use.

- **Concepts** (`app/api/concepts.py`): `GET/POST /concepts`,
  `GET/PUT/DELETE /concepts/<guid>`, `POST /concepts/import`,
  `GET/POST /concepts/<guid>/values`, `DELETE /concepts/<guid>/values/<value_guid>`.
- **Lookup values/valuesets** (`app/api/lookup_tables.py`, prefix
  `/api/v1/lookup`): full CRUD for `/values` and `/valuesets`, plus valueset
  membership `/valuesets/<guid>/values[/<value_guid>]`.
- **PlanDefinitions** (`app/api/plandefinitions.py`): `GET/POST /plandefinitions`,
  `GET/PUT/DELETE /plandefinitions/<guid>`.
- **Forms** (`app/api/forms.py`): `/forms`, `/forms/produce`,
  `/forms/<guid>/questionnaire`, `/forms/<guid>/publish` (publish → immutable),
  `/forms/<guid>/render-ready`, `/forms/<guid>/immutability`, `/forms/<guid>/versions`.
- **Form definitions** (`app/api/form_definitions.py`): CRUD under
  `/form-definitions` and `/form-definitions/<guid>/items`.

### Save enforcement — GA-5 fail-closed (`app/services/save_guard.py`)

Concept/plandef saves run the deterministic validators and **block** on
`error`-severity issues (warnings pass). Gated by `PLANDEF_VALIDATION_ENFORCED`
(default **on**; kill-switch). An admin/SU may force with
`override_validation=1` (JSON key or form field), which is written to the app log
as an audit trail. On a block, the web route flashes and the JSON API returns
**HTTP 422** with the structured issues (`SaveBlocked.as_dict()`).

---

## 4. FHIR R5 terminology profile (`/api/v1`) — LIVE

Additive to the CRUD JSON (does not replace it). Canonical URLs are
`https://plan.pdhc.se/fhir/{Resource}/{id}` (a FHIR identifier — routes stay under
`/api/v1`). `$`-operations are also registered under the `%24`-escaped path for
clients that encode `$`.

**ValueSet** (`app/api/fhir_valueset.py`)
- `GET /ValueSet`, `GET /ValueSet/<guid>`
- `GET /ValueSet/<guid>/$expand`, `POST /ValueSet/$expand`
- `GET /ValueSet/<guid>/$validate-code`, `POST /ValueSet/$validate-code`

**CodeSystem** — local id `plan-pdhc-local` (`app/api/fhir_codesystem.py`)
- `GET /CodeSystem`, `GET /CodeSystem/<id>`
- `GET/POST /CodeSystem/$lookup`
- **The local CodeSystem `code` is the `Concept.guid`** (ADR D1). Each entry
  carries the concept's `canonical-lib` / `canonical-ref` / `status` as
  properties; external systems delegate lookups to termbank.

**ConceptMap** — local id `plan-pdhc-canonical-bindings`
(`app/api/fhir_conceptmap.py`)
- `GET /ConceptMap`, `GET /ConceptMap/<id>`
- `GET/POST /ConceptMap/$translate` — translate local concept ↔ external canonical
  code (LOINC/SNOMED/…).

**Terminology surface** (`app/api/terminology.py`): a `$validate-code` entry point
plus termbank proxies (`/termbank/concept/<system>/<code>`, `/termbank/search`).

**FHIR PlanDefinition read** (`app/api/fhir_plandefinitions.py`):
`GET /PlanDefinition`, `GET /PlanDefinition/<fhir_id>`,
`GET /PlanDefinition/<fhir_id>/$expand`.

---

## 5. Authoring assistant (epic #516) — opt-in

Blueprint `app/api/authoring.py`, prefix `/api/v1`. All endpoints are
`@requires_role('read_write')` and **none of them mutate data**. Gated by
`AUTHORING_ASSISTANT_ENABLED` (default **false**); when off every endpoint
returns `{"enabled": false}` and existing save paths are untouched.

- `GET  /authoring/models` — allowlisted Claude models + whether a key is set.
- `POST /authoring/validate` — run Layer-1 validators on a `concept` or `plandef`
  draft; returns structured issues. Works with **no** API key.
- `POST /authoring/assist` — Layer-2 Claude suggestion for a plain-language
  `intent`, self-checked against Layer 1. Requires an intent; degrades to
  validation-only without a key.
- `POST /authoring/openehr-realisable` — proxy to rosetta.pdhc's realisability
  check; degrades gracefully (`available:false` + reason) when rosetta is
  unconfigured/unreachable.

**Two layers** (design doc `plandef_authoring_assistant_design.md`):
- **Layer 1 — `app/services/plandef_validation.py`**: pure, deterministic,
  shared by web + API. Invariant codes include `E-UNIT-REQUIRED`,
  `E-VALUESET-REQUIRED`, `E-RESPONSE-TYPE-UNKNOWN`, `E-DANGLING-REF`,
  `E-RANGE-INVERTED` (errors) and `W-TERM-MISSING`, `W-TERM-UNVERIFIED`,
  `W-UNIT-CONTRADICTS`, `W-EMPTY-PLANDEF` (warnings). This is the actual safety
  floor and is used by GA-5 (§3).
- **Layer 2 — `app/services/plandef_assistant.py`**: Anthropic Messages API call.
  Model is caller-selected from `AUTHORING_ASSISTANT_MODELS` (default
  `claude-sonnet-5`, allowlist also `claude-opus-4-8`, `claude-haiku-4-5-*`); a
  non-allowlisted model is rejected. Searches existing concepts/termbank first,
  runs Layer 1 on its own proposal, never auto-commits, never raises. No PHI is
  sent — only concept/terminology metadata + the author's intent.

MDR note: PlanDef thresholds flow to request.pdhc's data-driven alerts, so Layer
1 is the reviewed, deterministic guarantee; the assistant is a reviewed-draft
helper on top of it.

---

## 6. Authentication & authorization

Two paths, both in `app/api/auth.py`.

### SSO (interactive users)

- Login redirect + callback: `/api/v1/auth/{login,callback,logout,me}`. On
  callback the JWT is validated with SSO and the bearer stored in the session.
- **No blob caching (Rule 11 / #49).** Every protected request re-validates the
  stored bearer against `sso.pdhc /api/auth/me/service`
  (`app/services/sso_service.validate_token`). `session['sso_user']` is a
  **display-only** cache refreshed on each validation and is *never* trusted for
  authorization. A revoked/flushed token 401s on the very next call.
- Forced password change (`must_change_password`) → 403 with a
  `change_password_url` (API) or redirect to SSO change-password (web).
- **Role mapping** (`requires_role`), levels read_only(1) < read_write(2) <
  admin(3):
  - `read_only` — any authenticated session.
  - `read_write` — `user_type == "professional"` **and** `"planning"` in the
    session's phases, **or** an SU admin.
  - `admin` — `is_su_admin`.
- **Phases:** `_phases()` prefers the reform-canonical **`session_phases`**
  (M0 #421) and falls back to legacy **`effective_phases`** for pre-reform
  tokens. The `planning` gate value is identical in both.
- **SU bypass:** `is_su_admin` short-circuits all role checks.
- **Local dev:** `AUTH_DISABLED=true` bypasses auth entirely and auto-logs-in the
  local `admin` user. **Never ship this to prod.**

### Service key (trusted siblings)

`X-Source-Service` + `X-Service-Key` headers let a recognised sibling call
POST/PUT/DELETE without an SSO session (`_service_key_outcome()`). Recognised
sources (`KNOWN_SERVICES`):
- `loader.pdhc` → env `PLAN_LOADER_SERVICE_KEY` (bulk concept loader)
- `sim.pdhc` → env `SIM_PDHC_SERVICE_KEY` (concept-GUID resolution at run time)

An unknown source, missing key, or wrong key returns **403**. Valid-shape
service-key callers also bypass the rate limiter (`@limiter.request_filter` in
`app/__init__.py`) so canonicaliser warmup bursts don't trip the default
`200/minute`.

---

## 7. Configuration (`app/config.py` / `.env`)

Key env vars (see `.env.example`):

| Var | Purpose |
|-----|---------|
| `DATABASE_URL` | Postgres DSN (default DB `pdhc_gateway` on `:9031`) |
| `AUTH_DISABLED` | `true` = bypass auth (local dev only); prod sets `false` |
| `SSO_BASE_URL` / `SSO_CLIENT_ID` / `SSO_CLIENT_SECRET` / `SSO_CALLBACK_URL` | SSO integration |
| `PLAN_LOADER_SERVICE_KEY` / `SIM_PDHC_SERVICE_KEY` | trusted-sibling service keys |
| `AUTHORING_ASSISTANT_ENABLED` | master flag for `/api/v1/authoring/*` (default false) |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_API_BASE` | Layer-2 assistant (no key ⇒ validation-only) |
| `AUTHORING_ASSISTANT_MODELS` / `_DEFAULT_MODEL` / `_MAX_TOKENS` / `_TIMEOUT_SECONDS` | model allowlist + bounds |
| `PLANDEF_VALIDATION_ENFORCED` | GA-5 fail-closed on save (default true; kill-switch) |
| `ROSETTA_BASE_URL` / `ROSETTA_SERVICE_KEY` | openEHR-realisable proxy |
| `CDR6_BASE_URL` / `CDR6_SERVICE_KEY` / `CDR_TRANSFER_TARGETS` | #530 Transfer page (thin proxy to cdr_6) |
| `RATELIMIT_DEFAULT` (`200/minute`) / `RATELIMIT_STORAGE_URI` | Flask-Limiter |
| `BOOTSTRAP_SU_USERNAME` / `BOOTSTRAP_SU_PASSWORD` | first-run SU bootstrap |
| `APP_VERSION` | reported by `/api/health` |

---

## 8. CLI & operations

- **SU bootstrap:** on first run `create_app()` creates a superuser from
  `BOOTSTRAP_SU_USERNAME` / `BOOTSTRAP_SU_PASSWORD` if no users exist (Rule 23).
- **Bulk concept import (#134):** `flask import-concepts <path.xlsx|.csv>
  [--operator NAME] [--dry-run] [--json-out]`. Parses, validates, and imports
  concepts; reports created/updated/rejected with per-row reasons; exit code 1 if
  any row is rejected.
- **Migrations:** `flask db upgrade` (Alembic). Note: `alembic_version` is
  `varchar(32)` — keep revision ids short.
- **Docker:** `docker compose up -d --build` (Dockerfiles `COPY . .`, so a plain
  restart runs stale code — rebuild or verify). Build context is the repo root so
  root-level docs get baked into the image (Colima virtiofs can't bind-mount
  `/usr/local/www`).
- **Health check:** `curl -s https://plan.pdhc.se/api/health` — expect 200 +
  `"database":"connected"`.

---

## 9. Notes for integrators

- Address every resource by **GUID**; never match on integer id across services
  (Rule 18).
- To read the authored terminology programmatically, prefer the FHIR operations
  in §4 (`$expand`, `$validate-code`, `$lookup`, `$translate`) — they reflect
  live authoring with no cache to invalidate.
- The service-key path (§6) is the supported way for `loader.pdhc` / `sim.pdhc`
  to write/resolve without an SSO session; other callers must use SSO.
- Do not rely on `Transaction.unit` / `Goal.target_unit` as the unit of record —
  resolve the unit from the concept (§2).
