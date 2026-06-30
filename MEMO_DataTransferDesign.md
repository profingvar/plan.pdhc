# MEMO: Data Transfer Design in the PDHC Ecosystem — Version 2

**Subject:** How data moves between request.pdhc, 1177.pdhc, provider.pdhc, gateway.pdhc, and the return receipt chain
**Date:** 2026-04-01
**Version:** 2
**Author:** Martin Ingvar

**Change log — Version 2 (2026-04-01):**
- Added Section 5.3: provider.pdhc implementation details (push reception, meta.tag extraction, grant storage)
- Added Section 5.4: Gateway receipt delivery back to provider.pdhc
- Updated Section 10: provider.pdhc configuration dependencies
- Updated data flow diagram (Section 7) to include receipt return path

---

## Kort introduktion — vad handlar det här om?

Tänk dig att en läkare vill att en patient ska fylla i ett formulär om sin hälsa, eller att en vårdgivare ska utföra ett uppdrag och rapportera tillbaka vad de hittat. Det låter enkelt, men i verkligheten sitter läkaren, patienten och vårdgivaren i helt olika datasystem som inte automatiskt kan prata med varandra. Det här dokumentet beskriver hur vi löser det problemet.

**PDHC-ekosystemet** är ett nätverk av tjänster (små webbapplikationer) som samarbetar:

- **request.pdhc** — här skapar klinikern en beställning ("ServiceRequest"). Tänk på det som att skicka ett paket: man packar ihop patientinfo, en vårdplan och eventuella formulär, och adresserar det till rätt mottagare.
- **1177.pdhc** — den tjänst som visar formulär för patienter (som 1177:s e-tjänster). Den tar emot beställningen, plockar ut formulären och presenterar dem för patienten.
- **provider.pdhc** — en extern vårdgivares system. Det tar emot uppdrag, visar dem för vårdgivarpersonal, och skickar tillbaka resultat.
- **gateway.pdhc** — en "inkorgsserver" som tar emot all data som kommer tillbaka (observationer, formulärsvar). Den kontrollerar att avsändaren verkligen har rätt att skicka data, och lagrar resultaten.

**Huvudproblemet som löses här** är att data måste flöda säkert i två riktningar:

1. **Ut** (från klinikern till vårdgivare/patient): Beställningen med patientdata ska nå rätt mottagare, och ingen annan.
2. **Tillbaka** (från vårdgivare/patient till systemet): Resultaten ska komma tillbaka och systemet måste kunna verifiera att de verkligen kommer från rätt avsändare och gäller rätt patient.

**Hur säkerheten fungerar, förenklat:** Varje gång en beställning skickas ut medföljer en "nyckel" (grant token) — en kryptografisk kod som bevisar att mottagaren har fått tillstånd att skicka tillbaka data. Nyckeln är bunden till en specifik patient, en specifik beställning och en specifik vårdgivare. Utan den rätta nyckeln nekar systemet att ta emot data. Det är ungefär som att en bank kräver att du visar upp både legitimation och en unik referenskod för att kunna sätta in pengar på ett visst konto.

**Varför det är krångligare än det ser ut:** Patientdata skyddas av GDPR. Varje gång data överförs måste det loggas vem som skickade vad, om vilken patient, och när. Om en patient begär att få veta vilka som sett deras data måste systemet kunna svara. Dessutom kan nätverket gå ner, nycklar kan löpa ut och system kan krascha mitt i en överföring — allt detta måste hanteras utan att data förloras eller patienten märker något.

Resten av dokumentet beskriver exakt hur varje steg fungerar, vilka säkerhetskontroller som sker, och vad som händer när saker går fel.

---

## 1. Scope of This Memo

This memo documents the data transfer design for two critical flows in the PDHC ecosystem:

1. **Outbound delivery** — how request.pdhc pushes ServiceRequest bundles to 1177.pdhc and to external provider systems
2. **Inbound return** — how 1177.pdhc and provider systems send observations and QuestionnaireResponses back to the gateway

