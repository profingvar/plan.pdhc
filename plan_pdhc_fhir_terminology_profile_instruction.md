# plan.pdhc — Implement a conformant FHIR R5 terminology profile

**Status:** **IMPLEMENTED 2026-06-22.** All §6 work items shipped; §7
non-goals declared in CapabilityStatement; §8 sequencing followed
end-to-end. Test count 76 → 195 across the implementation. See
`plan_pdhc_fhir_terminology_profile_DECISIONS.md` for the locked
decisions (all five APPROVED) and `progress.md` for the per-step
landing log.

**Outstanding (not blocking ship):** CI job for `make conformance`
(Risk §9.4 — devops); three open questions at the bottom of the
ADR. Both are post-deploy work.

**Audience:** plan.pdhc developers (now also: future maintainers
extending the FHIR terminology surface).
**Golden rule:** *Add* a conformant FHIR terminology surface. Do **not** remove,
rename, or change the behaviour of any endpoint that currently works. Every new
operation is additive and lives behind new routes or new query parameters.

---

## 1. Why this work exists

The paper's Limitations section states that plan.pdhc "exposes a partial FHIR
terminology surface but does not yet publish its value sets, its local concept
system, and its canonical bindings as conformant FHIR ValueSet, CodeSystem, and
ConceptMap resources with the standard `$expand`, `$lookup`, and `$translate`
operations." This document specifies exactly what to build to close that gap.

The deliverable is a **FHIR-conformant terminology API profile**: other FHIR
systems should be able to point a generic FHIR terminology client at
plan.pdhc and perform standardized terminology operations without bespoke
integration code.

---

## 2. What already exists — DO NOT BREAK

These are working today and must keep working byte-for-byte unless a change is
explicitly listed in §6. Treat this list as a regression contract.

| Area | Endpoint(s) | File |
|------|-------------|------|
| FHIR CapabilityStatement | `GET /api/v1/metadata` | `app/api/capability.py` |
| Human-readable capability | `GET /api/v1/capability-statement`, `/endpoints` | `app/api/capability.py` |
| FHIR PlanDefinition | `GET /api/v1/PlanDefinition`, `GET /api/v1/PlanDefinition/{id}`, `GET .../{id}/$expand` | `app/api/fhir_plandefinitions.py` |
| FHIR Questionnaire | `/api/v1/forms*`, `/api/v1/form-definitions*` | `app/api/forms.py`, `app/api/form_definitions.py` |
| Code-validation shim | `GET /api/v1/ValueSet/$validate-code?system=&code=` | `app/api/terminology.py` |
| Termbank proxies | `GET /api/v1/termbank/concept/<system>/<code>`, `/api/v1/termbank/search` | `app/api/terminology.py`, `app/services/termbank_client.py` |
| Relational CRUD | `/api/v1/concepts`, `/values`, `/valuesets`, `/canonical-libs`, … | `app/api/*.py` |

**Important caveat about this regression contract:** there are currently **no
automated tests** for any of the endpoints above. `planp/tests/` is empty of
`.py` files. The "do not break" guarantee is therefore unverifiable until
characterization tests are added — see §4 Prerequisites.

**Two behaviours that look like FHIR terminology operations but are NOT, and must
be preserved as-is:**

1. `GET /api/v1/PlanDefinition/{id}/$expand` currently means *"force-regenerate
   the PlanDefinition FHIR JSON from relational data."* This is **not** the FHIR
   ValueSet `$expand`. Leave it untouched. The new ValueSet `$expand` lives on a
   different resource path (`/api/v1/ValueSet/{id}/$expand`).
2. `GET /api/v1/ValueSet/$validate-code?system=&code=` currently answers a
   *global adoption* question ("is this canonical referenced anywhere in
   plan.pdhc?"). Downstream callers (cdr.pdhc's `$validate-code` shim at
   `cdr.pdhc/cdr_app/app/services/plan_client.py` and
   `app/api/fhir_read.py:1034`) depend on this exact contract. Do **not** change
   its semantics in place — see §6.2 for the compatibility strategy.

---

## 3. Data-model facts the implementation must respect

From `app/models/concept_models.py` (verify before coding):

- `Concept` has **one** canonical binding: `canonical_lib` (FK → `canonical_libs.guid`)
  plus `canonical_refnumber`. It also has `status` (default `'draft'`),
  `vers_number`, `concept_name`, `concept_display_text`, `concept_explain`,
  `response_type`, `unit`, `range_low/high`, and an optional `valueset` FK.
