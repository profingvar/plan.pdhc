# Plan / Terminology “Early Components” — Comprehensive Description

This document describes, in a detailed and end-to-end way, what the early building blocks in this repository do: **Concepts**, **Values**, **ValueSets**, and how those are used to create **PlanDefinitions** (and later CarePlans). It also wraps up the **backend endpoints** that are needed to provide these services.

The description below is derived from the repository’s implementation, primarily:

- `app/models/concept_models.py` (terminology + lookup table data model)
- `app/api/concepts.py` (Concept CRUD + concept↔valueset value association)
- `app/api/lookup_tables.py` (CRUD for canonical libs, types, units, valuesets, values, and valueset bindings)
- `app/models/fhir_models.py` (FHIR PlanDefinition persistence model)
- `app/models/activity_models.py` (PlanDefinition builder’s “activities + transactions + goals” relational model and FHIR mapping helpers)
- `app/routes/plandefinitions.py` (web UI builder: create/edit PlanDefinitions + persist goals/activities/transactions + generate stored FHIR JSON)
- `app/api/fhir_plandefinitions.py` (FHIR-facing PlanDefinition read/search/expand endpoints)
- `app/services/fhir_service.py` (FHIR serialization, esp. `FHIRService.create_fhir_plandefinition`)
- `app/templates/plandefinitions/builder.html` (2-column builder with inline JavaScript — form builder left, live FHIR JSON preview right)
- `app/api/fhir_valueset.py`, `app/api/fhir_codesystem.py`, `app/api/fhir_conceptmap.py`, `app/api/fhir_helpers.py` (the conformant FHIR R5 terminology profile added 2026-06-22 — see §9 below)

---

## 1) Architectural context (why these components exist)

The system is split into a **web UI** and an **API**, exposed through a reverse proxy. Practically, that means:

- **Terminology primitives** (concepts/values/valuesets and supporting lookup tables) are:
  - Managed via web UI routes (human workflow)
  - Accessible via JSON REST endpoints (programmatic workflow)
- **PlanDefinitions** are:
  - Created/edited primarily through the web builder (interactive UI)
  - Exposed as FHIR PlanDefinition resources (FHIR API)

The intent is to treat Concepts/Values/ValueSets as the “vocabulary” layer, and PlanDefinitions as a reusable “care-plan template” layer that **references** vocabulary items.

---

## 2) Core domain concepts (definitions)

### 2.1 Canonical Library (CodeSystem-like source)

A **Canonical Library** represents a terminology authority or canonical source system (examples: SNOMED CT, LOINC, ICD-10). In the database it is stored as `CanonicalLib` (`canonical_libs` table).

Why it matters:

- Concepts, Values, and ValueSets all optionally (or mandatorily) attach to a canonical library.
- When converting plan structures to FHIR actions/goals, the system attempts to include canonical codings (system + code) if available.

Key fields (as implemented):

- `canonical_lib_name`: required, short identifier/name
- `canonical_lib_display_text`: optional display label
- `canonical_lib_url`: optional URL (used as a coding `system` when present)
- Common metadata: `guid`, `author`, `vers_number`, timestamps

### 2.2 Lookup tables that “shape” a Concept

These are small controlled vocabularies used to constrain or describe how Concepts behave:

- **ConceptType** (`concept_types`): what kind of concept it is (question/measurement/observation etc.)
- **ResponseType** (`response_types`): the “answer shape” (quantity/categorical/single-choice/etc.)
- **Unit** (`units`): measurement unit for quantity concepts
- **PlanDefType** (`plandef_types`): allowed PlanDefinition “type” choices for builder dropdowns
- **IntendedUse** (`intended_uses`): selectable tags for transaction usage contexts in the builder

They matter because they define:

- How the UI should render input controls (e.g., categorical vs numerical)
- Whether a ValueSet is required (there is an explicit business rule for “single choice” response types)
- Which PlanDefinition types are selectable in the builder UI

### 2.3 Value (an individual selectable item)