These are the two directions of a single care process cycle: a clinician requests a service, the request reaches its destination, work is done, and results come back. The transfer design must preserve clinical semantics, enforce authorization, protect patient privacy, and tolerate network failures — all across organisational boundaries.

---

## 2. Outbound: request.pdhc to Providers and 1177

### 2.1 What Gets Sent

When a clinician finalizes and pushes a ServiceRequest, the system assembles a **FHIR Bundle** (type: `message`) containing:

- **Entry 0: The ServiceRequest resource** — the top-level order, with all context embedded as contained resources:
  - `Patient` (excerpt — minimized for GDPR, no address/telecom)
  - `CarePlan` (synthesized from PlanDefinition, with goals and activities)
  - `Goal` resources (one per clinical target)
  - `Questionnaire` resources (one per form to be completed — injected from form snapshots)

- **Additional entries** (for contract-matched providers only):
  - `Binary` entries with base64-encoded render-ready form snapshots (tagged with `form_guid` and `render_ready`)

- **Bundle.meta.tag** — delivery metadata under system `https://pdhc.se/delivery`:
  - `grant_token` — the HMAC-SHA256 authorization token
  - `expires_at` — grant expiry (ISO 8601)
  - `organisation_guid` — the receiving provider's org identity
  - `contract_guid` — the governing contract (empty string `""` for direct 1177 delivery)
  - `service_request_guid` — traceability
  - `patient_guid` — the data subject
  - `receipt_token` — (provider push only) delivery receipt bearer token

### 2.2 Two Delivery Paths

The push service handles two distinct delivery scenarios:

#### Path A: Contract-Matched Provider Push

```
request.pdhc
  |
  |  1. Look up ServiceRequestContractMatch records (status: pending)
  |  2. For each match, look up provider's PAT with delivery_mode=push
  |  3. Resolve push_endpoint_url and push_auth_key from the PAT record
  |  4. Issue a DataExchangeGrant (HMAC over composite key)
  |  5. Create a ServiceRequestReceipt (bearer token for callback)
  |  6. Build FHIR Bundle with SR + Binary render-ready entries + meta tags
  |  7. POST to provider's push_endpoint_url
  |     Headers: Content-Type: application/fhir+json
  |              Authorization: Bearer <SSO JWT>
  |              X-API-Key: <push_auth_key from PAT>
  |  8. On 2xx: receipt.delivery_status = 'delivered', match.status = 'sent'
  |     On failure: receipt.delivery_status = 'failed', error body logged
  |
  v
provider system (e.g. provider.pdhc)
```

**Key design decisions:**
- The provider's endpoint URL and auth key are stored on the PAT record, not configured per-request
- A delivery receipt is created *before* the HTTP call, ensuring we have a record even if the process crashes mid-push
- The receipt_token serves as a bearer credential for the provider's callback (no auth required to respond via receipt)

#### Path B: Direct 1177 Push (Forms Delivery)

```
request.pdhc
  |
  |  1. Check if SR has forms with Questionnaire snapshots (form_snapshot not null)
  |  2. Deep-copy the SR's FHIR resource
  |  3. Inject Questionnaires as contained resources in the SR
  |     (deduplicate by ID, handling both "form_guid" and "questionnaire-form_guid" patterns)
  |  4. Issue a DataExchangeGrant with contract_guid = sr.contract_guid or ''
  |  5. Build FHIR Bundle with SR as sole entry + meta tags
  |  6. POST to FORMS_1177_WEBHOOK_URL (configured in environment)
  |     Headers: Content-Type: application/fhir+json
  |              X-API-Key: <FORMS_1177_API_KEY>
  |
  v
1177.pdhc /api/webhook/inbound
```

**Key design decisions:**
- Questionnaires are injected as **contained resources inside the SR**, not as separate Bundle entries. This matches 1177's webhook parser, which extracts Questionnaires from `contained[]`.
- The deep-copy prevents mutation of the persisted SR's FHIR resource
- `contract_guid` defaults to empty string `""` (not null) when no contract exists. This is load-bearing: the HMAC grant token includes contract_guid in its composition, so the return path must use the same empty string.
- No receipt token is generated for 1177 push — the grant token alone authorizes the return
- This push runs automatically alongside (not instead of) the contract-matched pushes in `push_all_matches`

