# plan.pdhc FHIR R5 terminology profile — decisions record

**Status:** Draft, awaiting sign-off.
**Date:** 2026-06-22.
**Companion to:** [`plan_pdhc_fhir_terminology_profile_instruction.md`](plan_pdhc_fhir_terminology_profile_instruction.md) §5.
**Why this file exists:** the spec doc defers five decisions to the implementer.
Each has consequences that propagate through every §6 work item, and some are
irreversible once published. This file is where the decisions get locked. No
§6 implementation begins until each section below is marked **APPROVED**.

For each decision: the recommended pick, the rationale, the alternatives that
were considered, the concrete consequences, and the reversibility cost.

---

## D1 — Local code identity

**Decision (recommended):** the local FHIR `CodeSystem`'s `concept[].code`
shall be the `Concept.guid` (UUID string).

### What "code" means in FHIR

In a FHIR `CodeSystem`, `concept[].code` is **the string a consumer stores
as identity**. When cdr.pdhc records "this observation references
plan-pdhc-local code X", or a downstream analyse.pdhc pivot groups by
"this plan.pdhc concept", X is what lives in their row. Same for
`ConceptMap.group.element[].code` — that string is the join key against
the rest of the universe. So D1 is really: *which column on the `Concept`
model do external consumers persist as the join key?*

### The four candidates on the `Concept` model

| Field | Stable? | Human-readable? | Editable via UI? |
|---|---|---|---|
| `guid` | yes (PK, never changes) | no (UUID) | no |
| `concept_name` | no (auto-renamed on duplicate; editable from builder UI) | yes | yes |
| `concept_display_text` | no (free-form Swedish text) | yes | yes |
| `canonical_refnumber` | stable within a `canonical_lib` but **NOT a local identity** — it's the external code (e.g. `4548-4` for LOINC HbA1c) | depends | no |

`canonical_refnumber` is tempting because it's stable, but it isn't a
*local* identity — it's the canonical's code. Two `Concept` rows can
share the same `canonical_refnumber` if they bind to different
`canonical_lib`s, and a Concept may have *no* canonical binding (early
draft, locally-defined). It can't carry the local-identity contract.

That leaves `guid` vs `concept_name`.

### Rationale — GUID is already the cross-service identity

This is the strongest argument:
`cdr.pdhc/cdr_app/app/services/plan_client.py:216` already does this:

```python
def resolve_concept(self, guid: str) -> dict | None:
    """Look up plan.pdhc /api/v1/concepts/<guid>..."""
    url = f"{self.base_url}/api/v1/concepts/{guid}"
```

This is invoked when sim or another upstream sends a FHIR `coding[]`
with `system=https://plan.pdhc.se/Concept` and `code=<guid>`. **The
GUID is already the cross-the-wire identity for a plan.pdhc local
concept in production today.** D1 makes the same choice explicit at
the FHIR CodeSystem layer, instead of inventing a second identity for
the new surface.

Additional supporting reasons:
- Immutable by schema (the PK never changes).
- Rule 18 codebase preference — GUID-only for inter-service refs.
- No `concept_name` ambiguity (see failure modes below).

### Alternatives considered

**`concept_name`** — concrete failure modes that disqualify it:
1. **Edit-from-UI silently changes identity.** A clinician opens the
   builder and renames `hba1c` to `hba1c_blood`. Every downstream row
   keyed on `hba1c` is now orphaned. plan.pdhc has no edit-log
   subscription for external systems.
2. **Auto-rename on conflict produces unexpected codes.** The existing
   `_setup_concept_deps` fixture exposed this: posting
   `concept_name='duplicate_test'` twice yields `duplicate_test_1` the
   second time. An external system expecting to find `duplicate_test`
   finds nothing; the new row's identity drifted under it.