A **Value** is an individual, atomic term that can appear inside a ValueSet. It is stored as `ValueCatalog` (`values_catalog` table).

Think of a Value as:

- A single selectable response option (“Yes”, “No”, “Mild”, “Moderate”, “Severe”)
- Or a coded term (“Hypertension stage 1”) depending on your use case

Key fields (as implemented):

- `canonical_lib`: required reference to the canonical library (`canonical_libs.guid`)
- `canonical_refnumber`: optional canonical code (string)
- `value_name`: required machine-ish name / key
- `value_display_text`: optional human-friendly label
- `value_explanation`: optional long explanation
- Common metadata: `guid`, `author`, `vers_number`, timestamps

### 2.4 ValueSet (a named collection of Values)

A **ValueSet** is a named collection of Values (stored as `ValueSet` in the `valuesets` table).

Important: In this repo, the data model is very explicit:

- ValueSet metadata is stored in `valuesets`
- Membership is stored in a junction table `valueset_values` (model `ValueSetValue`)

Key fields (as implemented):

- `canonical_lib`: required reference to canonical library
- `canonical_refnumber`: optional canonical reference (string)
- `valueset_name`: required identifier/name
- `valueset_display_text`: optional label
- `valueset_explanation`: optional description/explanation

Membership fields (as implemented):

- `valueset_guid`: ValueSet GUID
- `value_guid`: Value GUID
- `sort_order`: optional ordering value (used when presenting options)

### 2.5 Concept (the central terminology object)

A **Concept** is the system’s main “terminology building block” (stored as `Concept` in `concepts` table). Concepts represent “things you can ask/measure/record” in care plan transactions/goals.

Key Concept fields (as implemented):

- **Identification**
  - `guid` (UUID primary key)
  - `canonical_lib` (required; which canonical library the concept belongs to)
  - `canonical_refnumber` (optional string code in the canonical library)
  - `concept_name` (required string; treated as unique-ish; enforced via name uniqueness service)
  - `concept_display_text` (optional human label)
  - `concept_explain` (optional long explanation)
  - `status` (draft/active/retired-like lifecycle field)
- **Typing / response shape**
  - `concept_type` (optional FK to `concept_types`)
  - `response_type` (optional FK to `response_types`)
  - `unit` (optional FK to `units`)
- **Ranges and UI helpers**
  - `range_low`, `range_high` (numeric; with a DB check constraint \(low \le high\) when both present)
  - `anchor_low_text`, `anchor_high_text` (optional texts for slider-like controls)
- **ValueSet binding**
  - `valueset` (optional FK to `valuesets`)
  - `no_of_values_connected` (counter-like integer; used for filtering “has values”)

How a Concept “connects” to Values:

- A Concept does **not** directly connect to Values.
- Instead, a Concept optionally points to a ValueSet (`Concept.valueset`).
- The ValueSet then lists its Values via `ValueSetValue` rows.

This design makes “allowed answers” reusable: multiple Concepts can point at the same ValueSet.

---

## 3) CRUD and management capabilities (what you can actually do)

This section is explicitly aligned to the functionality exposed in:

- `app/api/concepts.py`
- `app/api/lookup_tables.py`
- and the corresponding web UI routes

### 3.1 Create and manage Concepts

Capabilities implemented:

- **List/search/filter Concepts**
  - Filter by text search (`concept_name`, `concept_display_text`, `concept_explain`)
  - Filter by `concept_type`, `response_type`, `canonical_lib`
  - Filter by “has values” (using `no_of_values_connected` > 0)
  - Deterministic sorting: `concept_name` ascending + `guid` ascending
  - Pagination is validated

- **Create Concept**
  - Requires: `canonical_lib`, `concept_name`
  - Validates UUID formats for lookup-table fields
  - Sanitizes strings
  - Enforces name uniqueness:
    - API path: automatically makes names unique on import by auto-renaming (`make_unique_concept_name`)
    - Web UI path: rejects duplicates for manual entry (`NameUniquenessService.validate_name_for_manual_entry`)
  - Sets defaults like `status` and version numbers