### 2.3 Poll Delivery (Provider-Initiated)

For providers with `delivery_mode=poll`, no push occurs. Instead:

```
provider system
  |
  |  GET /api/v1/provider/feed
  |  Header: X-Provider-Token: <raw PAT>
  |
  v
request.pdhc
  |  1. Validate PAT via bcrypt hash comparison
  |  2. Derive provider_org_guid from the validated PAT (NEVER from query params)
  |  3. Return ServiceRequests addressed to this org (metadata only, no patient data)
  |
  v
provider system
  |
  |  GET /api/v1/provider/download/<sr_guid>
  |  Header: X-Provider-Token: <raw PAT>
  |
  v
request.pdhc
  |  1. Validate PAT
  |  2. Issue DataExchangeGrant if none exists for this provider+SR
  |  3. Return full FHIR Bundle + grant_token
```

**Key design decision:** The feed endpoint returns only metadata (no patient data) — the provider must explicitly download each SR to get the FHIR Bundle. This implements GDPR data minimization: bulk listing does not expose patient information.

### 2.4 The Grant Token: What It Is and Why It Matters

Every outbound delivery (push or pull) includes a **DataExchangeGrant**. This is the mechanism that authorizes the return path.

**How the grant token is computed:**

```python
msg = f"{sr_guid}:{patient_guid}:{org_guid}:{contract_guid}:{expires_iso}"
grant_token = HMAC-SHA256(key=HMAC_SECRET, msg=msg)
```

**What gets persisted (in `data_exchange_grants` table):**

| Column | Purpose |
|--------|---------|
| `service_request_guid` | Which SR this grant authorizes |
| `patient_guid` | The data subject (indexed for GDPR queries) |
| `provider_org_guid` | Which org may use this grant |
| `contract_guid` | Which contract governs (empty string for direct) |
| `grant_token` | The HMAC hex digest (128 chars) |
| `grant_type` | `bidirectional` / `download` / `upload` |
| `expires_at` | When the grant expires |
| `used_count` / `max_uses` | Usage tracking (null max = unlimited) |
| `revoked` | Boolean revocation flag |

**Design rationale — why HMAC, not JWT:**
- The grant token is opaque to the bearer. Unlike JWT, the provider cannot decode it to learn the expiry or other fields. This prevents information leakage.
- Validation is server-side only: recompute HMAC + constant-time compare. No key distribution problem.
- The composite key (5 fields) binds the grant to a specific purpose. A stolen token is useless for any other SR, patient, or org.
- Simpler than OAuth2 token exchange, which would require both parties to participate in the same authorization server.

---

## 3. Inbound at 1177: Webhook Processing

When 1177.pdhc receives a push at `/api/webhook/inbound`, the processing is:

```
POST /api/webhook/inbound
  |
  |  1. Validate X-API-Key against configured API_KEY
  |  2. Unwrap Bundle:
  |     - Extract meta.tag entries (system: https://pdhc.se/delivery)
  |       → grant_token, contract_guid, organisation_guid, expires_at
  |     - Find the ServiceRequest entry in Bundle.entry[]
  |  3. Extract Patient from SR.contained[] → patient_guid
  |  4. Extract all Questionnaire resources from SR.contained[]
  |  5. For each Questionnaire:
  |     a. Get resource ID (e.g. "questionnaire-a1b2c3d4-...")
  |     b. Strip "questionnaire-" prefix → clean UUID (fits VARCHAR(36))
  |     c. Parse version string → integer
  |     d. Create Assignment:
  |        - patient_guid
  |        - form_guid (stripped UUID)
  |        - form_version
  |        - questionnaire_fhir (full JSON, stored verbatim)
  |        - request_guid (SR ID, for traceability)
  |        - grant_token, contract_guid, organisation_guid (for return path)
  |        - grant_expires_at (parsed from ISO string)
  |        - status = 'pending'
  |  6. Commit all assignments
  |  7. Return 201 with assignment summary
```

