% Guided PlanDefinition authoring — an opt-in, Claude-assisted, guard-railed builder for non-expert authors
% plan.pdhc / PDHC platform
% 2026-07-31

---

## 0. Purpose

Make the production of a `PlanDefinition` (and its `Concept`s, goals and
thresholds) **resilient for a non-expert author**, so someone who is not a
clinical-terminology specialist can build a *correct* plan in the plan.pdhc
builder — one with the right data type, a real terminology binding, a unit
where a unit is required, and a threshold that matches the data it guards.

This document is the offline design rationale for the tool. It commits the
architecture; the code is delivered under tickets **#516 (epic)** and
**#517–#522 (GA-1…GA-6)**.

---

## 1. Why this is needed — the authoring surface today

An audit of the plan.pdhc authoring path (models, routes, API, services)
found that **almost every guardrail a novice needs is missing**, and the few
that exist live only in the web UI and are bypassed by the JSON API:

- The data model is permissive by design — nearly every clinically-meaningful
  column is nullable. The only real DB invariant is `range_low ≤ range_high`
  (`ck_concept_range`).
- **`response_type` is not an enum.** It is a user-editable lookup *table*
  whose meaning is resolved by matching the human-typed name (English *or*
  Swedish) against a hardcoded map in `forms_service.RESPONSE_TYPE_MAP`. A
  typo or a new row silently changes downstream behaviour.
- **Terminology binding is never verified.** `canonical_refnumber` (the LOINC/
  SNOMED code) is optional free text; the termbank service that could check it
  is wired only to the UI autocomplete, never to the save path.
- **The one real cross-field rule** (single-choice ⇒ must have a value set)
  exists only in the web route; the JSON API accepts the invalid state.
- There is **no shared validation service** — web and API each do their own
  thin checks — and **no wizard, assistant, or LLM code** anywhere.

So a non-expert can, today, save: a quantity with no unit; a coded concept
with no answer set; a binding to a code that doesn't exist; a threshold whose
unit contradicts the concept's unit; and a PlanDef with dangling concept
references — all silently accepted.

**MDR context.** A PlanDef's thresholds flow to `request.pdhc`, which applies
them and fires the data-driven alerts — inside the platform's medical-device
scope. A wrong unit or wrong threshold authored by an untrained person is a
**safety-relevant** defect, not cosmetic. That raises the bar for how the
guardrails are built (see §6).

---

## 2. The core design decision — two layers, never one

The single most important decision: **the assistant is not the guardrail.**
An LLM is probabilistic; an invariant must hold for *every* PlanDef, including
those authored through the raw API or with the assistant switched off. So the
tool is two distinct layers with distinct guarantees:

### Layer 1 — deterministic validation (the floor)

A pure, deterministic `plandef_validation.py` shared by *both* the web route
and the JSON API. It encodes the invariants the model is missing and returns
**structured, explainable issues**. It has no LLM in it and no required
network call. This is the layer that actually makes authoring resilient,
because it is the same for everyone.

### Layer 2 — the Claude-backed assistant (the helper)

`plandef_assistant.py` sits *on top* of Layer 1. Its job is the genuinely hard,
human-facing translation that rules cannot do: turn clinical intent into the
right `response_type` + unit + terminology code, **search for an existing
concept before minting a new one**, draft the goal/threshold, and explain
every choice — and every Layer-1 failure — in plain language. Crucially, the
assistant **runs the Layer-1 validators on its own proposal** and returns the
result, so it can never propose something the floor would reject without
saying so.

> **The rule:** the validator refuses invalid PlanDefs; the assistant helps
> the author reach a valid one. Neither substitutes for the other. The
> assistant *proposes*; the tool *disposes*.

---

## 3. Opt-in by design

Per the brief, the whole tool is **optional use**:

- A feature flag `AUTHORING_ASSISTANT_ENABLED` (default **false**) gates the
  entire API surface. Off ⇒ the endpoints report "service disabled" and
  nothing about existing behaviour changes.
- The assistant needs `ANTHROPIC_API_KEY`. With no key, Layer 2 degrades
  gracefully to **validation-only** (Layer 1 still works) and never raises.
- Existing concept/plandef save paths are **untouched** in the first delivery.
  Making Layer 1 *fail-closed on save* is a separate, explicitly
  operator-gated step (**GA-5 / §7**), because it changes the accept/reject
  behaviour of a live device-scope service and needs a data audit first.

This means the tool can ship, be trialled, and prove its worth without any
risk to current authoring — exactly the resilience-without-disruption the
request asked for.

---

## 4. Layer 1 — the invariants

Each is deterministic and explainable. Severity `error` blocks a
future fail-closed save (GA-5); `warning` always informs but never blocks.