3. **No uniqueness across `canonical_lib`.** Two libs can both have a
   `concept_name='glucose'`. The FHIR `code` must be unique per
   CodeSystem (D2's single CodeSystem makes that mandatory). Either we
   add a global-uniqueness constraint (schema change + migration) or
   accept ambiguity. Both worse than just using GUID.

Rejected.

**`concept_display_text`** — same problems as `concept_name`, plus
more explicitly a human label. Rejected.

**A new stable slug column on `Concept`** — could work if the column
is frozen (no UI edits, uniqueness enforced). But that's a bigger
schema-and-UX change than D1 itself and contradicts how the builder
currently works. **Not rejected outright** — it remains an additive
future option: we can add a `slug` column later and start emitting
slugs alongside GUIDs in a future version, marking GUIDs deprecated.
The current decision doesn't preclude that.

### Display strategy (so humans never see raw UUIDs)

GUID as `code` doesn't mean clients render UUIDs to humans. The FHIR
pattern is:

```json
{
  "code": "8c7f3a16-b482-4e2a-87f8-29c8d8c9c4d5",
  "display": "HbA1c"
}
```

Every emission of `concept[].code` is paired with
`display = concept_display_text || concept_name`. UIs render `display`;
consumers store `code`. Same applies to `ConceptMap.group.element[].code/display`
and `$lookup` responses. The user-facing pain is zero; the
integration-side pain is "UUIDs are ugly in logs", which is true but
irrelevant for correctness.

### Consequences

- Every `ConceptMap.group.element[].code` (§6.4) emits a `Concept.guid`
  as source code.
- Every `CodeSystem.concept[].code` (§6.3) emits a `Concept.guid`.
- `display` is **always** set to `concept_display_text` (falling back
  to `concept_name` when display text is null).
- The §6.3 `$lookup` operation accepts the GUID as the `code` parameter
  (when `system` matches the local CodeSystem URL).
- The cdr.pdhc indirection at `plan_client.py:216` keeps working
  unchanged — D1 simply formalises what it already does.

### Reversibility — HARD once published

Once external consumers persist `(plan-pdhc-local-codesystem-url, <code>)`
rows, changing what's in the `code` position requires **coordinated
migration at every consumer.**

If we ship with GUID and later want to switch to `concept_name` (or a
slug), the migration playbook is:

1. Emit BOTH for one deprecation window — GUID in `code`, the new
   identifier as `designation` or a `property`.
2. Every consumer reads both, double-stores or rewrites existing rows.
3. Flip the canonical position: emit the new identifier in `code`,
   GUID as legacy alias.
4. Drop the alias after a grace period.

Doable but expensive in cross-team coordination — and worse, the
migration breaks if any consumer is offline during the window.

**Asymmetry that favours starting with GUID:** starting with GUID and
then needing a friendlier identifier later is easier than the reverse,
because GUID is stable. The reverse direction (start with `concept_name`,
later need GUID) has to handle in-flight renames during the deprecation
window — every concurrent UI edit becomes a migration hazard. So even
if there were only 80% confidence GUID is right, the recovery path from
"wrong choice" is gentler in this direction.

**Status:** ☑ APPROVED 2026-06-22 / ☐ modified / ☐ rejected.

---

## D2 — CodeSystem cardinality

**Decision (recommended):** a single FHIR `CodeSystem` for all local
plan.pdhc concepts. Resource identity:
- `id`: `plan-pdhc-local`
- `url`: `{PLAN_BASE}/fhir/CodeSystem/plan-pdhc-local`
- Routes: `GET /api/v1/CodeSystem/plan-pdhc-local`,
  `GET /api/v1/CodeSystem/$lookup?system={url}&code={guid}` (see D3 for the
  URL/route relationship).

**Rationale.** The `Concept` model is flat — no domain partitioning is
exposed in URLs today. Splitting into multiple CodeSystems is additive and
can be done later by adding a `concept_type → CodeSystem` mapping, with no
breakage of D1's GUID-as-code contract.

**Alternatives considered:**
- One CodeSystem per `concept_type` (observation, medication, condition…).
  Looks tidier but adds resource-cardinality and discovery complexity for
  zero current consumer value. Defer until a consumer asks. Rejected.
- One CodeSystem per `canonical_lib` adoption set. Conflates "concepts we've
  defined locally" with "canonicals we've adopted from termbank" — the two
  belong on different resources (CodeSystem vs ConceptMap). Rejected.

**Consequences:**
- §6.3 `$lookup` for the local system has exactly one code-space to scan.
- `Concept.concept_type` is surfaced as a `concept[].property` so downstream
  consumers can filter by domain without us splitting the resource.
- §6.4 ConceptMap's `group.source` is the single canonical URL above.

**Reversibility:** **EASY** in principle (publish additional CodeSystems
later without removing the umbrella one) but **HARDER if we narrow the URL
later** (splitting changes the source URL on every ConceptMap.group). Stay
unsplit unless a real consumer asks.

**Status:** ☑ APPROVED 2026-06-22 / ☐ modified / ☐ rejected.

---

## D3 — Canonical URL scheme

**Decision (recommended):** routes remain under `/api/v1/...`. The FHIR
canonical `url` field on each resource shall use the form
`{PLAN_BASE}/fhir/{Resource}/{id}`. The canonical URL is an **identifier**
and is not required to resolve — FHIR clients treat it as an opaque
identifier for caching and reference, not as a URL to GET.

Concretely:
| Resource | Route (what GETs work) | `url` field value (identifier) |
|---|---|---|
| ValueSet | `GET /api/v1/ValueSet/{guid}` | `{PLAN_BASE}/fhir/ValueSet/{guid}` |
| CodeSystem | `GET /api/v1/CodeSystem/plan-pdhc-local` | `{PLAN_BASE}/fhir/CodeSystem/plan-pdhc-local` |
| ConceptMap | `GET /api/v1/ConceptMap/{id}` | `{PLAN_BASE}/fhir/ConceptMap/{id}` |

A single URL-builder helper (added in `app/models/concept_models.py`
next to `PLAN_BASE`) is the only place these strings are constructed —
all other files import from it. Lint test will assert no other file
hardcodes `/fhir/`.

**Rationale.** Two separate concerns:
1. *Where the implementation lives* — `/api/v1/...` keeps the existing
   route structure, no nginx config change, no consumer breakage.
2. *What the FHIR identifier is* — `/fhir/{Resource}/{id}` is the form
   external FHIR clients store, cache, and use in `reference`,
   `valueSet`, and `system` fields. Conflating it with the route would
   force a route migration (and the consequent rewrites everywhere).

**Alternatives considered:**
- Move routes to `/fhir/...` directly. Breaks the existing reverse-proxy
  configuration, the existing UI calls, and cdr.pdhc's hardcoded
  `/api/v1/...` paths. Rejected.
- Use a single URL form for both (canonical = route). Same problem.
  Rejected.

**Consequences:**
- The URL field in resources points to identifiers that may 404 if a
  client follows them. This is FHIR-compliant; clients are not supposed to
  follow the canonical URL as a resolution endpoint. (Resolution happens
  via the operation's `?url=...` query parameter on `/api/v1/`.)
- The URL-builder helper is the single source of truth. Anything that
  hardcodes `/fhir/` outside that helper is a lint failure.
- §6.6 `searchParam` resolution by URL: `GET /api/v1/ValueSet?url=...`
  must accept either the new canonical form OR a legacy
  `{PLAN_BASE}/api/v1/...` form during the transition (D3.b below).

**D3.b — Legacy URL acceptance (transition).** During §6 rollout the
existing CRUD models emit URLs like
`{PLAN_BASE}/api/v1/valuesets/{guid}`. After §6.1, ValueSet acquires the
new canonical form `{PLAN_BASE}/fhir/ValueSet/{guid}`. To avoid breaking
any in-flight consumer:
- `GET /api/v1/ValueSet?url=...` must match BOTH forms during transition.
- The new canonical form is the only one returned in NEW responses.
- The legacy `url` fields on `valuesets/<guid>` lowercase-CRUD JSON stay
  unchanged (per §2 regression contract).

**Reversibility:** **MEDIUM**. Changing the canonical URL pattern later
requires a one-time identifier rewrite at every consumer. Doable but
disruptive. The choice to keep routes at `/api/v1/` is easily reversible
because routes are not normative.

**Status:** ☑ APPROVED 2026-06-22 / ☐ modified / ☐ rejected.

---

## D4 — Version derivation

**Decision (recommended):** each FHIR terminology resource emits its
`version` field as `str(vers_number)` where `vers_number` is the integer
column already on the underlying SQLAlchemy model. No platform-wide
version. No `0.x` / semver translation.

**Rationale.** Each resource has its own lifecycle (a ValueSet can be
edited without bumping a CodeSystem). Coupling them via a global
version invents work and ambiguity. The plain integer is precise:
"version 7" of a ValueSet is unambiguous.

**Alternatives considered:**
- A semver-shaped `1.7.0` style. Implies semantic compatibility
  promises we don't make. Rejected.
- A platform-wide single version on `/metadata`. Useful for
  CapabilityStatement (where it stays), but coupling resource versions
  to it would force gratuitous bumps. Rejected.

**Consequences:**
- `Concept.vers_number` → `CodeSystem.concept[]` properties carry their
  per-concept version (or roll up into a single `vers_number` on the
  parent CodeSystem — TBD in §6.3 review).
- `ValueSet.vers_number` → `ValueSet.version`.
- The CapabilityStatement keeps its own `API_VERSION` constant unchanged.

**Reversibility:** **EASY**. Version format is per-response; we can
switch to semver later by changing the URL-builder helper's version
emission. No external migration.

**Status:** ☑ APPROVED 2026-06-22 / ☐ modified / ☐ rejected.

---

## D5 — FHIR R5 validator in CI

**Decision (recommended):** two layers.
1. **Fast layer:** add `fhir.resources` (Python pydantic models) to
   `requirements.txt`. Every test run validates the SHAPE of each new
   FHIR response against the R5 models. Catches missing required fields,
   wrong cardinalities, wrong primitive types. ~10 ms overhead per test.
2. **Slow layer:** the official HL7 Java `validator_cli.jar` runs against
   a corpus of representative resources in a `make conformance` CI job.
   Catches the FHIR-semantic checks `fhir.resources` cannot
   (terminology binding rules, slicing, profile compliance). Runs once
   per CI build via Docker; not on every commit, but on every PR before
   merge.

**Rationale.** Pure-Python layer gives fast feedback in `pytest`; Java
layer gives the canonical conformance verdict. Both are needed: shape
errors caught at unit-test speed, full conformance enforced at PR speed.

**Alternatives considered:**
- Java validator only. Slow feedback loop hurts §6 velocity. Rejected.
- `fhir.resources` only. Misses semantic checks needed for the §7
  CapabilityStatement claims (§4.8 in the original sequencing). Rejected.
- Inferno hosted. External dependency, network-bound, slow CI. Rejected.

**Consequences:**
- `requirements.txt` adds `fhir.resources>=7.0.0` (R5 support).
- Tests in `tests/test_terminology.py`, `tests/test_capability.py`, and
  the new §6 test files validate responses through `fhir.resources`
  pydantic models.
- `planp/Makefile` (new or extended) adds a `conformance` target that
  runs `validator_cli.jar` against fixtures in `tests/fhir_corpus/`.
- CI gains one new job: `conformance`, gating PR merge.
- Day-or-two of one-time devops work to wire the Java jar into the
  Docker image used by CI.

**Reversibility:** **EASY**. Removing either layer later is trivial.
The decision lock is mainly cost (Java jar in CI image, extra Python
dep).

**Status:** ☑ APPROVED 2026-06-22 / ☐ modified / ☐ rejected.

---

## Sign-off

When each decision above is marked **approved**, this document is the
binding ADR for the §6 implementation. Any later change to a decision
requires updating this file and the cross-references in the spec doc,
not silently changing the code.

Approved by: martiningvar Date: 2026-06-22

All five decisions approved as recommended. This ADR is now binding
for §6 implementation.

---

## Open questions for the reviewer (not blocking sign-off)

1. **CodeSystem `concept[].property` schema.** When (not if) we want to
   filter by `concept_type` from a FHIR client, what property URI do we
   coin? Suggestion: `{PLAN_BASE}/fhir/CodeSystem/plan-pdhc-local#concept-type`.
   Decide as part of §6.3 review; doesn't block sign-off here.
2. **`ConceptMap.group` cardinality.** Today every concept has 0..1
   canonical binding. Spec §6.4 says the response shape returns `match[]`
   as an array (future-proof). Should the ConceptMap resource itself
   surface multiple `group[]` entries (one per canonical_lib) or a single
   group with all mappings? Single group is simpler; multi-group is more
   FHIR-idiomatic. Defer to §6.4 review.
3. **§6.2 `$validate-code` POST Parameters form.** The spec says we add
   a POST form alongside the existing GET. Question: does the POST body
   have to match the existing GET response on cdr.pdhc's plan_client?
   Looking at the code, plan_client only ever uses GET — so POST is for
   future external consumers and can be designed cleanly without legacy
   constraints. Confirm before §6.2 work.