**Critical detail — the questionnaire- prefix stripping.** plan.pdhc's FHIR builder assigns Questionnaire IDs as `questionnaire-{uuid}`, producing strings up to 51 characters. The `form_guid` column is VARCHAR(36), sized for raw UUIDs. The webhook strips the prefix to fit. This is a runtime contract between plan.pdhc's naming convention and 1177's storage schema.

**What is stored for the return path.** The Assignment record stores `grant_token`, `contract_guid`, `organisation_guid`, and `grant_expires_at`. These are the exact fields needed to dispatch the response back to the gateway. If any required field is missing (grant_token, organisation_guid, or request_guid), the return dispatch is silently skipped.

---

## 4. Return Path: 1177 to Gateway

When a patient completes a form in 1177.pdhc, the system dispatches the result to the gateway:

### 4.1 What Gets Sent

```
POST {GATEWAY_URL}/api/v1/provider/report/{request_guid}

Headers:
  Content-Type: application/fhir+json
  X-Provider-Token: {GATEWAY_PROVIDER_TOKEN}

Body:
{
  "patient_guid":      "<from assignment>",
  "contract_guid":     "<from assignment, or empty string ''>",
  "organisation_guid": "<from assignment>",
  "grant_token":       "<HMAC token from original push>",
  "expires_at":        "<ISO 8601, from assignment>",
  "report_payload":    { <FHIR QuestionnaireResponse> }
}
```

### 4.2 Design Decisions

**Fire-and-forget dispatch.** The dispatch is a non-blocking call after form submission. The patient's submission is confirmed and the local database updated regardless of whether the gateway accepts the response. If the gateway is down or rejects the submission, the error is logged but the patient sees success. The response data remains in 1177's database and can be re-dispatched or retrieved via the REST API.

**Why fire-and-forget?** The patient has fulfilled their obligation by completing the form. Their experience should not be degraded by backend infrastructure issues. The alternative (synchronous dispatch with rollback on failure) would create confusing UX: "Your form was submitted but not really."

**contract_guid as empty string, never null.** When the original push had no contract (direct 1177 delivery), `contract_guid` is stored as `""` on the Assignment. The return dispatch sends `""`, not `null` or an omitted field. This is critical because the HMAC grant token was computed with `""` in the composite key. If the return sends a different value (even null), the HMAC recomputation will produce a different hash and the gateway will reject the submission.

**X-Provider-Token for 1177.** 1177.pdhc authenticates to the gateway as a "provider" using a PAT configured in `GATEWAY_PROVIDER_TOKEN`. This reuses the existing provider authentication infrastructure — the gateway doesn't need a separate auth path for 1177. The PAT determines the org identity and must have `write` scope.

### 4.3 Guard Conditions

The dispatch is skipped entirely if any of these are missing:
- `assignment.grant_token` — no way to authorize at the gateway
- `assignment.organisation_guid` — required field in the report body
- `assignment.request_guid` — determines the URL path

Note: `contract_guid` is NOT a guard condition. It may be empty string for direct delivery, but the dispatch proceeds.

---

## 5. Return Path: Provider to Gateway

External providers (not 1177) have two return mechanisms:

### 5.1 Report Endpoint (Primary)

```
POST /api/v1/provider/report/{sr_guid}

Headers:
  X-Provider-Token: <raw PAT>

Body:
{
  "patient_guid":      "<required>",
  "organisation_guid": "<required — cross-checked against PAT>",
  "grant_token":       "<required>",
  "contract_guid":     "<optional — from original grant>",
  "status":            "completed | accepted | rejected",
  "report_payload":    { <FHIR data> }
}
```

### 5.2 Receipt Acknowledgment (For Push Delivery)

Providers who received a push can also acknowledge via the receipt token:

```
POST /api/v1/provider/receipt/{receipt_token}/ack

Headers:
  X-Provider-Token: <raw PAT>

Body:
{
  "status": "accepted | rejected | acknowledged"
}
```

The receipt_token was included in the push bundle's meta tags. This endpoint provides a simpler callback mechanism — the receipt token itself identifies the SR and match.

### 5.3 Provider.pdhc: How It Receives and Stores Requests

Provider.pdhc is the reference implementation of an external provider system. It supports both push and poll delivery modes and stores the full grant metadata needed for the return path.

#### Push Reception

```
request.pdhc
  |
  |  POST /api/v1/inbound/push
  |  Header: X-Push-Secret: <shared secret>
  |  Body: FHIR Bundle
  |
  v
provider.pdhc
  |  1. Validate X-Push-Secret against PUSH_SECRET config
  |  2. Validate Bundle resourceType
  |  3. Extract ALL meta.tag entries (system: https://pdhc.se/delivery):
  |     → receipt_token (required — 400 if missing)
  |     → grant_token
  |     → contract_guid
  |     → organisation_guid
  |     → expires_at → parsed to grant_expires_at (DateTime)
  |  4. Extract ServiceRequest from Bundle.entry[]
  |  5. Extract patient_guid from SR.subject.reference
  |  6. Extract CarePlan from SR.contained[]
  |  7. Store InboundRequest with full grant metadata:
  |     - grant_token, contract_guid, organisation_guid, grant_expires_at
  |  8. Create ProviderTask (status: dispatched)
  |  9. Cache CarePlan for guided response
  |  10. Audit log: push_received
  |  11. Acknowledge receipt upstream (fire-and-forget)
  |
  v
  Return: 202 Accepted { receipt_token, request_guid }
```

**Key design decisions:**
- All five meta.tag values are extracted and stored. The `contract_guid`, `organisation_guid`, and `grant_expires_at` fields were added in version 2 — these are critical for the composite key return path.
- The push receiver is idempotent: if a request_guid already exists, the record is updated rather than duplicated.
- Receipt acknowledgement to request.pdhc is fire-and-forget — push acceptance is not blocked by upstream response.

#### Poll Reception (Two-Step Sync)

```
provider.pdhc
  |
  |  Step 1: GET /api/v1/provider/feed
  |  Header: X-Provider-Token: <PAT>
  |  → Metadata only (GDPR data minimization)
  |
  |  Step 2: For each new/updated SR:
  |  GET /api/v1/provider/download/{sr_guid}
  |  Header: X-Provider-Token: <PAT>
  |  → Full FHIR Bundle + grant_token
  |
  |  Store: InboundRequest with grant_token, contract_guid, patient_guid
  |  Create: ProviderTask, CarePlanCache
  |  Audit: sync event
```

**Key design decision:** Provider.pdhc auto-detects which mode to use based on config: if `PROVIDER_TOKEN` is set, it uses the PAT-authenticated two-step feed. If only `SSO_API_KEY` is set, it falls back to the legacy `/requests` endpoint.

#### Report Submission (Composite Key)

When a provider completes a task and submits a report, the stored grant metadata is assembled into a composite key:

```
provider.pdhc
  |
  |  1. Load InboundRequest for the task (has grant_token, patient_guid,
  |     contract_guid, organisation_guid from original delivery)
  |  2. POST /api/v1/provider/report/{sr_guid}
  |     Header: X-Provider-Token: <PAT>
  |     Body: {
  |       patient_guid, contract_guid, organisation_guid, grant_token,
  |       status: "completed",
  |       report_payload: { ...observations or freeform... }
  |     }
  |
  v
request.pdhc (gateway) — validates per Section 6
```

**Key design decision:** The `StatusCallbackService` checks for the presence of `grant_token` and `patient_guid` on the InboundRequest. If both exist (new format), it uses the composite key path. If not (legacy format), it falls back to the old status push. This allows mixed-mode operation during migration.

### 5.4 Gateway Receipt Delivery to Provider.pdhc

