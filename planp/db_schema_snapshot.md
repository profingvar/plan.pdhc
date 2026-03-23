# PDHC PlanDef Builder — Database Schema Snapshot

**Date:** 2026-03-20
**Database:** pdhc_planp (PostgreSQL 16)
**Tables:** 17

---

## Core Resources

### concepts

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `59013287-07a0-458d-adf4-57f09b93e899` |
| canonical_lib | string(36) FK | | `84ec5c0e-50bd-408e-80a2-3d7a46842742` |
| canonical_refnumber | string(255) | *(null)* | |
| concept_name | string(255) | pain_level | |
| concept_display_text | string(500) | Pain Level | |
| concept_explain | text | *(null)* | |
| status | string(20) | draft | |
| concept_type | string(36) FK | *(null)* | |
| response_type | string(36) FK | *(null)* | |
| unit | string(36) FK | *(null)* | |
| range_low | float | *(null)* | |
| range_high | float | *(null)* | |
| anchor_low_text | string(255) | *(null)* | |
| anchor_high_text | string(255) | *(null)* | |
| valueset | string(36) FK | *(null)* | |
| no_of_values_connected | integer | 0 | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 13:14:37 | |
| date_valid | datetime | 2026-03-19 13:14:37 | |

### values_catalog

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `0cbbd99f-d4d5-41db-b9d8-4fd7d6beee16` |
| canonical_lib | string(36) FK | | `84ec5c0e-50bd-408e-80a2-3d7a46842742` |
| canonical_refnumber | string(255) | *(null)* | |
| value_name | string(255) | Mild | |
| value_display_text | string(500) | *(null)* | |
| value_explanation | text | *(null)* | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 13:14:37 | |
| date_valid | datetime | 2026-03-19 13:14:37 | |

### valuesets

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `a8902e0e-9377-420a-a099-0833e1e144cd` |
| canonical_lib | string(36) FK | | `84ec5c0e-50bd-408e-80a2-3d7a46842742` |
| canonical_refnumber | string(255) | *(null)* | |
| valueset_name | string(255) | Severity | |
| valueset_display_text | string(500) | *(null)* | |
| valueset_explanation | text | *(null)* | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 13:14:37 | |
| date_valid | datetime | 2026-03-19 13:14:37 | |

### valueset_values

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | *(empty)* | |
| valueset_guid | string(36) FK | | — |
| value_guid | string(36) FK | | — |
| sort_order | integer | | |

> No membership rows yet.

---

## PlanDefinition Resources

### plan_definitions

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `8b7ccde6-bed9-4446-ac0b-403716bfd69e` |
| fhir_id | string(36) | | `f2dd13b0-299e-4fdb-bbd2-7da370aadebe` |
| name | string(255) | test_blood_pressure_plan | |
| title | string(500) | Test Blood Pressure Plan | |
| description | text | A test plan | |
| status | string(20) | draft | |
| type | string(100) | *(null)* | |
| version | string(50) | 1.0.0 | |
| subject_type | string(100) | Patient | |
| publisher | string(255) | *(null)* | |
| purpose | text | *(null)* | |
| usage | text | *(null)* | |
| copyright | text | *(null)* | |
| author | string(500) | *(null)* | |
| editor | string(500) | *(null)* | |
| reviewer | string(500) | *(null)* | |
| endorser | string(500) | *(null)* | |
| approval_date | date | *(null)* | |
| last_review_date | date | *(null)* | |
| effective_period_start | date | *(null)* | |
| effective_period_end | date | *(null)* | |
| validity_duration | string(50) | *(null)* | |
| related_artifact | text | *(null)* | |
| library | string(500) | *(null)* | |
| goal | text (JSON) | `[{"concept_name": "Systolic BP", ...}]` | |
| action | text (JSON) | `[{"title": "Measure BP", ...}]` | |
| fhir_data | json | *(FHIR R5 PlanDefinition resource)* | |
| date_created | datetime | 2026-03-19 20:55:18 | |
| date_updated | datetime | 2026-03-19 20:55:18 | |