- `ValueSet` has `guid`, `canonical_lib`, `canonical_refnumber`, and members via
  `ValueSetValue` (junction) → `ValueCatalog`.
- `ValueCatalog` (individual answer values) has `guid`, `canonical_lib`,
  `canonical_refnumber`, `value_name`.
- `CanonicalLib` is the **authority registry only** (name, display, url). The
  actual canonical codes (SNOMED CT, LOINC, ICD-10) live in the separate
  **termbank.pdhc** service, reached via `TermbankClient` (already implements
  TTL-cached `.lookup()` and `.search()` — §6.3 delegation is wiring, not building).
- `PLAN_BASE = "https://plan.pdhc.se"` is already defined in
  `models/concept_models.py` and is used today as the prefix for relational
  resource URLs. The new FHIR canonical URLs will extend this — see §5.3.

Implication: plan.pdhc is the terminology server for its **local** concept
system, its **value sets**, and the **local→canonical mappings**. It is *not* the
authority for the external canonicals — `$lookup` of an external code is
delegated to termbank.pdhc.

---

## 4. Prerequisites — write the regression contract first

The §2 "do not break" guarantee is the load-bearing constraint of this whole
spec. As of today it is **unenforced**: there are no tests for the §2 endpoints,
and the cross-service contract with cdr.pdhc's `$validate-code` shim is held
together by hope. Before any §6 work begins, these tests must exist.

### 4.1 Characterization tests for the §2 surface

Create `planp/tests/test_existing_fhir_surface.py` (and supporting fixtures)
that pin down the current behaviour of every endpoint in §2:
- Happy-path response shape (key fields present).
- HTTP status code.
- `Content-Type` header.
- For the FHIR-shaped responses, `resourceType` and required top-level fields.
- Pagination shape for searchset Bundles (mirroring `fhir_plandefinitions.py`).

These tests must **not** assert any property the spec wants to change. They
exist to detect regressions, not to lock in correctness.

Estimated ~300 LOC across one or two test files.

### 4.2 Cross-service regression test for the cdr.pdhc shim

Add a test (here, not in cdr.pdhc) that mocks or hits the
`GET /api/v1/ValueSet/$validate-code?system=&code=` endpoint with the exact
parameter shape cdr.pdhc's `plan_client.py` sends, and asserts the response
shape `fhir_read.py:1034` expects. This is the single most important
regression to guard, because it bridges two services in production.

### 4.3 Establish the ADR file

Create `plan_pdhc_fhir_terminology_profile_DECISIONS.md` (sibling of this file)
holding the §5 decisions once locked. Reference it from `progress.md`.

**Done when:** `pytest` runs and the §2 surface plus the cdr cross-service
contract are covered. No §6 work begins before this point.

---

## 5. Decisions to lock before any §6 work

Each decision below has consequences that propagate through the rest of the
implementation. Some are irreversible once external systems start consuming the
output. Capture the choice and rationale in the ADR file (§4.3) before
starting on the affected §6 item.

### 5.1 Local code identity — what is the "code" on the local CodeSystem?

**Choice:** `Concept.guid` vs `Concept.concept_name` vs something else.

**Recommended: `Concept.guid`.** The schema already uses GUIDs everywhere
(Rule 18 — GUID-only for internal refs). GUIDs are stable through rename and
republish; `concept_name` is mutable.

**Trade-off:** GUIDs are not human-readable in raw FHIR. Mitigate by setting
`display = concept_display_text` on every `concept[]` entry and `match[].concept`.

**Irreversibility:** Once a `ConceptMap` is published and external systems
(or even our own cdr.pdhc / observation pipelines) store the source code,
changing identity is a breaking change for them. Lock this **before §6.4**.

### 5.2 CodeSystem cardinality — one CodeSystem or many?

**Choice:** Single CodeSystem for all local concepts, vs one CodeSystem per
ontological domain.

**Recommended: single CodeSystem,** `id = plan-pdhc-local`,
`url = {PLAN_BASE}/fhir/CodeSystem/plan-pdhc-local`. The model is flat (no
domain partitioning in URLs today) and splitting is an additive future move.

**Trade-off:** One large system is less self-describing. Surface the existing
`concept_type` as a `concept[].property` if filtering by domain matters to a
downstream consumer.

### 5.3 Canonical URL scheme for FHIR resources

**Choice:** Keep all routes under `/api/v1/...` (no breakage), or introduce a
`/fhir/...` prefix for FHIR resources.