- **Read one Concept**
  - Returns concept metadata
  - Additionally, when the concept has a ValueSet, the API attempts to **include the ValueSet’s Values** in the response (`valueset_values`) with ordering information.

- **Update Concept**
  - Increments `vers_number`
  - Updates `date_valid`
  - Re-validates UUID shapes for referenced lookup-table rows

- **Delete Concept**
  - Deletes the row (no “soft delete” at this level)

Crucial behavior to understand:

- A Concept may have `response_type` that implies it needs an associated ValueSet (e.g., “single choice”).
- In the web UI routes (`app/routes/concepts.py`) there’s an explicit business rule:
  - If response type name matches common single-choice aliases, the Concept must have a `valueset` selected.

### 3.2 Create and manage Values (ValueCatalog)

Capabilities implemented:

- **List/search Values**
  - API returns all values (without pagination in the current implementation) with optional filtering
  - Ordering by `value_name`

- **Create Value**
  - Requires: `value_name` and `canonical_lib`
  - Validates canonical lib UUID
  - Sanitizes strings
  - Enforces uniqueness:
    - API: can auto-rename on import (`make_unique_value_name`)
    - Web UI: rejects duplicates for manual entry

### 3.3 Create and manage ValueSets

Capabilities implemented:

- **List/search ValueSets** (with pagination)
- **Create ValueSet**
  - Requires: `valueset_name`, `canonical_lib`
  - Validates canonical lib UUID
  - Sanitizes strings
  - Enforces uniqueness:
    - API: can auto-rename on import (`make_unique_valueset_name`)
    - Web UI: rejects duplicates for manual entry

### 3.4 Manage membership: add/remove Values in a ValueSet

Capabilities implemented:

- **Get values in a valueset** (reads `ValueSetValue` + `ValueCatalog`)
- **Add a value to a valueset**
  - Validates UUIDs
  - Prevents duplicates
  - Allows optional `sort_order`
- **Remove a value from a valueset**

This is the mechanism that defines which categorical answer options exist for a concept that references this ValueSet.

### 3.5 Manage membership: add/remove Values for a Concept

There are two ways this exists:

- **API concept values endpoints**: `Concept` → values are accessed “through its valueset”.
  - `GET /concepts/<concept_id>/values`: returns the values in the bound ValueSet
  - `POST /concepts/<concept_id>/values`: adds a value to the concept’s ValueSet (so it is effectively “add to valueset”)
  - `DELETE /concepts/<concept_id>/values/<value_id>`: removes from that ValueSet

- **Web UI concept value management page**: same behavior, but via web forms.

Important constraint:

- If a Concept has no `valueset`, attempts to add a value via concept endpoint return an error (“Concept does not have a valueset”).

---

## 4) PlanDefinition creation: what a “plan definition” means here

### 4.1 Two representations are used simultaneously

In this repo, a PlanDefinition is both:

1) A **FHIR resource** (the official external/serialized representation)
2) A **relational structure** used by the builder for editing, querying, and building CarePlans

Those two are kept in sync by:

- Storing builder state in relational tables (`activities`, `transactions`, `plandefinition_goals`, `plandefinition_activities`)
- Storing a **FHIR JSON** representation in `plan_definitions.fhir_data` (JSONB)
- Optionally also storing raw builder JSON fragments in text fields (`plan_definitions.goal` and `plan_definitions.action`) for backward compatibility

### 4.2 PlanDefinition “content” in builder terms

The PlanDefinition builder models a plan as:

- **Metadata**: title, description, status, type, subject type, versioning and contributors
- **Goals**: high-level desired outcomes, each tied to a Concept and optionally having a numeric/categorical target
- **Activities** (also called “actions” in FHIR terms): a set of scheduled units of work
  - Each activity contains **Transactions** (sub-actions) which are the “things to do/record” and are tied to Concepts

At persistence time, the system creates and maintains:

- `plan_definitions` row: PlanDefinition metadata + raw JSON strings (`goal`, `action`) + `fhir_data`
- `plandefinition_goals` rows: one row per goal for queryability/editing
- `activities` rows: one row per activity
- `transactions` rows: one row per transaction, each tied to one activity
- `plandefinition_activities` rows: junction table to attach activities to a PlanDefinition in a specific order

---

## 5) Step-by-step: creating “concepts”, “values”, “valuesets”, and then “plan definitions”

This is the “definition of concepts”, “definition of values”, “definition of valuesets”, and the ability to create PlanDefinitions described as a pipeline.

### 5.1 Step A — Define supporting lookup values (optional but recommended)

Before you define Concepts, you typically want the following lookup tables populated:

- **Canonical libraries** (`CanonicalLib`): the terminologies you will use
- **Concept types** (`ConceptType`): categories like question/observation/procedure
- **Response types** (`ResponseType`): quantity, categorical choice, slider, etc.
- **Units** (`Unit`): measurement units, used when response type is quantity
- **PlanDefinition types** (`PlanDefType`): the selectable `type` values for PlanDefinitions in the builder UI
- **Intended use** (`IntendedUse`): UI-configurable tags used to annotate transactions for downstream use-cases

These are also the tables that make the UI “feel complete”: dropdowns, consistent names, and constraints.

### 5.2 Step B — Define Values (ValueCatalog)

If you will have any categorical choices, define Values first.

For each Value, the main decisions are:

- **Which canonical library** it belongs to (`canonical_lib`)
- Whether it has a **canonical_refnumber** (a code from that terminology)
- Its human-visible label and explanation

Once created, the Value becomes a reusable token that you can place inside many ValueSets.

### 5.3 Step C — Define ValueSets (ValueSet)

A ValueSet is a named collection of Values that can be reused across concepts.

For each ValueSet, the main decisions are:

- Which canonical library the ValueSet belongs to
- A stable `valueset_name` (uniqueness is enforced)
- Display text and explanation (so non-technical users know what the list represents)

After you create a ValueSet, you still need to populate its membership:

- Add Values into the ValueSet (each membership optionally has `sort_order`)

### 5.4 Step D — Define Concepts (Concept)

When you define a Concept, you are defining “something that can be requested/recorded” in a plan.

Key Concept decisions and how the repo uses them:

- **Canonical library** and optional canonical code (`canonical_refnumber`)
  - If present, it can be emitted as an additional coding in FHIR actions/goals.
- **Response type**
  - Determines whether values are needed and how targets are represented.
  - Web UI enforces that “single choice” implies a selected ValueSet.
- **Unit**
  - Used for numeric responses and for goal targets/transaction metadata.
- **Range**
  - Range constraints exist in the database model; these often feed UI validation or downstream analytics.
- **ValueSet binding**
  - If categorical, Concept typically points to a ValueSet.
  - The builder UI and the `/concepts/<id>` API can load the bound values to populate dropdowns.

Result:

- You now have a “concept vocabulary” that the PlanDefinition builder can reference.

### 5.5 Step E — Create a PlanDefinition (template)

PlanDefinition creation, as implemented, happens primarily through the web UI builder route:

- **Web route**: `/plandefinitions/builder`
  - If creating a new PlanDefinition, user must be logged in and have `read_write` permissions.
  - Concepts are loaded server-side and injected into the template as JSON to avoid client-side authentication issues.

The builder then allows you to define:

- **PlanDefinition metadata**
  - `title`, `description`, `status`, `type`, `subject_type`
  - `name`: if omitted, auto-generated from title (lowercased, non-word stripped, underscores)
  - `version`, `publisher`, `purpose`, `usage`, `copyright`
  - contributor fields: `author`, `editor`, `reviewer`, `endorser`
  - timing/validity: a `validity_duration` can be converted into `effective_period_start/end`

- **Goals**
  - Each goal is tied to a Concept (`concept_guid`, `concept_name`)
  - Each goal has `priority` and a target that can be:
    - **numerical quantity** with an operator (stored as a FHIR extension `goal-operator`)
    - **numerical range** (low/high)
    - **categorical** value (text), with additional GUID lookup for value selection when editing

