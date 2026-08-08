# plan.pdhc — User Manual

*Audience: clinical and terminology authors who use the tool. No coding
knowledge assumed.*

---

## 1. What plan.pdhc is

**plan.pdhc is the authoring service for the PDHC platform.** It is where you
*design* the clinical building blocks that every other service later uses to
collect, store, and act on patient data. Nothing here treats a patient — it is
a design workbench. Think of it as the "master library" of the platform:

- **Concepts** — the individual things you can measure or record (e.g. *Systolic
  blood pressure*, *Pain level*, *Diagnosis*). A concept says what data type is
  expected, what unit it uses, what answer options it allows, and which standard
  terminology code (LOINC, SNOMED, ICD-10, KVÅ …) it maps to.
- **PlanDefinitions** — a structured clinical plan built from concepts. A plan
  bundles together **goals** (targets/thresholds to reach), **activities**
  (things to do, e.g. "Measure BP"), and **transactions** (the specific data
  points each activity should collect).
- **Questionnaires / Forms** — authored forms built on top of concepts, produced
  and published as FHIR Questionnaires for data capture.
- **ValueSets and Values** — the reusable answer sets that coded concepts point
  at (e.g. a *Severity* value set of Mild / Moderate / Severe).

Everything you author is versioned and identified by a stable GUID, so
downstream services always reference exactly the concept you built.

Why it matters: a PlanDefinition's thresholds flow onward to `request.pdhc`,
which applies them and raises data-driven alerts. **A wrong unit or a wrong
threshold authored here is a patient-safety issue, not a cosmetic one.** The
tool is deliberately built with guardrails (see §6) for that reason.

---

## 2. The core idea: the unit lives on the concept

This is the single most important modelling rule to understand as an author.

**A concept carries its own canonical unit.** When you say "Systolic blood
pressure is measured in mmHg", you set that unit *once*, on the concept. Every
goal, threshold, activity, and transaction that refers to that concept inherits
the unit from the concept — you do not (and should not) re-type the unit on each
plan.

The plan-building forms deliberately do **not** offer a per-transaction unit
picker. If a stray unit *does* end up on a transaction or a goal target that
disagrees with the concept's own unit, the validator flags it
(`W-UNIT-CONTRADICTS`) so it can be corrected. Set the unit on the concept and
let everything else resolve to it — that keeps a plan automatically in sync when
terminology is later updated.

The same "resolve from the concept" principle applies to code system, concept
type, response type, and bound value set: one concept GUID resolves the whole
tree, so none of it has to be duplicated into the plan.

---

## 3. What you author, step by step

A typical authoring flow:

1. **Create or reuse a Concept.** Give it a name and display text, pick its
   **response type** (numeric quantity, single/multiple choice, free text …),
   set its **unit** if it is a quantity, and bind it to a terminology code
   (`canonical_lib` + `canonical_refnumber`, e.g. LOINC `8480-6`). For coded
   concepts, attach a **ValueSet** of allowed answers.
2. **Build a ValueSet** (if needed) from reusable **Values**, ordered with a
   sort order, and bind it to the concept.
3. **Create a PlanDefinition.** Add:
   - **Goals** — what the plan aims for, optionally with a numeric target,
     operator, range, or a categorical target value.
   - **Activities** — the actions in the plan, each with optional timing
     (frequency/period/duration).
   - **Transactions** — the concrete data points an activity collects, each
     pointing at a concept.
4. **Author a Form / Questionnaire** over your concepts when you need a capture
   form, then **publish** it (published questionnaires become immutable).
5. **Save.** On save the platform runs the deterministic validators; if
   fail-closed enforcement is on, saves with blocking errors are rejected with a
   clear list of what to fix (see §6).

Concepts have a `status` (`draft` by default), so you can work up a draft before
it is relied upon.

### Bulk import

Terminology authors can bulk-load concepts from a spreadsheet. An operator runs
`flask import-concepts <file.xlsx|.csv>` (with an optional `--dry-run` to
validate without committing). Rejected rows are reported with the reason, so a
large curation batch can be cleaned up before it lands.

---

## 4. Signing in and what you are allowed to do

Access is via the platform single sign-on (SSO). Your permissions come from your
SSO account, in three levels:

