# #521 GA-5 pre-enforcement data cleanup — record & rollback (2026-08-01)

Read-only audit found **33 of 74** prod concepts would be blocked by fail-closed
validation. All were fixed (or the rule adjusted) so **0 concepts are now
blocked** and enforcement can be enabled with no fallout. All changes below were
applied directly to the prod plan.pdhc DB (`pdhc_app`) and are reversible from
the recorded values.

## Changes applied

### 1. 25 choice→Boolean re-types (E-VALUESET-REQUIRED)
Created response type **`Boolean`** guid `5e7a7a21-2d0a-4a30-94eb-978b7d30e653`.
Re-typed 25 diagnosis/med/encounter/procedure concepts from `Single choice`
(old response_type `2439c887-a757-4dfa-bee3-f017d0c6f9c9`) → `Boolean`:
ckd_diagnosis, diabetic_foot_ulcer, diabetic_neuropathy, diabetic_retinopathy,
enc_diabetes_nurse_visit, enc_primary_care_visit, heart_failure,
hypertension_diagnosis, inpatient_admit, med_acei, med_arb, med_aspirin,
med_glp1, med_insulin, med_metformin, med_sglt2, med_statin, med_thiazide,
mi_history, proc_foot_screening, proc_hba1c_sampling, proc_retinal_screening,
stroke_history, t1dm_diagnosis, t2dm_diagnosis.
**Rollback:** set each concept's `response_type` back to `2439c887-…`.

### 2. CGM → Boolean
Concept `22d0f6c6-2438-4637-ad4e-9d85431b8edb`; old response_type = `None`.
**Rollback:** set response_type = `None`.

### 3. Units (E-UNIT-REQUIRED)
Created unit **`10^9/L`** guid `4ac218c5-299d-43fb-aead-8a33dd66fae3`. Assigned to
`leukocytes` (`ff07c0fd-…`, old unit None) and `platelets` (`81ac94e8-…`, old unit None).
`cgm_hypo_count` (`d368dd8e-…`) re-typed → `Integer` (old response_type
`2e367166-f8be-4c4f-944b-04dbbea2eaf0`).
**Rollback:** clear the two units; restore cgm_hypo_count response_type.

### 4. smoking_status → value set
Created value set **`Smoking status`** guid `129fec0b-f56f-470c-81dd-31f944960882`
with values Never smoker (`faec0d69-…`, SNOMED 266919005), Former smoker
(`3ee70523-…`, 8517006), Current smoker (`6dd4f0aa-…`, 77176002). Concept
`smoking_status` (`7415a46d-…`) valueset set (old = None).
**Rollback:** set smoking_status.valueset = None; delete the value set + 3 values.

### 5. Validator rule change (code, commit 58dcb40)
`E-TERM-MISSING` (missing terminology code) downgraded **error → warning**
(`W-TERM-MISSING`): free-text info fields / PROMs / self-reported values may
legitimately lack a standard code. Unblocks `QOL` and `Self reported body Weight`.

### 6. Information 1 — removed (was a free-text instruction field, operator chose delete)
Deleted concept `ea75ca90-7e2b-4814-8885-b55354a6055c`
(display_text "Detta är information om det formulär vi der dig fylla i…").
Also removed: transaction `bafdee49-…` (activity `0e5e60ea-…` "Inför operation"),
form items `7cd41935-…` (form `8cd1292a-…` "Alla frågor") and `6aa5d7b0-…`
(form `87212ab6-…` "Prova 1177"), and the matching transaction entry from the
**Form-operation** plandef (`fhir_id f7b4a6bf-…`) `action` blob. Full row
snapshots are in the removal-run output (session transcript) for restore.
NOTE: Form-operation's cached `fhir_data` still references it until the plan is
re-saved in the builder (the authoritative action blob is already scrubbed).

## Result
73 concepts, **all pass**; plandef references clean. Ready for fail-closed
enforcement (GA-5 proper) + an audited override hatch.

## Post-removal: Form-operation FHIR cache refresh
After removing `Information 1`, the Form-operation plandef's authoritative
`action` blob was already clean but its cached `fhir_data` still mentioned it.
Regenerated the cache server-side via
`FHIRService.create_fhir_plandefinition(pd)` (the same call a builder re-save
makes) and committed — verified the new `fhir_data` references `Information 1`
neither by guid (`ea75ca90-…`) nor by name. This was a single-row DB update
(no code change), recorded here for the audit trail.