- **Activities**
  - Each activity has:
    - title, description
    - performer type / subject type
    - timing (“once” vs “repeat” frequency-based schedule)
    - optional notes
  - Each activity includes **Transactions**:
    - each transaction ties to a Concept (`concept_guid`) and carries optional expectations:
      - expected value
      - unit
      - min/max range
      - requirement type (required vs recommended)

#### What happens on PlanDefinition “Save” (create)

When the builder is saved through `/plandefinitions/create` (POST), the backend performs (in broad order):

1) **Validate required metadata**
   - Title must exist
   - Goals and actions JSON must be valid JSON strings

2) **Derive / validate the PlanDefinition name**
   - If name is empty, it’s derived from title
   - Name uniqueness is enforced for manual creation (Rule 3.4) via `NameUniquenessService`

3) **Compute effective period**
   - If a validity duration is provided, compute:
     - `effective_period_start` = today
     - `effective_period_end` = today + days (unit d/wk/mo, month approximated as 30 days)

4) **Create the `plan_definitions` row**
   - Generates `fhir_id` (UUID string)
   - Stores metadata fields
   - Stores `goal` and `action` as JSON strings (backward compatibility fields)

5) **Persist goals relationally**
   - Inserts `plandefinition_goals` rows
   - Extracts the target:
     - numeric quantity + operator
     - range low/high
     - categorical text (with optional value GUID included in the builder payload for edit stability)

6) **Persist activities + transactions relationally**
   - Inserts `activities` rows
   - Creates `plandefinition_activities` junction rows
   - Inserts `transactions` rows for each activity

7) **Generate and store canonical FHIR JSON**
   - Calls `FHIRService.create_fhir_plandefinition(plandef)`
   - Stores result into `plan_definitions.fhir_data` (JSONB)

This is what makes PlanDefinitions later retrievable as valid-ish FHIR PlanDefinition resources from the API.

#### What happens on PlanDefinition “Save” (edit)

When editing (`/plandefinitions/<id>/edit` POST), the backend:

- Updates PlanDefinition metadata
- Re-parses goals/actions JSON
- Deletes and recreates:
  - `PlanDefinitionActivity` links
  - `PlanDefinitionGoal` rows
- Updates or creates Activities by GUID (action.id), and deletes Activities removed from the plan if they’re not referenced elsewhere
- Replaces Transactions for each Activity (delete old, insert new)
- Regenerates `fhir_data` using the same serializer

---

## 6) How FHIR PlanDefinition serialization works (in this repo)

The serializer `FHIRService.create_fhir_plandefinition(plandef)` builds an ordered JSON object with:

- `meta.versionId` and `meta.lastUpdated`
- `resourceType = "PlanDefinition"`
- `id = plandef.fhir_id`
- `identifier` using system `https://pdhc.se/plan-definitions` and value `plandef.name or plandef.fhir_id`
- `url` as `https://pdhc.se/PlanDefinition/<fhir_id>`
- `version` from `plandef.version` (default `"1.0.0"`)
- `name`, `title`, `status`
- `type`:
  - if `plandef.type` exists it uses that string as the code under HL7’s plan-definition-type code system
  - otherwise it defaults to `clinical-protocol`
- `subjectCodeableConcept` derived from `plandef.subject_type` (default `Patient`)
- Optional descriptive fields: `publisher`, `description`, `purpose`, `usage`, `copyright`
- Optional date fields: `approvalDate`, `lastReviewDate`, `effectivePeriod`
- Optional contributors: topic, author, editor, reviewer, endorser
- `relatedArtifact` (parsed if stored as JSON string)
- `library` (single string stored as array)
- Finally: `action` and `goal` are included by parsing the stored `plandef.action` and `plandef.goal` JSON.

Important practical implication:

- The **FHIR API** endpoints will often return the stored `fhir_data` (if present), enriched with identifier/url if missing.
- The `$expand` endpoint forces regeneration to ensure “full expansion” (and stable inclusion of nested structure).

