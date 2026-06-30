# SSO Integration — plan.pdhc ↔ sso.pdhc

**Status:** current as of 2026-06-30 (rollup #325 / ticket #338 rewrite).
**Code:** `planp/app/api/auth.py` + `planp/app/services/sso_service.py`.

This document describes the actual handshake plan.pdhc implements. The
prior version of this file described a JWT-issuing model the service
never shipped — that text is superseded entirely.

---

## 1. Boundary

Plan.pdhc does NOT issue its own tokens. It is a relying party for
sso.pdhc. Every protected request re-validates the bearer against
sso.pdhc per-request; there is no token caching, no refresh route.

## 2. The handshake

### H1 — Login redirect
Browser hits `GET /api/v1/auth/login`. Plan.pdhc generates a CSRF
nonce, stores it in the session, and 302-redirects to
`{SSO_BASE_URL}/api/login` with `redirect_uri=
{SSO_CALLBACK_URL}` and the nonce as `state`.

### H2 — Callback
sso.pdhc authenticates the user and 302s back to
`GET /api/v1/auth/callback?code=<code>&state=<nonce>`. Plan.pdhc:

1. Checks `state` matches the stored nonce.
2. POSTs `code` to `{SSO_BASE_URL}/api/auth/exchange` with the
   client credentials (`X-SSO-Client-Id` + `X-SSO-Client-Secret`),
   receives an access token + user blob.
3. Sets a short-lived session cookie holding the bearer token.

### H3 — Per-request validation
Every protected view passes through `@sso_login_required` which:

1. Reads the bearer from the session cookie (or `Authorization`
   header for service-to-service).
2. Calls `sso.pdhc /api/auth/me/service` with
   `X-SSO-Client-Id` + `X-SSO-Client-Secret` headers.
3. Caches NOTHING. Every request → one sso.pdhc round trip. An
   sso.pdhc-side logout takes effect on the next plan.pdhc request.

If sso.pdhc returns the user blob, the request proceeds with that
identity. Otherwise the request 401s.

### H4 — Logout
`GET|POST /api/v1/auth/logout` clears the session cookie and
302-redirects to `{SSO_BASE_URL}/api/logout`.

## 3. Service-key bypass

Trusted sibling services may bypass SSO by sending two headers:

- `X-Source-Service: <name>` — one of the names in
  `KNOWN_SERVICES` (`planp/app/api/auth.py:14`). Currently
  `loader.pdhc` and `sim.pdhc`.
- `X-Service-Key: <key>` — must match the env var named in
  `KNOWN_SERVICES[name]` (`PLAN_LOADER_SERVICE_KEY` or
  `SIM_PDHC_SERVICE_KEY`).

Rationale: the canonicaliser warmup burst hits hundreds of
`/lookup/...` reads on cold-start; routing them through the SSO
callback would blow the SSO IO budget. The keys are deployed
out-of-band by the operator and rotated manually.

## 4. Configuration

`planp/.env` keys consumed by SSO (see `planp/.env.example`):

```
SSO_BASE_URL=https://sso.pdhc.se
SSO_CLIENT_ID=plan_pdhc_local
SSO_CLIENT_SECRET=replace_me
SSO_CALLBACK_URL=https://plan.pdhc.se/api/v1/auth/callback
PLAN_LOADER_SERVICE_KEY=<rotated by operator>
SIM_PDHC_SERVICE_KEY=<rotated by operator>
```

For local dev, set `AUTH_DISABLED=true` to bypass the entire
handshake; `_auto_login()` in `app/__init__.py:77` will log every
request in as the bootstrap admin. NEVER ship with `AUTH_DISABLED`
on.

## 5. Endpoints

| Method | Path                          | Auth   |
|--------|-------------------------------|--------|
| GET    | `/api/v1/auth/login`          | none   |
| GET    | `/api/v1/auth/callback`       | none (validates state nonce) |
| GET    | `/api/v1/auth/me`             | SSO    |
| GET    | `/api/v1/auth/logout`         | SSO    |
| POST   | `/api/v1/auth/logout`         | SSO    |

There is no `POST /api/v1/auth/login` and no `/api/v1/auth/refresh`.
Both were listed by the historical capability statement but never
shipped; the capability was rewritten in rollup #325 / ticket #326.

## 6. Failure modes

- **sso.pdhc unreachable** → every protected request 503s. Plan.pdhc
  has no fallback because per-request re-validation is the security
  model.
- **client credentials wrong** → `/api/auth/me/service` returns 401;
  plan.pdhc treats that as "not authenticated". The memory note
  `project_pdhc_sso_client_creds` covers the on-server creds audit
  procedure.
- **state nonce mismatch** → callback 400s; replay-attempt or stale
  bookmark.

## 7. References

- `planp/app/api/auth.py` — handshake implementation.
- `planp/app/services/sso_service.py` — sso.pdhc HTTP client.
- `gateway.pdhc` source — mirror implementation; phrasing reused here.
- CLAUDE.md §11 — platform-wide auth contract.
- Memory `project_pdhc_sso_client_creds` — creds audit playbook.