**Recommended: keep `/api/v1/` for routes; use `{PLAN_BASE}/fhir/{Resource}/{id}`
for the canonical `url` field inside the resource bodies.** That is the form
FHIR clients store, cache, and resolve against. Routes can stay `/api/v1/`
without violating FHIR conformance — only the `url` field is normative.

Centralize URL building in one helper (extend the existing `PLAN_BASE` pattern
in `models/concept_models.py`). Do not let multiple files invent their own form
of canonical URLs — see Risk §9.3.

### 5.4 Version derivation

**Choice:** Per-resource `vers_number` (integer on the underlying model) vs
platform-wide version.

**Recommended: per-resource.** Emit FHIR `version` as `str(vers_number)` on
each resource. A platform-wide version is not needed and would couple
unrelated resources.

### 5.5 FHIR R5 validator — what runs in CI?

**Choice:**
- **(a) HL7 Java `validator_cli.jar`** — canonical, slow, runs in CI via Docker.
- **(b) `fhir.resources` Python library** — shape-check only (pydantic models);
  no operation-conformance; fast.
- **(c) Inferno / Touchstone hosted** — external dependency, slow CI.

**Recommended: (a) for the final DoD, (b) as a development-time fast-feedback
layer alongside.** Add `fhir.resources` to `requirements.txt` for unit tests;
add an opt-in `make conformance` (and CI job) that runs `validator_cli.jar` in
a container against a corpus of sample resources.

Plan one full day for CI wiring of (a).

---

## 6. Work items

Each item is additive. For each, build behind a new route, add tests, and update
the CapabilityStatement (§6.7) to declare it. Use the existing
`_operation_outcome()` and `_validate_parameters()` helpers in
`terminology.py` as the pattern for FHIR-shaped responses.

### 6.1 Publish ValueSets as FHIR `ValueSet` resources + `$expand`

**Build:**
- `GET /api/v1/ValueSet/{guid}` → a FHIR R5 `ValueSet` resource (with `url`,
  `version`, `status`, `compose`).
- `GET /api/v1/ValueSet?url=&_count=&_offset=` → FHIR `searchset` Bundle (mirror
  the paging pattern already in `fhir_plandefinitions.py`).
- `GET /api/v1/ValueSet/{guid}/$expand` and `POST /api/v1/ValueSet/$expand`
  (Parameters body) → a `ValueSet` with a populated `expansion.contains[]`, each
  entry carrying `system`, `code`, `display`. Build the expansion from
  `ValueSetValue` → `ValueCatalog`, resolving `canonical_lib` to its
  `canonical_lib_url` for the `system`.

**Keep working:** the existing custom `/api/v1/valuesets/{guid}` CRUD JSON is
unchanged. The new FHIR representation is a **separate** capital-`V` route
(`/ValueSet`), exactly as PlanDefinition already has both `/plandefinitions`
(CRUD) and `/PlanDefinition` (FHIR).

**Done when:** a FHIR client can read a ValueSet and expand it; output validates
against the chosen validator (§5.5); the custom CRUD characterization tests still pass.

### 6.2 Make `$validate-code` ValueSet-scoped (without breaking the shim)

**Problem:** FHIR `ValueSet/$validate-code` validates a code against a *specific*
ValueSet (by `url`/`valueSet`), but the current endpoint answers a global
adoption question and cdr.pdhc relies on that.

**Strategy — keep both:**
- Preserve the current global behaviour when the request has **no** ValueSet
  identifier (i.e. only `system` + `code`). This is the existing cdr.pdhc
  contract; do not touch its response shape. The §4.2 cross-service test
  enforces this.
- Add proper FHIR semantics when a ValueSet is identified: support
  `GET /api/v1/ValueSet/{guid}/$validate-code?system=&code=` and
  `?url=...&code=...`, plus a `POST` Parameters form. When scoped, validate
  membership against that ValueSet's expansion and return `result`, `display`,
  and a `message` on failure.

**Done when:** cdr.pdhc's existing calls return identical responses; scoped calls
return correct membership results; both paths are covered by tests in
`tests/test_terminology.py`.

### 6.3 Expose the local concept system as a FHIR `CodeSystem` + `$lookup`

**Build:**
- `GET /api/v1/CodeSystem/{id}` → a FHIR `CodeSystem` representing plan.pdhc's
  local concept set. Use the cardinality and identity locked in §5.1/§5.2 (the
  recommended baseline is a single CodeSystem with `Concept.guid` as the
  code). Map `Concept.concept_name`/`concept_display_text`/`concept_explain`
  to `concept[].code/display/definition`; surface `status` and `vers_number`.