### plandefinition_goals

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `a0dc4866-882e-4cd3-959a-27b626e3e0a8` |
| plandefinition_guid | string(36) FK | | `8b7ccde6-bed9-4446-ac0b-403716bfd69e` |
| concept_guid | string(36) FK | *(null)* | |
| concept_name | string(255) | Systolic BP | |
| priority | string(50) | high-priority | |
| target_type | string(50) | *(null)* | |
| target_quantity | float | *(null)* | |
| target_operator | string(10) | *(null)* | |
| target_range_low | float | *(null)* | |
| target_range_high | float | *(null)* | |
| target_categorical_text | string(500) | *(null)* | |
| target_value_guid | string(36) | *(null)* | |
| target_unit | string(100) | *(null)* | |
| sort_order | integer | 0 | |
| date_created | datetime | 2026-03-19 20:55:18 | |

### activities

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `8527db52-4c71-4837-b9bb-d2f5314099e4` |
| title | string(500) | Measure BP | |
| description | text | Take blood pressure reading | |
| performer_type | string(100) | *(null)* | |
| subject_type | string(100) | *(null)* | |
| timing_type | string(20) | *(null)* | |
| timing_frequency | integer | *(null)* | |
| timing_period | float | *(null)* | |
| timing_period_unit | string(10) | *(null)* | |
| timing_duration | float | *(null)* | |
| timing_duration_unit | string(10) | *(null)* | |
| notes | text | *(null)* | |
| date_created | datetime | 2026-03-19 20:55:18 | |
| date_updated | datetime | 2026-03-19 20:55:18 | |

### plandefinition_activities

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| plandefinition_guid | string(36) FK | | `8b7ccde6-bed9-4446-ac0b-403716bfd69e` |
| activity_guid | string(36) FK | | `8527db52-4c71-4837-b9bb-d2f5314099e4` |
| sort_order | integer | 0 | |

### transactions

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `97dc6b75-5c7f-4a2e-87a6-4891d80a9b5b` |
| activity_guid | string(36) FK | | `72feee13-ba6e-4cd3-a16b-14c03aeac25a` |
| concept_guid | string(36) FK | *(null)* | |
| expected_value | string(500) | *(null)* | |
| unit | string(100) | *(null)* | |
| range_min | float | *(null)* | |
| range_max | float | *(null)* | |
| requirement_type | string(50) | *(null)* | |
| sort_order | integer | 0 | |
| date_created | datetime | 2026-03-19 21:22:44 | |

---

## Lookup Tables

### canonical_libs

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 2 | |
| guid | string(36) | | `c7baf862-4b4a-4b7d-bca5-c960f130628b` |
| canonical_lib_name | string(255) | KVÅ | |
| canonical_lib_display_text | string(500) | KVÅ | |
| canonical_lib_url | string(500) | http://www.socialstyelsen.se | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 20:37:10 | |
| date_valid | datetime | 2026-03-19 20:37:10 | |

### concept_types

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 2 | |
| guid | string(36) | | `28b3d058-f646-40c4-a703-7b6e64dcb02d` |
| concept_type_name | string(255) | Diagnos | |
| concept_type_display_text | string(500) | Diagnos | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 20:42:27 | |
| date_valid | datetime | 2026-03-19 20:42:27 | |

### response_types

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `e869b3d0-2f89-4769-a894-ab4015c3f4cb` |
| response_type_name | string(255) | Single Choice | |
| response_type_display_text | string(500) | Envalsfråga | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 20:41:26 | |
| date_valid | datetime | 2026-03-19 20:41:26 | |

### units

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `c358aa14-9266-44ab-90e3-126d8eb1d85f` |
| unit_name | string(255) | Liter | |
| unit_display_text | string(500) | l | |
| author | string(255) | *(null)* | |
| vers_number | integer | 1 | |
| date_created | datetime | 2026-03-19 20:39:23 | |
| date_valid | datetime | 2026-03-19 20:39:23 | |