After gateway.pdhc accepts an observation report and stores it, it pushes a **receipt** back to provider.pdhc confirming ingestion. This closes the data delivery loop with cryptographic proof.

```
gateway.pdhc
  |
  |  POST {PROVIDER_SERVICE_URL}/api/v1/receipts/ingest
  |  Header: X-Service-Key: <internal gateway service key>
  |  Body: {
  |    "receipt_guid": "<generated UUID>",
  |    "service_request_guid": "<sr_guid>",
  |    "patient_guid": "<patient_guid>",
  |    "provider_org_guid": "<org_guid>",
  |    "contract_guid": "<contract_guid>",
  |    "observations_stored": 3,
  |    "accepted_at": "2026-03-26T07:00:00Z",
  |    "payload_hash": "<SHA-256 of stored payload>"
  |  }
  |
  v
provider.pdhc
  |  1. Validate X-Service-Key against GATEWAY_SERVICE_KEY config
  |  2. Deduplicate by receipt_guid (idempotent)
  |  3. Store GatewayReceipt record
  |  4. Audit log: gateway_receipt_ingested
  |
  v
  Return: 202 Accepted { receipt_guid, action: created|duplicate }
```

**Key design decisions:**
- Auth uses `X-Service-Key` (internal service key), not PAT or API key. This is a machine-to-machine channel between gateway.pdhc and provider.pdhc.
- Gateway receipt delivery is fire-and-forget from the gateway side — it does not block the 202 response to the original report submission.
- The `payload_hash` allows provider.pdhc to verify that what the gateway stored matches what was sent.
- Receipts are displayed in the provider dashboard under the "Gateway" nav section.

---

## 6. Gateway Validation: The Report Endpoint

When the gateway receives a report (from 1177 or a provider), the validation chain is:

```
POST /api/v1/provider/report/{sr_guid}
  |
  |  LAYER 1: PAT Authentication (middleware)
  |  ─────────────────────────────────────────
  |  1. Extract X-Provider-Token header
  |  2. Load all non-revoked PATs from database
  |  3. bcrypt.checkpw(raw_token, stored_hash) for each — find match
  |  4. Verify PAT is not expired/revoked
  |  5. Verify PAT has required scope ('write' for report)
  |  6. Set g.provider_org_guid and g.provider_contract_guid from PAT
  |     → Provider identity is DERIVED FROM THE TOKEN, never from request body
  |
  |  LAYER 2: Request Validation (endpoint)
  |  ──────────────────────────────────────
  |  7. Require JSON body
  |  8. Require fields: patient_guid, organisation_guid, grant_token
  |  9. Cross-check: body.organisation_guid == g.provider_org_guid (from PAT)
  |     → Prevents org impersonation even with a valid grant token
  |
  |  LAYER 3: Composite Key Validation (report_service)
  |  ──────────────────────────────────────────────────
  |  10. ServiceRequest exists with matching patient_guid
  |      → 404 if SR not found; 400 if patient mismatch (with audit)
  |  11. Contract match lookup (OPTIONAL):
  |      Query ServiceRequestContractMatch by sr_guid + org_guid + contract_guid
  |      → May return None for direct 1177 delivery — this is OK
  |  12. DataExchangeGrant validation:
  |      a. Find grant by sr_guid + org_guid + contract_guid (not revoked)
  |      b. grant.is_valid() — check expiry, max_uses, revocation
  |      c. grant.patient_guid == submitted patient_guid
  |      d. hmac.compare_digest(grant.grant_token, submitted_grant_token)
  |         → Constant-time comparison prevents timing attacks
  |      → 403 if any check fails (with audit)
  |  13. Record grant use: increment used_count, audit log
  |
  |  LAYER 4: State Update
  |  ────────────────────
  |  14. If contract match exists:
  |      match.status = report_status (if valid) or 'acknowledged'
  |      match.response_at = now
  |      match.response_payload = { status, payload, received_at }
  |  15. If no contract match: response stored on SR directly (direct delivery)
  |  16. Commit
  |
  |  LAYER 5: Audit
  |  ─────────────
  |  17. Log report.received event with full context:
  |      patient_guid, provider_org_guid, contract_guid, report_status
  |      data_subject_guid = patient_guid (for GDPR queries)
  |
  v
  Return: { status: 'recorded', match_status: 'completed' | 'direct' }
```

