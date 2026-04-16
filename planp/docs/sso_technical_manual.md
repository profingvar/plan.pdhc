# SSO Technical Manual — plan.pdhc.se

**Version:** 1.0
**Date:** 2026-03-20

---

## 1. Overview

plan.pdhc.se delegates all user authentication to sso.pdhc.se via a four-step browser-based handshake. plan.pdhc never stores passwords or manages user accounts — it receives a signed JWT from SSO, validates it, and caches the resulting access blob in a server-side session.

---

## 2. Architecture

```
                          ┌──────────────┐
                          │  sso.pdhc.se │
                          │              │
                          │  - User DB   │
                          │  - JWT issue │
                          │  - Token     │
                          │    validate  │
                          └──────┬───────┘
                                 │
              H1 redirect  ──────┤────── H4 validate
              H3 callback  ◄─────┘
                                 │
┌─────────┐              ┌──────┴───────┐
│ Browser │◄────────────►│plan.pdhc.se  │
│         │   HTML/CSS   │              │
│         │   Session    │ - Flask app  │
│         │   cookie     │ - SSO client │
│         │              │ - Session    │
└─────────┘              └──────────────┘
```

### Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `sso_service.py` | `app/services/` | SSO HTTP client — builds login URL, validates tokens, fetches orgs |
| `auth.py` | `app/api/` | Auth blueprint — `/login`, `/callback`, `/logout`, `/me` endpoints |
| `@sso_login_required` | `app/api/auth.py` | Decorator — redirects unauthenticated users to SSO |
| `@requires_role` | `app/api/auth.py` | Decorator — enforces role-based access from SSO access blob |
| `base.html` | `app/templates/` | Nav bar — shows Login/Logout/user email based on session |

---

## 3. Handshake Flow (H1–H4)

### H1 — Redirect to SSO

**Trigger:** User clicks Login, or `@sso_login_required` detects no session.

```
Browser  ──GET /api/v1/auth/login──►  plan.pdhc.se
plan.pdhc.se:
  1. Generate random CSRF state token (secrets.token_urlsafe(32))
  2. Store state in Flask session: session['sso_state'] = state
  3. Build SSO URL:
     https://sso.pdhc.se/login?next={SSO_CALLBACK_URL}&state={state}
  4. Return 302 redirect to SSO URL
Browser  ◄──302 Location: https://sso.pdhc.se/login?next=...&state=...──
```

### H2 — User Authenticates at SSO

```
Browser  ──GET https://sso.pdhc.se/login?next=...&state=...──►  sso.pdhc.se
sso.pdhc.se:
  1. Display login form
  2. User enters email + password
  3. Validate credentials (bcrypt)
  4. Issue JWT (HS256, 24h expiry, subject=user_guid)
  5. Validate callback URL against ALLOWED_CALLBACK_URLS
  6. Redirect back with token + state
Browser  ◄──302 Location: https://plan.pdhc.se/api/v1/auth/callback?token={JWT}&state={state}──
```

### H3 — Callback Receives Token

```
Browser  ──GET /api/v1/auth/callback?token={JWT}&state={state}──►  plan.pdhc.se
plan.pdhc.se:
  1. Check for error params (error, error_description)
  2. CSRF validation: compare request state vs session['sso_state']
  3. Extract token from query params
  4. Proceed to H4 (token validation)
```

### H4 — Token Validation

```
plan.pdhc.se  ──GET /api/auth/me/service──►  sso.pdhc.se
Headers:
  Authorization: Bearer {JWT}
  X-SSO-Client-Id: {SSO_CLIENT_ID}
  X-SSO-Client-Secret: {SSO_CLIENT_SECRET}

sso.pdhc.se:
  1. Verify JWT signature + expiry
  2. Check token not revoked
  3. Verify client credentials (CLIENT_ID + SECRET)
  4. Build access blob from user + professional/patient + group data
  5. Return JSON access blob

plan.pdhc.se  ◄──200 {access blob JSON}──

plan.pdhc.se (on success):
  1. Store blob: session['sso_user'] = blob
  2. Store token: session['sso_token'] = token
  3. Set session.permanent = True (24h lifetime)
  4. Redirect to dashboard
```

---

## 4. Access Blob Structure

The access blob returned by `/api/auth/me/service` contains user identity and authorization data.

### Professional User

```json
{
  "user_guid": "550e8400-e29b-41d4-a716-446655440000",
  "email": "anna.lindqvist@hospital.se",
  "user_type": "professional",
  "is_su_admin": false,
  "professional_guid": "660e8400-e29b-41d4-a716-446655440001",
  "professional_role": "doctor",
  "fhir_resource_type": "Practitioner",
  "organization_ids": ["org-uuid-1"],
  "groups": [
    {
      "group_guid": "770e8400-e29b-41d4-a716-446655440002",
      "group_name": "Oncology Planning",
      "category": "planning",
      "status": "approved",
      "is_admin": false
    }
  ],
  "effective_phases": ["planning"]
}
```

### Patient User

```json
{
  "user_guid": "550e8400-e29b-41d4-a716-446655440010",
  "email": "patient@example.com",
  "user_type": "patient",
  "is_su_admin": false,
  "patient_guid": "880e8400-e29b-41d4-a716-446655440011",
  "organisation_guid": "org-uuid-1",
  "in_registry": true,
  "registries": ["INCA"],
  "fhir_resource_type": "Patient"
}
```