---

## 7) Backend endpoints needed to provide these services (comprehensive wrap-up)

This section is a “what endpoints are needed” checklist, aligned to what this repo already implements (and where there are notable gaps).

### 7.1 Authentication (prerequisite for most write operations)

- `POST /api/v1/auth/login`: obtain JWT (access + refresh tokens).
- `POST /api/v1/auth/logout`: client discards token.
- `GET /api/v1/auth/me`: current user info.
- `POST /api/v1/auth/refresh`: refresh access token using refresh token.

Rate limiting: 10 requests/minute on login, 200 requests/minute on all other endpoints.

Practical requirement:

- Terminology CRUD and PlanDefinition creation are protected by role checks (`read_write`).
- Read endpoints are public (no auth required).
- Local dev runs with `AUTH_DISABLED=true` — all auth bypassed.

### 7.2 Terminology / lookup management endpoints

These endpoints provide the “definition of values” and “definition of valuesets”, plus supporting lookup tables.

Canonical libraries:

- `GET /api/v1/canonical-libs`
- `POST /api/v1/canonical-libs`
- (plus update/delete endpoints if you need full CRUD parity; the API file follows a standard pattern)

Concept types:

- `GET /api/v1/concept-types`
- `POST /api/v1/concept-types`

Response types:

- `GET /api/v1/response-types`
- `POST /api/v1/response-types`

Units:

- `GET /api/v1/units` (optional auth in this repo)
- `POST /api/v1/units`

PlanDefinition types:

- `GET /api/v1/plandef-types?all=true` (used by builder)

Values catalog:

- `GET /api/v1/values` (or `/api/v1/values_catalog` in docs; verify which one is wired in routing)
- `POST /api/v1/values`

ValueSets:

- `GET /api/v1/valuesets`
- `POST /api/v1/valuesets`

ValueSet membership:

- `GET /api/v1/valuesets/<valueset_id>/values`
- `POST /api/v1/valuesets/<valueset_id>/values`
- `DELETE /api/v1/valuesets/<valueset_id>/values/<value_id>`

### 7.3 Concept management endpoints

Core Concept CRUD:

- `GET /api/v1/concepts`
- `POST /api/v1/concepts`
- `GET /api/v1/concepts/<concept_id>`
- `PUT /api/v1/concepts/<concept_id>`
- `DELETE /api/v1/concepts/<concept_id>`

Concept ↔ values (through Concept’s ValueSet):

- `GET /api/v1/concepts/<concept_id>/values`
- `POST /api/v1/concepts/<concept_id>/values` (adds a value to the bound ValueSet)
- `DELETE /api/v1/concepts/<concept_id>/values/<value_id>`

These are the endpoints the PlanDefinition builder relies on to:

- load the list of concepts
- load categorical values for concepts (dropdown options)

### 7.4 PlanDefinition endpoints (FHIR-facing)

Read/search:

- `GET /api/v1/PlanDefinition` (FHIR searchset bundle, supports `status`, `title`, `_count`, `_offset`)
- `GET /api/v1/PlanDefinition/<id>` (returns stored `fhir_data` or regenerates)

Expand:

- `GET /api/v1/PlanDefinition/<id>/$expand` (forces regeneration intended to include full nested structure)

Create via FHIR:

- `POST /api/v1/PlanDefinition` currently returns “not supported” (501) and instructs to use the builder UI or the CRUD API.

Create via CRUD API (full support):

- `POST /api/v1/plandefinitions` — accepts JSON with title, goals, actions (with transactions). Persists all relational rows and generates FHIR JSON automatically.
- `PUT /api/v1/plandefinitions/<guid>` — update with partial or full data.
- `DELETE /api/v1/plandefinitions/<guid>` — cascade delete with orphan cleanup.
- `GET /api/v1/plandefinitions` — paginated list with status/title filtering.
- `GET /api/v1/plandefinitions/<guid>` — full detail including goals, activities, transactions.