### 6.1 Defense in Depth

The validation chain implements defense in depth — each layer catches different attack scenarios:

| Layer | What It Catches |
|-------|----------------|
| PAT authentication | Unauthorized systems, expired/revoked tokens |
| Org cross-check | A valid provider trying to submit as another org |
| SR + patient check | Grant replay against wrong SR or wrong patient |
| Contract match (optional) | Verifies the provider-contract relationship |
| HMAC validation | Forged or tampered grant tokens |
| Expiry check | Grants used after their authorized window |
| Max uses check | Grants used more times than authorized |
| Revocation check | Explicitly revoked grants |

### 6.2 Why the Contract Match Is Optional

In the original design, every report required a contract match. This blocked the 1177 direct delivery path: when request.pdhc pushes forms directly to 1177 (not through a contract-matched provider), there is no ServiceRequestContractMatch record. Making the match optional enables both delivery paths through the same endpoint:

- **With match:** Update match status and payload → `match_status: 'completed'`
- **Without match:** Grant validation is the sole auth → `match_status: 'direct'`

---

## 7. End-to-End Data Flow Summary

```
OUTBOUND (request.pdhc → destinations)
═══════════════════════════════════════

                                    ┌─── Provider (push, with PAT endpoint)
                                    │    Bundle: SR + Binary render-ready
                                    │    Auth: X-API-Key (mutual)
                                    │    Tags: receipt_token + grant_token + ...
                                    │
request.pdhc ──push_all_matches()──┤
                                    │
                                    └─── 1177.pdhc (webhook push)
                                         Bundle: SR (Questionnaires as contained)
                                         Auth: X-API-Key (configured)
                                         Tags: grant_token + ... (no receipt_token)

                                    ┌─── Provider (poll, no push)
request.pdhc ◄──provider/feed──────┤    GET feed → metadata only
             ◄──provider/download──┘    GET download → full Bundle + grant


INBOUND (destinations → gateway)
════════════════════════════════

1177.pdhc ──────────┐
                    │    POST /api/v1/provider/report/{sr_guid}
                    ├──► gateway.pdhc (request.pdhc Provider API)
                    │    Auth: X-Provider-Token (PAT)
provider system ────┘    Body: patient_guid + org_guid + grant_token + payload

                         Validation: PAT → org cross-check → SR exists →
                         patient match → grant HMAC → expiry → usage → audit

provider system ───────► POST /api/v1/provider/receipt/{token}/ack
                         Auth: X-Provider-Token (PAT)
                         Body: { status: accepted/rejected }
                         (Simpler callback using receipt bearer token)


RECEIPT RETURN (gateway → provider)
═══════════════════════════════════

gateway.pdhc ──────────► POST /api/v1/receipts/ingest
                         Auth: X-Service-Key (internal)
                         Body: receipt_guid + sr_guid + observations_stored
                         + payload_hash
                         ──────────► provider.pdhc stores GatewayReceipt
                                     (proof of observation ingestion)
```

---

## 8. Failure Modes and Recovery

| Failure | Impact | Recovery |
|---------|--------|----------|
| Push to provider fails (network) | Receipt marked `failed`, match stays `pending` | Retry via UI (push again) |
| Push to 1177 fails (network) | Logged, no receipt | Retry via push_all_matches |
| 1177 webhook rejects (400/500) | Logged with HTTP status + error body | Fix payload issue, retry |
| 1177 dispatch to gateway fails | Patient sees success; QR stored locally | Manual re-dispatch or API retrieval |
| Gateway rejects report (403) | Grant invalid/expired/revoked | Re-issue grant (requires new push) |
| Gateway rejects report (400) | Patient mismatch or missing fields | Fix data, re-submit |
| PAT expired during poll window | Provider gets 401 | Re-issue PAT |
| Grant expired before patient completes form | Gateway returns 403 | Re-push SR with new grant |