---

## 5. Role Mapping

plan.pdhc maps SSO access blob fields to three internal permission levels:

| plan.pdhc Role | Level | SSO Condition | Allowed Actions |
|----------------|-------|---------------|-----------------|
| `read_only` | 1 | Any authenticated session | View all pages |
| `read_write` | 2 | `user_type=professional` AND `"planning"` in `effective_phases` | Create, edit, delete content |
| `admin` | 3 | `is_su_admin=true` | Full access, admin operations |

### Route Protection

| Route Pattern | Protection | Who Can Access |
|---------------|-----------|----------------|
| `/` (dashboard), list pages | Public | Everyone (no login required) |
| `/concepts/create`, `/*/edit`, `/*/delete` | `@sso_login_required` | Authenticated users with `read_write` |
| API mutations | `@requires_role('read_write')` | Professionals in planning phase |

---

## 6. Configuration

### Environment Variables (plan.pdhc)

| Variable | Purpose | Example |
|----------|---------|---------|
| `AUTH_DISABLED` | `true` bypasses all SSO (local dev), `false` enables SSO | `false` |
| `SSO_BASE_URL` | SSO server base URL | `https://sso.pdhc.se` |
| `SSO_CLIENT_ID` | Service credential — identifies plan.pdhc to SSO | `VjUvjd2R...` |
| `SSO_CLIENT_SECRET` | Service credential — authenticates plan.pdhc to SSO | `HAZuzZSG...` |
| `SSO_CALLBACK_URL` | Exact URL SSO redirects to after login | `https://plan.pdhc.se/api/v1/auth/callback` |
| `FLASK_SECRET_KEY` | Signs the Flask session cookie | (random 48+ chars) |

### Environment Variables (sso.pdhc)

| Variable | Purpose |
|----------|---------|
| `ALLOWED_ORIGINS` | Comma-separated origins for CORS (must include `https://plan.pdhc.se`) |
| `ALLOWED_CALLBACK_URLS` | Comma-separated callback URLs (must include exact callback URL) |
| `SSO_CLIENT_ID_PLAN` | Client ID issued to plan.pdhc |
| `SSO_CLIENT_SECRET_PLAN` | Client secret issued to plan.pdhc |

---

## 7. Session Lifecycle

| Event | Session State |
|-------|---------------|
| User visits site (no login) | No session — public pages work, write routes redirect to SSO |
| User clicks Login | `sso_state` stored in session, redirect to SSO |
| Callback succeeds | `sso_user` (access blob) + `sso_token` stored, `session.permanent = True` |
| Session expires (24h) | Session cleared — next write-route access triggers SSO redirect |
| User clicks Logout | `sso_user`, `sso_token`, `sso_state` removed from session |

---

## 8. Error Handling

| Scenario | What Happens |
|----------|-------------|
| SSO returns error on callback | 401 with error description |
| CSRF state mismatch | 403 — session may have expired between redirect and callback |
| Token validation fails (invalid/expired JWT) | 401 — user must re-authenticate |
| Invalid client credentials (CLIENT_ID/SECRET) | 403 from SSO — check `.env` on both sides |
| SSO unreachable | Retried 3 times with backoff, then 401 |
| User lacks `planning` phase | 403 on write operations — read-only access still works |

---

## 9. Security Measures

- **CSRF protection:** Random state parameter validated on callback
- **Token validation:** JWT verified server-side via SSO API (not decoded locally)
- **Client authentication:** Service credentials (CLIENT_ID + SECRET) required for token validation
- **Session security:** Server-side Flask session, signed cookie, 24h expiry
- **HTTPS only:** All SSO communication over TLS
- **No local passwords:** plan.pdhc never stores or handles user credentials
- **Retry with backoff:** SSO client retries failed requests (max 3, 0.5s × attempt)

---

## 10. Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/login` | GET | Redirect to SSO login page |
| `/api/v1/auth/callback` | GET | Receive JWT from SSO, validate, create session |
| `/api/v1/auth/logout` | GET, POST | Clear session, redirect to dashboard |
| `/api/v1/auth/me` | GET | Return current user's access blob (or 401) |

---

## 11. Troubleshooting

### Login button does nothing / redirects back to plan.pdhc

- Check `SSO_BASE_URL` in plan.pdhc `.env` — must be `https://sso.pdhc.se`
- Check SSO is running: `curl https://sso.pdhc.se/api/health`

### Callback returns "CSRF state mismatch"

- Flask session lost between redirect and callback
- Check `FLASK_SECRET_KEY` is set (not empty)
- Check cookies are enabled in the browser
- Check the session cookie domain matches

### Callback returns "Token validation failed"

- CLIENT_ID/SECRET mismatch between plan.pdhc and sso.pdhc
- SSO may have been restarted without the credentials in `.env`
- Check: `SSO_CLIENT_ID` in plan.pdhc must equal `SSO_CLIENT_ID_PLAN` in sso.pdhc

### User logged in but gets 403 on create/edit

- User is not a professional, or lacks `planning` in `effective_phases`
- Check user's group memberships in SSO admin
- SU admins bypass all role checks

### Login link not visible in nav bar

- Check `AUTH_DISABLED` is `false` in plan.pdhc `.env`
- Container may need rebuild if code was updated: `docker-compose up -d --build`