| Level | Who | Can do |
|-------|-----|--------|
| **read_only** | any signed-in user | browse concepts, plans, value sets, forms |
| **read_write** | a professional whose session includes the **planning** phase (or a superuser) | create/edit/delete concepts, plans, value sets, forms; use the authoring assistant |
| **admin** | a platform superuser | everything, including forcing a save past validation errors (audited) |

You always see the freshest version of your permissions: the tool re-checks your
session with SSO on **every** request, so if your access is changed or revoked
centrally it takes effect immediately — there is no stale cached copy of your
rights.

If SSO asks you to change your password, the tool sends you to the SSO
change-password page before letting you continue.

---

## 5. The FHIR R5 terminology service (for the people who consume your work)

Everything you author is also published, live, as a standards-based **FHIR R5
terminology service** at `/api/v1/`. You do not have to operate this — it is how
other systems read the library you build — but it is useful to know it exists:

- **ValueSet `$expand`** — hand a system your value set and it returns the full
  list of allowed answers.
- **ValueSet `$validate-code`** — check whether a given code is a legal answer in
  one of your value sets.
- **CodeSystem `$lookup`** — look up one of your local concepts and get its
  display text and terminology binding back. (Locally, a concept's *code* is its
  GUID.)
- **ConceptMap `$translate`** — translate between your local concept and its
  external standard code (LOINC/SNOMED/…).

The practical benefit for you: the moment you curate a concept or a value set,
downstream services see the change through these operations — you are the single
source of truth for platform terminology.

---

## 6. The authoring assistant and the guardrails (opt-in)

plan.pdhc includes an **opt-in guided-authoring assistant** designed so that
someone who is *not* a terminology specialist can still build a correct plan. It
is two distinct layers:

### Layer 1 — the deterministic checker (always the floor)

A fixed set of rules, identical for every author and every path, that catches the
mistakes a novice makes. Examples of what it flags:

- a quantity concept with **no unit** (`E-UNIT-REQUIRED`)
- a single/multiple-choice concept with **no answer set** (`E-VALUESET-REQUIRED`)
- an **unknown response type** name (`E-RESPONSE-TYPE-UNKNOWN`)
- a **dangling reference** — a goal/transaction pointing at a concept that
  doesn't exist (`E-DANGLING-REF`)
- an **inverted range** where low > high (`E-RANGE-INVERTED`)
- warnings for a **missing** or **unverified** terminology code, a **unit that
  contradicts the concept's unit**, or an **empty plan**

Each issue comes back with a plain-language message telling you what is wrong.
When fail-closed enforcement is switched on, an `error`-level issue blocks the
save; `warning`s always inform but never block. (An admin can force a save past
errors, and that override is written to the audit log.)

### Layer 2 — the Claude-assisted co-author (the helper)

When enabled and configured, you can describe what you want in plain language
("resting systolic blood pressure, adult") and the assistant proposes a complete,
correct concept: the right response type, unit, terminology code, and any answer
set — and it **searches for an existing concept first** so you don't re-create
one that already exists. It then runs the Layer-1 checker on its own proposal and
shows you the result, so it can never quietly hand you something invalid.

Important properties:

- The assistant **only proposes** — it pre-fills the form for you to review and
  confirm. It never saves on its own.
- It is **off by default** and must be switched on by an operator. When off, the
  assistant endpoints simply report "disabled" and nothing about normal
  authoring changes.
- No patient data is ever involved — only concept/terminology metadata and your
  typed intent.
- The operator can pick which Claude model backs it (a cheaper one for quick
  checks, a stronger one for the hardest terminology calls). Without a key, the
  tool still runs Layer 1 (validation-only) and never breaks.

There is also a "Check openEHR export" helper that asks rosetta.pdhc whether your
concept set can be exported to openEHR, degrading quietly if that service isn't
configured.

---

## 7. Quick reference

- **Where:** `https://plan.pdhc.se`
- **Sign-in:** platform SSO; your role (read-only / read-write / admin) comes
  from your SSO account and the *planning* phase.
- **What you build:** Concepts → ValueSets/Values → PlanDefinitions (goals +
  activities + transactions) → Questionnaires/Forms.
- **Golden rule:** set the **unit on the concept**; everything else resolves to
  it.
- **Safety:** the deterministic validator is the floor; the assistant is the
  helper. The assistant proposes, you dispose.

For the API surface, deployment, and configuration, see `technical.md`.
