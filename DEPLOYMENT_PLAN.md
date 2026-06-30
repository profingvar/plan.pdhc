# plan.pdhc — Deployment Plan

**Status:** current as of 2026-06-30 (rollup #325 / ticket #338).
**Supersedes:** the historical "PDHC Gateway" deployment plan (pre-2026-04). That
document described a now-defunct host-process model with JWT auth and a
separate observation-gateway repo; this file is the source of truth.

---

## 1. What is plan.pdhc

A Flask + PostgreSQL service that owns the FHIR R5 terminology
canonicaliser and the PlanDefinition authoring surface for the PDHC
platform. External traffic hits `https://plan.pdhc.se` via the shared
nginx reverse proxy on the macmini; internally the service binds to
`127.0.0.1:9030`.

## 2. Container layout

Two containers, one compose project (`pdhc`):

| Container  | Role                          | Port (host loopback) |
|------------|-------------------------------|----------------------|
| `pdhc_db`  | PostgreSQL 16 (alpine)         | 9031 → 5432          |
| `pdhc_app` | Flask + gunicorn (2 workers)   | 9030 → 9030          |

Both bind to `127.0.0.1` on the host via the compose port map; the
gunicorn process inside the container binds `0.0.0.0:9030`. The host
port map (`docker-compose.yml:32`) is what enforces loopback-only
exposure, NOT the gunicorn flag — bear that in mind when reading logs
or auditing exposure.

## 3. Files / scripts

| Path                          | Owner | Purpose |
|-------------------------------|-------|---------|
| `start.sh`                    | Repo  | All-Docker entry point — `docker compose up -d --build` of db + app. |
| `planp/entrypoint.sh`         | Repo  | Runs inside `pdhc_app`: waits for db, runs `flask db upgrade`, execs gunicorn. |
| `planp/.env.example`          | Repo  | Committed template. Copy to `planp/.env` for local dev. |
| `planp/.env`                  | Op    | Live secrets. Never committed. |
| `docker-compose.yml`          | Repo  | Single compose project pinned via `COMPOSE_PROJECT_NAME=pdhc`. |
| `planp/migrations/`           | Repo  | Alembic migrations. Applied on container start by entrypoint. |
| `planp/requirements.txt`      | Repo  | Python deps. Image rebuild required after edits. |

Scripts referenced in the historical document that **do not exist**
and must not be invoked: `safe_restart.sh`, `server_deploy.sh`,
`pack_deploy.sh`, `scripts/init_db.py`, `scripts/create_su.py`. DB
init is `flask db upgrade` (alembic). Superuser creation happens
automatically via `_bootstrap_superuser()` in `app/__init__.py:283` on
first run if `BOOTSTRAP_SU_USERNAME` + `BOOTSTRAP_SU_PASSWORD` env are
set.

## 4. Database

DB name: **`pdhc_gateway`** — legacy name retained for data continuity
(rollup #325 / ticket #336). Renaming the volume risks data loss (see
CLAUDE.md memory `feedback_db_safety.md`). The `.env.example` /
`config.py` default both reflect this name; do not change.

Local credentials live in `planp/.env`; production credentials live in
the `.env` on miserver (`/usr/local/www/plan.pdhc/planp/.env`).

## 5. Auth

SSO via `sso.pdhc.se`. Plan.pdhc does **not** issue tokens of its own.
Per request:

1. Browser hits `GET /api/v1/auth/login` → 302 to sso.pdhc with the
   callback in the redirect.
2. sso.pdhc bounces back to `GET /api/v1/auth/callback?code=…`. The
   callback exchanges `code` for an access token, calls
   `sso.pdhc /api/auth/me/service` with `X-SSO-Client-Id` +
   `X-SSO-Client-Secret` to validate + fetch the user blob, and sets
   a short-lived session cookie.
3. Every subsequent request that touches a protected view re-validates
   the bearer against sso.pdhc — there is no token caching.

**Service-key bypass:** trusted sibling services may bypass SSO by
sending `X-Source-Service` + `X-Service-Key` headers; known sources are
listed in `planp/app/api/auth.py:KNOWN_SERVICES` (currently
`loader.pdhc` and `sim.pdhc`).

Local dev sets `AUTH_DISABLED=true` to short-circuit the whole thing —
NEVER deploy with that flag on. See `SSO_INTEGRATION_PLAN.md` for the
full handshake spec.

## 6. Bootstrap a fresh deploy

```
git clone <repo> /usr/local/www/plan.pdhc
cd /usr/local/www/plan.pdhc
cp planp/.env.example planp/.env
# edit planp/.env — fill POSTGRES_PASSWORD, FLASK_SECRET_KEY,
# SSO_CLIENT_SECRET, BOOTSTRAP_SU_PASSWORD, PLAN_LOADER_SERVICE_KEY,
# SIM_PDHC_SERVICE_KEY, API_KEY
./start.sh
curl http://127.0.0.1:9030/api/health
```

`flask db upgrade` runs inside the container; the superuser is created
on first start.

## 7. Reverse proxy

External `https://plan.pdhc.se` is mapped to `127.0.0.1:9030` by the
shared nginx config on miserver (owned by the operator — do not edit
without authorization; see CLAUDE.md §14).

## 8. Restart / rollback

Graceful restart of the in-scope service only:
```
cd /usr/local/www/plan.pdhc
./start.sh           # docker compose up -d --build is idempotent
```

NEVER run `colima stop`, `colima delete`, `docker compose down -v`, or
`colima restart` from this service — those affect every container in
the shared Colima VM.

## 9. Rate limiting

Default 200 requests/minute per source, applied globally via
`RATELIMIT_DEFAULT` in `planp/app/__init__.py`. Endpoints that should
stay freely pollable (`/api/health`, `/api/v1/capability-statement`,
`/api/v1/metadata`, `/api/v1/endpoints`) are decorated with
`@limiter.exempt`. Requests that carry a valid service-key bypass the
limiter via the global `request_filter`.

## 10. Verification

After any deploy:
```
curl https://plan.pdhc.se/api/health
curl https://plan.pdhc.se/api/v1/capability-statement
curl 'https://plan.pdhc.se/api/v1/CodeSystem/plan-pdhc-local' | jq .version
```

Healthy responses: 200 ok with `database: connected`; a non-empty
`.version` field on the CodeSystem (derives from
`max(Concept.vers_number)`).

## See also

- `SSO_INTEGRATION_PLAN.md` — auth handshake spec.
- `planp/docs/api_reference.md` — REST + FHIR endpoint reference.
- `plan_description.md` — domain model.
- `top_rules.md` — immutable constraints (Rule 16 start.sh contract, Rule 19 sudo-is-operator-only, etc.).
- `progress.md` + `changed_files.md` — repo bookkeeping per Rules 4 + 17.
