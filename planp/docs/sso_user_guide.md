# Logging In to PDHC PlanDef Builder — User Guide

**Version:** 1.0
**Date:** 2026-03-20

---

## What is SSO?

PDHC PlanDef Builder uses **Single Sign-On (SSO)** for authentication. This means you log in once through the central PDHC identity service (sso.pdhc.se), and that login is shared across all PDHC applications. You do not need a separate account for PlanDef Builder.

---

## Do I Need to Log In?

**Not always.** You can browse and view content without logging in:

- Dashboard
- Concept lists and details
- Value lists and details
- ValueSet lists and details
- PlanDefinition lists, details, and FHIR previews
- Reference tables (Libraries, Units, Response Types, Concept Types)
- Documentation

**You need to log in to make changes** — creating, editing, or deleting any content requires authentication.

---

## How to Log In

1. Go to [plan.pdhc.se](https://plan.pdhc.se)
2. Click the **Login** button in the top-right corner of the navigation bar
3. You are taken to the PDHC login page (sso.pdhc.se)
4. Enter your **email** and **password**
5. After successful login, you are returned to PlanDef Builder
6. Your email address appears in the top-right corner, confirming you are logged in

If you are already logged in to another PDHC application (e.g. forms.pdhc.se), you may be logged in automatically without entering your password again.

---

## How to Log Out

1. Click your **email address** or the **Logout** button in the top-right corner
2. Your session is cleared
3. You can still browse and view content, but you will need to log in again to make changes

---

## What Can I Do Once Logged In?

Your permissions depend on your role in the PDHC system:

| Your Role | What You Can Do |
|-----------|-----------------|
| Any authenticated user | View all content (same as without login) |
| Professional in the **planning phase** | Create, edit, and delete concepts, values, valuesets, and PlanDefinitions |
| System administrator | Full access to all functions |

If you are logged in but cannot create or edit content, your account may not have planning phase access. Contact your PDHC administrator to request access.

---

## Common Questions

### I don't have a PDHC account

Accounts are managed through sso.pdhc.se. If you need access, ask your organisation's PDHC administrator to invite you, or submit an access request at sso.pdhc.se.

### I forgot my password

Go to [sso.pdhc.se](https://sso.pdhc.se) and use the password reset function. Your PlanDef Builder access uses the same credentials.

### I was logged in but now I'm asked to log in again

Login sessions last 24 hours. After that, you will need to log in again. This is a security measure.

### I get an error when trying to log in

- Make sure you are using the correct email and password
- Check that your browser accepts cookies (required for login sessions)
- If the problem persists, contact your PDHC administrator

### I can log in but I get "Insufficient permissions" when editing

Your account does not have write access to PlanDef Builder. This requires:
- A **professional** account type (not a patient account)
- Membership in a group with **planning** phase access

Contact your PDHC administrator to update your permissions.

---

## Security

- Your password is never shared with PlanDef Builder — authentication happens entirely at sso.pdhc.se
- Your session is stored securely on the server, not in your browser
- All communication is encrypted (HTTPS)
- Sessions expire automatically after 24 hours