### 7.5 PlanDefinition endpoints (Web UI routes that actually create/edit)

These are not pure API endpoints but they are currently the only “fully implemented creation surface”:

- `GET /plandefinitions` (list UI)
- `GET /plandefinitions/builder` (builder UI; supports edit via `?plandef_id=<fhir_id>`)
- `POST /plandefinitions/create` (create PlanDefinition from builder payload)
- `GET /plandefinitions/<id>` (view UI)
- `POST /plandefinitions/<id>/edit` (update from builder payload)
- `POST /plandefinitions/<id>/delete`
- `GET /plandefinitions/<id>/export` (download JSON)

### 7.6 Minimum endpoint set for the full “early components → plan definition” workflow

If you think of the complete workflow as a service offered to clients (UI or API), the minimum set is:

- **Auth**: login/logout, role enforcement
- **Lookup CRUD**: canonical libs, response types, units, concept types, plandef types
- **Values + ValueSets CRUD** + binding endpoints
- **Concept CRUD** + concept values endpoints
- **FHIR PlanDefinition read/search/expand**
- **PlanDefinition creation surface**:
  - either the existing **web builder** endpoints, or
  - a future `POST /api/v1/PlanDefinition` implementation

---

## 8) Practical “mental model” summary

- **Concepts** are *what to measure/ask/record*.
- **Values** are *individual categorical options*.
- **ValueSets** are *named collections of Values*, reusable across Concepts.
- A **Concept can bind to a ValueSet** to define allowed categorical answers.
- A **PlanDefinition** is a *template* containing:
  - goals tied to Concepts (with numeric/categorical targets)
  - activities containing transactions tied to Concepts (what should be done/recorded, when, by whom)
- The system persists PlanDefinitions as both:
  - relational data for editing/querying
  - FHIR JSON (`fhir_data`) for interoperability and downstream transaction engines

---

## 9) FHIR R5 terminology profile (added 2026-06-22)

The terminology substrate is also published as a conformant **FHIR R5
terminology API profile** so generic FHIR clients can interoperate
without bespoke code:

- **`ValueSet`** — the existing builder ValueSets are projected as
  FHIR ValueSet resources. Read, search-by-canonical-url, `$expand`
  (returns `expansion.contains[]`), and scoped `$validate-code`.
- **`CodeSystem`** — every local Concept appears in a single
  `CodeSystem` resource (`id = plan-pdhc-local`) with the Concept GUID
  as `concept[].code` (so external systems join against an immutable
  identifier — see [ADR D1](plan_pdhc_fhir_terminology_profile_DECISIONS.md)).
  `$lookup` works for local concepts; for external authorities
  (LOINC/SNOMED/ICD-10 via registered CanonicalLibs) `$lookup` delegates
  to the existing TTL-cached `TermbankClient` and returns
  termbank.pdhc's response transparently.
- **`ConceptMap`** — a single platform ConceptMap
  (`id = plan-pdhc-canonical-bindings`) projects every Concept's
  `canonical_lib + canonical_refnumber` binding. `$translate` is
  bidirectional: local Concept GUID → canonical code, or canonical →
  local.

Two regression contracts are explicitly preserved:

1. The legacy `/api/v1/lookup/valuesets/*` CRUD JSON is byte-identical
   to before (used by the builder UI).
2. The cdr.pdhc `$validate-code` "is this canonical adopted anywhere?"
   shim (called from `cdr.pdhc/cdr_app/app/services/plan_client.py`)
   keeps its exact pre-2026-06-22 request/response shape. The same
   route now ALSO answers FHIR-conformant scoped questions when a
   `url`/`valueSet` identifier is passed; the original global form
   is unchanged.

For the full spec and decision record:
- [`plan_pdhc_fhir_terminology_profile_instruction.md`](plan_pdhc_fhir_terminology_profile_instruction.md)
- [`plan_pdhc_fhir_terminology_profile_DECISIONS.md`](plan_pdhc_fhir_terminology_profile_DECISIONS.md)