- `GET /api/v1/CodeSystem/$lookup?system=&code=` and `POST` Parameters form →
  return the concept's properties for the **local** system.
- **Delegation rule:** when `system` names an external canonical (a registered
  `CanonicalLib` whose codes live in termbank), `$lookup` must delegate to
  `TermbankClient.lookup()` rather than 404. Reuse the existing TTL-cached
  client. Document this delegation explicitly in the CapabilityStatement.

**Keep working:** `canonical-libs` CRUD and the `termbank/concept/...` proxy are
unchanged; `$lookup` is a new, higher-level façade over them.

**Done when:** `$lookup` returns local concept details for the local system and
transparently proxies external systems to termbank.

### 6.4 Expose canonical bindings as a FHIR `ConceptMap` + `$translate`

This is the highest-value item — it is exactly PDHC's local↔canonical mapping
made standard.

**Build:**
- `GET /api/v1/ConceptMap/{id}` → a `ConceptMap` whose `group.element[]` maps each
  local `Concept` (source: local CodeSystem from §5.2, code from §5.1) to its
  `canonical_lib` + `canonical_refnumber` (target). Include
  `ValueCatalog`/`ValueSet` bindings as appropriate.
- `GET /api/v1/ConceptMap/$translate?code=&system=&targetsystem=` and `POST`
  Parameters form → return the mapped canonical code(s) as FHIR `Parameters`
  with `result` + `match[].concept`.

**Note:** each Concept currently holds a single canonical binding, so a translate
result is 0..1 targets per source. **Always return `match[]` as an array**, even
for a singleton, so future multi-binding support doesn't break the contract
(Risk §9.5).

**Done when:** `$translate` round-trips a known local concept to its canonical
code and back; unmapped concepts return `result: false` with a clear message.

### 6.5 FHIR operation I/O conventions (cross-cutting)

Apply uniformly to all new (and, where safe, existing FHIR) endpoints:
- Accept operations via **both** `GET` (query params) and `POST` with a FHIR
  `Parameters` resource body. Add a single shared `_parse_parameters_body()`
  helper.
- Return `Content-Type: application/fhir+json` (the `/metadata` route already
  does this — make the new routes match; do not retrofit the plain-`jsonify`
  PlanDefinition routes if that risks breaking current consumers — add the header
  only where it is safe and tested via the §4.1 characterization layer).
- Return a FHIR `OperationOutcome` (use the existing helper) for all error cases,
  with appropriate HTTP status.
- Keep the existing `200/minute` rate-limit decorator pattern.

### 6.6 Canonical URLs, versioning, and search parameters

- Assign every FHIR terminology resource a stable canonical `url` per §5.3
  (`{PLAN_BASE}/fhir/{Resource}/{id}`) and a `version` per §5.4
  (`str(vers_number)`).
- Support resolution by canonical URL: `GET /api/v1/ValueSet?url=...`,
  `/CodeSystem?url=...`, `/ConceptMap?url=...`.
- Centralize the URL builder in **one** helper next to `PLAN_BASE` in
  `models/concept_models.py`. Do not hardcode the scheme in multiple files
  (Risk §9.3).

### 6.7 Update the CapabilityStatement to be accurate

`app/api/capability.py` currently both over- and under-states reality (it
documents ValueSet as "not FHIR format", and lists the PlanDefinition `$expand`
as if it were a terminology op). After each work item ships:
- Add `ValueSet`, `CodeSystem`, and `ConceptMap` resource entries with their real
  `interaction` and `operation` lists (`expand`, `validate-code`, `lookup`,
  `translate`).
- Explicitly declare which operations are **not** supported and why (see §7).
- Keep the existing PlanDefinition/Questionnaire/FormDefinition entries.

### 6.8 Conformance testing

- Extend the §4 characterization suite with `tests/test_terminology.py` and
  `tests/test_fhir_endpoints.py` cases for each new operation (happy path,
  scoped vs. global validate-code, delegation to termbank, unmapped translate,
  error/OperationOutcome shapes).
- Run all new outputs through the validator chosen in §5.5 — fast Python
  shape-check on every test run, full `validator_cli.jar` corpus check via a
  `make conformance` target and a CI job.
- Add an explicit regression test asserting cdr.pdhc's existing
  `$validate-code` call shape is unchanged (the §4.2 test must continue to
  pass after every §6.2 change).

---

## 7. Explicitly out of scope (declare, don't build)

The local data model is **deliberately flat** — no inter-concept hierarchy. The
following FHIR terminology features cannot be supported meaningfully and must be
declared unsupported in the CapabilityStatement rather than faked:

- `CodeSystem/$subsumes`
- `is-a` / descendant filters in `ValueSet.compose` and in `$expand`
- hierarchical `$lookup` properties (parent/child)

Stating these as intentional non-goals is part of being conformant — a
CapabilityStatement that claims them and then fails is worse than one that
honestly excludes them.

---

## 8. Suggested sequencing

0. **§4 Prerequisites** — characterization tests for the §2 surface AND the
   cdr.pdhc cross-service test. Without these, every later step is flying
   blind on the "do not break" guarantee.
1. **§5 ADR** — lock the five decisions into
   `plan_pdhc_fhir_terminology_profile_DECISIONS.md`.
2. **§6.6 + §6.5 foundation** — canonical URL scheme + Parameters/POST/OperationOutcome
   helpers generalized from `terminology.py`. (Enables everything else.)
3. **§6.1 ValueSet + `$expand`** — most-requested operation, self-contained.
4. **§6.2 scoped `$validate-code`** — builds on the expansion from §6.1.
5. **§6.4 ConceptMap + `$translate`** — highest external value; data already present.
6. **§6.3 CodeSystem + `$lookup`** with termbank delegation.
7. **§6.7 + §6.8** — CapabilityStatement truth-up and conformance tests, run
   continuously, finalized last.

---

## 9. Risks to monitor through the build

1. **CDR regression risk.** Existing global `$validate-code` shape is consumed
   by `cdr.pdhc/cdr_app/app/services/plan_client.py` and
   `app/api/fhir_read.py:1034`. Any inadvertent shape change breaks
   production. **Mitigation:** §4.2 cross-service test in CI.
2. **Irreversible local-code identity.** Once a `ConceptMap` is published and
   external systems (including our own cdr/observation pipelines) store the
   source code, changing identity costs them. **Mitigation:** lock §5.1 in the
   ADR before any §6.4 work; treat the local code as a public contract from
   day one.
3. **URL scheme drift.** Mixing `/api/v1/` routes with
   `{base}/fhir/{Resource}/{id}` canonical URLs is fine **if consistent**. If
   multiple files invent their own form, FHIR client caching breaks and
   debugging is miserable. **Mitigation:** single URL-builder helper next to
   `PLAN_BASE`; lint or test that no other file hardcodes the scheme.
4. **Validator infra long-tail.** §6.8's "CI runs the terminology conformance
   suite" is easy to defer until DoD is "almost done forever". **Mitigation:**
   wire the §5.5 validator in CI *during* the §6.6 foundation step, before
   any of §6.1-§6.4 — that way every later commit is conformance-checked.
5. **Single canonical binding per Concept assumed everywhere.** Today's model
   gives 0..1 canonical per Concept; tomorrow could be 0..N. **Mitigation:**
   `match[]` in `$translate` and `expansion.contains[]` in `$expand` are
   already array-shaped — keep them arrays even for current 0..1 cases, and
   never collapse to a singleton in serialization.
6. **No FHIR validator dependency today.** `requirements.txt` has no
   `fhir.resources`, no Java JAR pinning. Adding either is a supply-chain
   decision (size, transitive deps, CVE surface). **Mitigation:** pin exact
   versions in `requirements.txt` and the CI image; review on each upgrade.

---

## 10. Definition of done

- **Prerequisites (§4) are landed and green** — characterization tests for the
  §2 surface exist and pass; the cdr.pdhc cross-service `$validate-code` test
  exists and passes; the §5 ADR file is committed.
- All endpoints in §2 still pass their characterization tests (regression
  contract held).
- New `ValueSet`, `CodeSystem`, and `ConceptMap` resources read, search by `url`,
  and support `$expand`, `$lookup`, `$translate`, and scoped `$validate-code`.
- External canonical `$lookup` transparently delegates to termbank.pdhc.
- Responses are `application/fhir+json`, accept `GET` and `POST`+Parameters, and
  emit `OperationOutcome` on error.
- The CapabilityStatement accurately lists supported and unsupported operations.
- Representative outputs pass the validator chosen in §5.5; CI runs the
  terminology conformance suite on every change to `app/api/` and
  `app/services/termbank_client.py`.
- `progress.md` and `changed_files.md` updated per repo Rule 4 / Rule 17;
  `top_rules.md` untouched (Rule 1).

---

*This is fill-in-and-conform work, not greenfield — but the "do not break"
guarantee in §2 has no enforcement today, so §4 Prerequisites is the first
real step.*