| Code | Sev | Rule | Why it matters |
|------|-----|------|----------------|
| `E-UNIT-REQUIRED` | error | a quantity (`numeric`/`numerical`) `response_type` **must** have a `unit` (sliders/integers are dimensionless and exempt) | a quantity with no unit is meaningless downstream and to `request.pdhc` thresholds |
| `E-VALUESET-REQUIRED` | error | single/multiple-choice **must** reference a `valueset` | closes the API bypass; a coded concept with no answer set can't be answered or validated |
| `E-RESPONSE-TYPE-UNKNOWN` | error | `response_type` name must be in the recognised vocabulary (`RESPONSE_TYPE_MAP` + validator aliases for prod names like `numerical`/`Free text`) | a typo silently breaks the form/FHIR mapping |
| `E-TERM-MISSING` | error | `canonical_refnumber` must be present | "full terminology binding" is the whole point; blank = unbound |
| `W-TERM-UNVERIFIED` | warning | the `(canonical_lib, canonical_refnumber)` pair does not resolve in termbank | catches a wrong/typo'd code; warning (not error) because termbank may be unreachable |
| `W-UNIT-CONTRADICTS` | warning | `Transaction.unit` / `Goal.target_unit` differs from the concept's own `Unit` | the free-string duplicate units can silently diverge from the concept |
| `E-DANGLING-REF` | error | `Transaction.concept_guid` / `Goal.concept_guid` / `target_value_guid` must exist | nullable/plain-string refs today allow orphans |
| `E-RANGE-INVERTED` | error | `range_low ≤ range_high` | mirrors `ck_concept_range` for early, friendly feedback before the DB rejects it |
| `W-EMPTY-PLANDEF` | warning | a plandef with no goal or no activity | usually an unfinished draft, worth flagging |

The list is intentionally small, reviewed, and additive — new invariants are
data/rule additions, not redesigns.

---

## 5. Layer 2 — the assistant

**Interface (opt-in, one call):** `suggest_concept(intent_text, model)` →

```json
{
  "reuse_candidates": [ {"concept_guid": "...", "concept_name": "...", "why": "..."} ],
  "proposal": {
    "response_type": "quantity",
    "unit": "mm[Hg]  (display: mmHg)",
    "canonical_lib": "LOINC",
    "canonical_refnumber": "8480-6",
    "valueset": null,
    "range_low": 60, "range_high": 250
  },
  "rationale": "Plain-language explanation for a non-expert…",
  "validation": [ { "code": "...", "severity": "...", "message": "..." } ],
  "model_used": "claude-sonnet-5",
  "assistant_available": true
}
```

**Behaviours that make it safe and useful:**

1. **Search-first.** Before proposing anything new it queries existing
   `Concept`s and the termbank, and surfaces reuse candidates — a novice's
   most common error is re-minting a concept that already exists with a
   curated binding.
2. **Self-checking.** It runs the Layer-1 validators on its own proposal and
   returns the issues, so a proposal is never silently invalid.
3. **Selectable model.** The caller chooses the Claude model from a
   config allowlist (default `claude-sonnet-5`; also `claude-opus-4-8` for the
   hardest terminology judgement calls, `claude-haiku-4-5` for cheap quick
   checks). A non-allowlisted model is rejected.
4. **Graceful degradation.** No key, a network error, or a malformed model
   reply ⇒ a validation-only result with an `assistant_unavailable` reason.
   It never raises into the request.
5. **Reviewed draft, never auto-commit.** The proposal pre-fills the form for
   the author to confirm; it does not write.
6. **No PHI leaves the box.** Only concept/terminology *metadata* and the
   author's free-text intent are sent to the API — never patient data.

### Why an LLM here, and via the API

The translation "clinical intent → correct terminology-bound data element" is
exactly the kind of fuzzy, knowledge-heavy mapping rules can't express but a
capable model does well — *and then the deterministic floor checks its work.*
Running it through the Anthropic **Messages API** (rather than a bundled
model) keeps plan.pdhc dependency-light, lets the operator pick the
cost/quality tier per call, and keeps the key in the server's env.

---

## 6. Safety posture (MDR)

- Layer 1 is **deterministic and reviewed** — the safety-relevant guarantee
  does not depend on model behaviour.
- The assistant's output is a **reviewed draft**; a human author confirms
  before anything is saved. An LLM proposing a binding is fine; an LLM being
  the *only* thing between a novice and a live alert rule is not.
- The fail-closed promotion (GA-5) is **operator-gated** and paired with a
  data audit of existing rows that would newly fail, plus an audited
  per-field override for legitimate edge cases.

---

## 7. Delivery plan (tickets)

| Ticket | Scope | State in first delivery |
|--------|-------|-------------------------|
| **#516** | EPIC / umbrella | — |
| **#517 GA-1** | `plandef_validation.py` + tests | **built** |
| **#518 GA-2** | `plandef_assistant.py` (selectable model) + tests | **built** |
| **#519 GA-3** | opt-in `/api/v1/authoring` surface + config flag | **built** |
| **#520 GA-4** | builder UI Check/Assist panel | follow-up |
| **#521 GA-5** | promote L1 to fail-closed on save | **operator sign-off required** |
| **#522 GA-6** | this doc + user/tech docs + bookkeeping | **built** |

The natural first thing to *use* is GA-1 + GA-3's `/validate` endpoint — a
novice (or the assistant) can check a draft and get a plain list of what's
wrong, with zero risk to existing plans. GA-2 adds the "help me build it"
step. GA-4 puts both behind buttons in the builder. GA-5 — when you're ready,
and only with sign-off — makes the floor mandatory for everyone.

---

## 8. Bottom line

Build it as **"deterministic floor + Claude co-author,"** opt-in, reviewed-draft
only. The floor is what actually makes PlanDef authoring resilient for a
non-expert, because it is identical for every author and every path; the
assistant is what makes reaching a valid plan *easy*, by translating intent
into correct, terminology-bound choices and explaining itself. The model is
selectable so the operator can dial cost against quality, and the whole thing
stays off until switched on — so it can prove itself with no risk to the live
service.