### plandef_types

> Empty — no rows.

| Column | Type |
|--------|------|
| id | integer |
| guid | string(36) |
| plandef_type_name | string(255) |
| plandef_type_display_text | string(500) |
| author | string(255) |
| vers_number | integer |
| date_created | datetime |
| date_valid | datetime |

### intended_uses

> Empty — no rows.

| Column | Type |
|--------|------|
| id | integer |
| guid | string(36) |
| intended_use_name | string(255) |
| intended_use_display_text | string(500) |
| author | string(255) |
| vers_number | integer |
| date_created | datetime |
| date_valid | datetime |

---

## Auth

### users

| Column | Type | Sample | GUID |
|--------|------|--------|------|
| id | integer | 1 | |
| guid | string(36) | | `fbbb5a49-66c9-4b49-9dd2-f6a2e57a2d92` |
| username | string | admin | |
| email | string | *(null)* | |
| password_hash | string | *(scrypt hash)* | |
| role | string | admin | |
| is_active | boolean | true | |
| date_created | datetime | 2026-03-19 12:57:43 | |
| date_updated | datetime | 2026-03-19 12:57:43 | |

---

## Foreign Key Map

```
concepts.canonical_lib        → canonical_libs.guid
concepts.concept_type         → concept_types.guid
concepts.response_type        → response_types.guid
concepts.unit                 → units.guid
concepts.valueset             → valuesets.guid
values_catalog.canonical_lib  → canonical_libs.guid
valuesets.canonical_lib       → canonical_libs.guid
valueset_values.valueset_guid → valuesets.guid
valueset_values.value_guid    → values_catalog.guid
plandefinition_goals.plandefinition_guid → plan_definitions.guid
plandefinition_goals.concept_guid       → concepts.guid
plandefinition_activities.plandefinition_guid → plan_definitions.guid
plandefinition_activities.activity_guid      → activities.guid
transactions.activity_guid    → activities.guid
transactions.concept_guid     → concepts.guid
```

## GUID Rule

Every entity has a `guid` column (UUID v4, auto-generated). All foreign key references use GUIDs — never integer IDs. All API endpoints address resources by GUID.

---

## Care Plan GUID Resolution Strategy

### GUIDs retained in the plan (minimum set)

| Stored in | Field | Points to | Purpose |
|-----------|-------|-----------|---------|
| plan_definitions | guid, fhir_id | *(self)* | Plan identity |
| plandefinition_goals | concept_guid | concepts | What the goal measures |
| plandefinition_goals | target_value_guid | values_catalog | Categorical target answer |
| plandefinition_goals | target_unit | units | Target unit (if overriding concept default) |
| plandefinition_activities | activity_guid | activities | Activity in the plan |
| transactions | concept_guid | concepts | Data point to collect |

### GUIDs resolved by lookup (NOT stored in plan)

Everything below chains off `concept_guid` — one lookup resolves the full tree:

```
concept_guid
  ├─→ concept.canonical_lib       → canonical_libs  (code system: SNOMED, LOINC, ICD-10...)
  ├─→ concept.concept_type        → concept_types   (observation, procedure, diagnosis...)
  ├─→ concept.response_type       → response_types  (numeric, single choice, text...)
  ├─→ concept.unit                → units           (kg, mmHg, mmol/L...)
  └─→ concept.valueset            → valuesets        (bound answer set)
       └─→ valueset_values        → values_catalog   (each coded answer + sort order)
            └─→ value.canonical_lib → canonical_libs  (value's code system)
```

### Principle

**`concept_guid` is the universal anchor.** A single concept GUID resolves:
terminology binding, code system URL, concept type, response type, unit,
value set, all answer values, and their sort order. None of these need
to be duplicated into the care plan — they are always looked up live,
ensuring the plan stays in sync when terminology is updated.
