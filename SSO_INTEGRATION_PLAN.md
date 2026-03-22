# SSO Integration — plan.pdhc.se ↔ sso.pdhc.se

**Date:** 2026-03-20

---

## Status: What's Already Done

The Flask code is complete on both sides. What remains is **configuration only**.

| Component | Status |
|-----------|--------|
| `sso_service.py` (SSO client in plan.pdhc) | Done |
| `auth.py` — login, callback, logout, `@sso_login_required`, `@requires_role` | Done |
| `base.html` — login/logout/user display in nav | Done |
| `@sso_login_required` on all write routes | Done |
| SSO dev credentials in sso.pdhc `.env` | Done (`plan-dev-client-id` / `plan-dev-client-secret`) |
| SSO dev callback allowlist | Done (`http://localhost:9030/api/v1/auth/callback`) |
| SSO oath_overview.csv registration | Done (plan.pdhc entry exists) |

---

## Step-by-Step: Production Integration

### Step 1 — Update sso.pdhc.se `.env` for production URLs

On the **server running sso.pdhc.se**, edit `/opt/sso_pdhc/app/.env`:

```bash
# Generate production credentials (replace the dev ones)
SSO_CLIENT_ID_PLAN=<generate: python3 -c "import secrets; print(secrets.token_urlsafe(24))">
SSO_CLIENT_SECRET_PLAN=<generate: python3 -c "import secrets; print(secrets.token_urlsafe(48))">

# Add plan.pdhc.se to the allowlists (append to existing comma-separated values)
ALLOWED_ORIGINS=...,https://plan.pdhc.se
ALLOWED_CALLBACK_URLS=...,https://plan.pdhc.se/api/v1/auth/callback
```

Then restart the SSO service:
```bash
cd /opt/sso_pdhc/app
./safe_restart.sh
```

Save the `CLIENT_ID` and `CLIENT_SECRET` values — you need them in Step 3.

---

### Step 2 — DNS

Create an A record:
```
plan.pdhc.se  →  <server IP>
```

Verify:
```bash
dig +short plan.pdhc.se
# Should return your server IP
```

---

### Step 3 — Configure plan.pdhc.se `.env`

On the **server running plan.pdhc**, edit the `.env`:

```bash
# ── Turn on SSO ──
AUTH_DISABLED=false

# ── SSO connection ──
SSO_BASE_URL=https://sso.pdhc.se
SSO_CLIENT_ID=<CLIENT_ID from Step 1>
SSO_CLIENT_SECRET=<CLIENT_SECRET from Step 1>
SSO_CALLBACK_URL=https://plan.pdhc.se/api/v1/auth/callback

# ── Production hardening ──
FLASK_ENV=production
FLASK_SECRET_KEY=<generate: python3 -c "import secrets; print(secrets.token_urlsafe(48))">
```

---

### Step 4 — Deploy plan.pdhc.se with nginx + SSL

Use your `nginx_implement_server19March.md` template with:

| Placeholder | Value |
|---|---|
| `GENERIC` | `plan_pdhc` |
| `GENERIC.DOMAIN` | `plan.pdhc.se` |
| `PORT#FE` | `9030` |
| `PORT#DB` | `9031` |

Condensed:
```bash
# 4a. Deploy the app (if not already running)
./server_deploy.sh plan_pdhc_deploy_*.tar.gz install

# 4b. nginx site config
sudo nano /etc/nginx/sites-available/plan.pdhc.se
# Paste the HTTP-only config from the template (section 4a)

sudo ln -s /etc/nginx/sites-available/plan.pdhc.se /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 4c. SSL certificate
sudo certbot certonly --webroot -w /var/www/certbot -d plan.pdhc.se

# 4d. Update nginx to HTTPS config (template section 5c)
sudo nano /etc/nginx/sites-available/plan.pdhc.se
sudo nginx -t && sudo systemctl reload nginx

# 4e. Verify
curl -s https://plan.pdhc.se/api/health
```

---

### Step 5 — Update SSO oath_overview.csv (production URLs)

Call the SSO admin API to update the service registry entry:

```bash
curl -X PUT https://sso.pdhc.se/api/admin/oath-overview \
  -H "Authorization: Bearer <SU_ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "plan.pdhc",
    "service_url": "https://plan.pdhc.se",
    "api_health_url": "https://plan.pdhc.se/api/health",
    "capability_statement_url": "https://plan.pdhc.se/api/v1/metadata",
    "endpoints_url": "https://plan.pdhc.se/api/v1/endpoints",
    "privilege_level": "authenticated",
    "notes": "FHIR R5 PlanDefinition Builder — planning phase"
  }'
```

---

### Step 6 — Test the login flow

1. Open `https://plan.pdhc.se` in browser
2. Click **Login** in the nav
3. You're redirected to `https://sso.pdhc.se/login?next=https://plan.pdhc.se/api/v1/auth/callback&state=...`
4. Enter your SSO email + password
5. SSO redirects back: `https://plan.pdhc.se/api/v1/auth/callback?token=JWT&state=...`
6. plan.pdhc validates token via `GET sso.pdhc.se/api/auth/me/service` (with Bearer + client creds)
7. Session created — your email appears in the nav bar
8. Try creating a concept — should work
9. Click **Logout** — session cleared

---

### Step 7 — Verify role mapping

| Action | Required SSO profile |
|--------|---------------------|
| View lists (concepts, valuesets, etc.) | No login needed (public) |
| Create / edit / delete anything | `user_type=professional` + `"planning"` in `effective_phases` |
| Admin operations | `is_su_admin=true` |

Test with:
- A professional user with planning phase access → should be able to create/edit
- A professional without planning phase → should get 403 on write operations
- A patient user → should get 403 on write operations
- An SU admin → should have full access

---

## Auth Flow

```
Browser                    plan.pdhc.se                   sso.pdhc.se
  │                              │                            │
  ├─ GET /api/v1/auth/login ────►│                            │
  │                              ├─ generate CSRF state       │
  │◄─ 302 ──────────────────────┤                            │
  │                              │                            │
  ├─ GET /login?next=callback&state=S ──────────────────────►│
  │                              │                        login page
  │                              │                     user enters creds
  │◄─ 302 callback?token=JWT&state=S ──────────────────────┤
  │                              │                            │
  ├─ GET /api/v1/auth/callback?token=JWT&state=S ──────────►│
  │                              ├─ verify state matches      │
  │                              │                            │
  │                              ├─ GET /api/auth/me/service ►│
  │                              │  Authorization: Bearer JWT │
  │                              │  X-SSO-Client-Id: xxx      │
  │                              │  X-SSO-Client-Secret: xxx  │
  │                              │◄─ access blob (JSON) ──────┤
  │                              │                            │
  │                              ├─ session['sso_user'] = blob│
  │◄─ 302 → dashboard ─────────┤                            │
```

---

## Checklist

- [ ] Step 1: sso.pdhc `.env` — production client credentials + allowlists updated, SSO restarted
- [ ] Step 2: DNS `plan.pdhc.se` → server IP
- [ ] Step 3: plan.pdhc `.env` — `AUTH_DISABLED=false`, SSO credentials set
- [ ] Step 4: nginx + SSL configured, `https://plan.pdhc.se/api/health` returns 200
- [ ] Step 5: oath_overview.csv updated with production URLs
- [ ] Step 6: Login → SSO → callback → session works end-to-end
- [ ] Step 7: Role-based access verified
- [ ] Firewall: ports 9030/9031 localhost-only
- [ ] `.env` file: `chmod 600`

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Redirect to SSO fails with "callback URL not allowed" | `ALLOWED_CALLBACK_URLS` in sso.pdhc `.env` missing the plan.pdhc URL | Add `https://plan.pdhc.se/api/v1/auth/callback` and restart SSO |
| Callback returns 403 "CSRF state mismatch" | Session lost between redirect and callback (cookie issue) | Ensure `FLASK_SECRET_KEY` is set, HTTPS is active, check cookie settings |
| Callback returns 401 "Token validation failed" | Invalid `CLIENT_ID` / `CLIENT_SECRET` or SSO unreachable | Verify credentials match between sso.pdhc `.env` and plan.pdhc `.env` |
| User logged in but gets 403 on create/edit | User doesn't have `planning` in `effective_phases` | Add user to a planning-phase group in SSO |
| Login button not showing | Template checks `config.get('AUTH_DISABLED')` | Verify `AUTH_DISABLED=false` in plan.pdhc `.env` |