**Design principle:** Local state is always saved before remote calls. If a remote call fails, the local record preserves what was attempted and enables retry. The patient's local experience (form submission confirmed) is never degraded by downstream failures.

---

## 9. Security Properties

**Confidentiality:**
- All transfers over HTTPS
- Patient data minimized in listings (feed returns metadata only)
- Grant tokens are opaque (HMAC, not JWT — bearer cannot decode)
- PAT raw tokens stored only as bcrypt hashes

**Integrity:**
- HMAC-SHA256 prevents grant token forgery
- `hmac.compare_digest` prevents timing-based attacks on token comparison
- Org identity derived from PAT (server-controlled), not from request body
- Body org is cross-checked against PAT org as defense in depth

**Authorization:**
- PAT scopes (read/write) enforced per endpoint
- Grant tokens bind authorization to specific SR + patient + org + contract
- Grant expiry and max_uses limit authorization window
- Grant revocation provides emergency kill switch

**Non-repudiation:**
- Every grant issuance, use, and validation is audit-logged
- All audit entries include `data_subject_guid` for GDPR traceability
- Correlation IDs thread through cross-service calls
- Delivery receipts with timestamps prove delivery was attempted/succeeded

**Privacy:**
- Feed endpoint returns no patient data (GDPR data minimization)
- Patient excerpt in Bundle is minimized (no address, telecom)
- Audit logs indexed by `data_subject_guid` for right-of-access queries

---

## 10. Configuration Dependencies

For the transfer design to function, these environment variables must be set:

**request.pdhc (outbound):**
- `HMAC_SECRET` — server secret for grant token computation (critical, must never leak)
- `FORMS_1177_WEBHOOK_URL` — 1177.pdhc webhook endpoint
- `FORMS_1177_API_KEY` — API key for 1177 webhook authentication
- `FORMS_1177_ORG_GUID` — organisation GUID to use for 1177 grants
- `PROVIDER_GRANT_EXPIRY_HOURS` — default grant lifetime (default: 72 hours)
- `PUSH_TIMEOUT_SECONDS` — HTTP timeout for push calls (default: 30)

**1177.pdhc (inbound webhook + outbound dispatch):**
- `API_KEY` — expected X-API-Key for webhook authentication
- `GATEWAY_URL` — gateway base URL for response dispatch
- `GATEWAY_PROVIDER_TOKEN` — PAT for authenticating to gateway as provider

**request.pdhc gateway / Provider API (inbound reports):**
- `HMAC_SECRET` — same secret as outbound (for grant validation)
- PAT records in `provider_access_tokens` table (per-provider)
- `PAT_DEFAULT_EXPIRY_DAYS` — default PAT lifetime (default: 365 days)

**provider.pdhc (push reception + poll sync + report submission + receipt ingestion):**
- `PROVIDER_GUID` — this instance's provider organisation identity
- `PROVIDER_TOKEN` — PAT issued by request.pdhc (enables PAT-based feed/download/report)
- `REQUEST_SERVICE_URL` — upstream request.pdhc base URL (default: `https://request.pdhc.se/api/v1`)
- `PUSH_SECRET` — shared secret for validating inbound pushes from request.pdhc
- `GATEWAY_SERVICE_KEY` — internal service key for validating receipt pushes from gateway.pdhc
- `SYNC_ENABLED` — enable background polling (`true`/`false`)
- `SYNC_INTERVAL_SECONDS` — polling interval (default: 60)
- `SSO_API_KEY` — legacy API key fallback (deprecated, kept for backward compatibility)

**gateway.pdhc (receipt delivery to provider.pdhc):**
- `PROVIDER_SERVICE_URL` — provider.pdhc base URL for receipt delivery (e.g. `http://localhost:9070/api/v1`)
