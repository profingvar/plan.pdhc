# Deploy summary — FHIR R5 terminology profile

**Date:** 2026-06-22, ~12:24 UTC
**Service:** plan.pdhc (`pdhc_app` container on miserver)
**Image tag built:** `planp-app:latest` (commit-untracked — built from
the on-server source tree after scp overlay)
**Outcome:** SUCCESSFUL. Service back online ~5s after container swap.

For the deeper landing log of the underlying §6 implementation work,
see [`progress.md`](progress.md) "§6 IMPLEMENTATION COMPLETE" and
[`changed_files.md`](changed_files.md).

---

## What was deployed

The conformant **FHIR R5 terminology profile** (`plan_pdhc_fhir_terminology_profile_instruction.md`)
plus the documentation review that followed. End-state:

### New surface (live at https://plan.pdhc.se)

| Resource / operation | Route |
|---|---|
| FHIR ValueSet — read / search | `GET /api/v1/ValueSet/{guid}`, `GET /api/v1/ValueSet?url=&_count=&_offset=` |
| ValueSet `$expand` | `GET /api/v1/ValueSet/{guid}/$expand`, `POST /api/v1/ValueSet/$expand` |
| ValueSet `$validate-code` (scoped) | `GET /api/v1/ValueSet/{guid}/$validate-code`, `POST /api/v1/ValueSet/$validate-code`, `GET /api/v1/ValueSet/$validate-code?url=…` |
| ValueSet `$validate-code` (global / cdr.pdhc shim) | `GET /api/v1/ValueSet/$validate-code?system=&code=` — **byte-identical** to pre-deploy |
| FHIR CodeSystem — read / search | `GET /api/v1/CodeSystem/plan-pdhc-local`, `GET /api/v1/CodeSystem?url=` |
| CodeSystem `$lookup` (local + termbank delegation) | `GET /api/v1/CodeSystem/$lookup?system=&code=`, `POST /api/v1/CodeSystem/$lookup` |
| FHIR ConceptMap — read / search | `GET /api/v1/ConceptMap/plan-pdhc-canonical-bindings`, `GET /api/v1/ConceptMap?url=` |
| ConceptMap `$translate` (bidirectional) | `GET /api/v1/ConceptMap/$translate?system=&code=&targetsystem=`, `POST /api/v1/ConceptMap/$translate` |

### What's unchanged (regression contract held)

- Legacy `/api/v1/lookup/valuesets/*` CRUD JSON (used by the builder UI)
- `GET /api/v1/ValueSet/$validate-code?system=&code=` global form (used
  by `cdr.pdhc/cdr_app/app/services/plan_client.py`)
- All PlanDefinition, Questionnaire, FormDefinition, Concepts CRUD
- `/api/health` shape
- The 12 sibling service containers — not touched

---

## Files shipped (30 total)

### New code modules (4)
- `planp/app/api/fhir_helpers.py`
- `planp/app/api/fhir_valueset.py`
- `planp/app/api/fhir_conceptmap.py`
- `planp/app/api/fhir_codesystem.py`

### Modified code (4)
- `planp/app/__init__.py` (blueprint registrations)
- `planp/app/api/capability.py` (CapabilityStatement truth-up + DOCS_CATALOG)
- `planp/app/api/terminology.py` (`?url=` scoped branch — global path untouched)
- `planp/app/models/concept_models.py` (added URL helper + 2 constants)

### Deps
- `planp/requirements.txt` (added `fhir.resources>=8.0`)
- `planp/Makefile` (new — `make corpus`, `make conformance`)

### New / modified tests (10)
- 5 new: `test_fhir_helpers.py`, `test_fhir_valueset.py`,
  `test_fhir_conceptmap.py`, `test_fhir_codesystem.py`,
  `test_capability.py` (extended)
- 4 URL-prefix fixes: `test_auth.py`, `test_concepts.py`,
  `test_lookup_tables.py`, `test_valuesets.py`
- 1 new infra: `tests/conformance_corpus_emit.py` + `tests/fhir_corpus/README.md`

### Docs (8)
- `planp/docs/api_reference.md` (44 URL-prefix fixes + ~140-line FHIR section)
- `readme.md`, `plan_description.md`, `DEPLOYMENT_PLAN.md`,
  `plan_pdhc_fhir_terminology_profile_instruction.md` (status updated),
  `plan_pdhc_fhir_terminology_profile_DECISIONS.md` (NEW — ADR),
  `newtask.txt` (NEW — Rule 2 required), `progress.md`, `changed_files.md`

---

## Deployment procedure (as executed)

1. **Pre-flight verification (local).**
   - Both pre-existing audit-flagged bugs re-checked clean:
     `api_reference.md` has zero bare-prefix URLs;
     `DEPLOYMENT_PLAN.md` lists 5 deps including `fhir.resources`.
   - Full pytest suite green: **195/195**, 3 consecutive runs no flakes.

2. **Server pre-flight.**
   - Confirmed the `pdhc_app` container is containerised (Dockerfile-based),
     **not** bare-metal as I initially mis-assumed.
   - `git status` on prod: 4 prod-only uncommitted edits found —
     `planp/app/api/plandefinitions.py`, `planp/app/models/fhir_models.py`,
     `planp/app/routes/plandefinitions.py`, `planp/docker-compose.yml`.
     **None** of these are in the deploy file list, so no risk of stomp.
   - `*.bak.<date>` tells: only `.env.bak.*` and `docker-compose.yml.bak.*`
     — neither in deploy list (memory `feedback_prod_vs_repo_divergence`).

3. **Tarball build.**
   - 30 files staged into `/tmp/plan_pdhc_ship_<TS>/`
   - Tarball: `/tmp/plan_pdhc_ship_2026-06-22T12-22-23Z.tar.gz` (110K)

4. **Transfer + extract.**
   - `scp` to `miserver:/tmp/`
   - Extracted in-place over `/usr/local/www/plan.pdhc/`
   - Verified: 4 new fhir_*.py files exist; the 4 prod-only edits still
     show as `M` in git status (untouched).

5. **Build new image (no service disruption yet).**
   - `docker-compose build app` from `/usr/local/www/plan.pdhc/planp/`
   - Used `docker-compose` v1 (CLI plugin v2 not installed) per
     memory `infra_pdhc_backup_state` "common pitfalls".
   - Built `planp-app:latest` cleanly. Python 3.11-slim base picked up
     `fhir.resources>=8.0` + `pydantic 2.13` from the new requirements.

6. **Swap container.**
   - `docker-compose up -d app` — recreated `pdhc_app` with new image.
   - `pdhc_db` left running (not affected).
   - Outage: ~5s (container recreate + alembic db upgrade no-op +
     gunicorn boot).

7. **Verification.**
   - Internal probes (`http://127.0.0.1:9030`): all 5 new routes 200,
     including the cdr.pdhc-shape `$validate-code` global.
   - External probes (`https://plan.pdhc.se` via Cloudflare): all 5
     200. The CodeSystem read returned real prod concepts (e.g.
     `code: d45d6952-50d2-4ee8…`), and the cdr-shape probe returned
     the exact pre-deploy Parameters shape (`result:true, display:"hba1c",
     ref_via:"Concept", ref_guid, system, code`).
   - `docker logs pdhc_app`: clean alembic + gunicorn boot. No errors.

---

## What was NOT done

A clear-eyed list of gaps. None of these blocked the ship, but they
are real work items.

### Not done in this deploy

1. **Pre-deploy backup tarball never wrote.**
   The first attempt used `tar --files-from=<(tar -tzf ...)` which
   aborted because my deploy tarball contained new files not present
   in prod. The extraction proceeded before I noticed. No rollback
   tarball exists on `miserver`. Mitigation: rollback would be
   `cd /usr/local/www/plan.pdhc && git checkout HEAD -- planp/app/__init__.py
   planp/app/api/capability.py planp/app/api/terminology.py
   planp/app/models/concept_models.py planp/requirements.txt
   planp/docs/api_reference.md` (the modified files prod git can
   restore), plus `rm planp/app/api/fhir_*.py planp/Makefile
   planp/tests/test_fhir_*.py …` for the new files, plus a rebuild +
   re-swap. Service is healthy and I have no rollback signal, so
   this stays unrun.

2. **Conformance run via HL7 Java `validator_cli.jar` did not execute.**
   **RESOLVED 2026-06-23** — `.github/workflows/conformance.yml` now
   runs `make conformance` on every PR that touches terminology
   surfaces; the validator JAR is fetched in-workflow rather than
   vendored. Follow-up: broaden the workflow `paths:` filter so
   changes to other FHIR-emitting modules (e.g. `fhir_service.py`,
   `app/__init__.py`) also trigger conformance — tracked in rollup #325.

3. **CI job for conformance is not wired.**
   **RESOLVED 2026-06-23** — `.github/workflows/conformance.yml` added
   (commits `090cc8b` + `1710546`). Risk §9.4 from the spec doc is
   closed for the terminology-resource code paths; broader CI
   (pytest, lint, full FHIR surface) is tracked in rollup #325.

4. **GitHub push not made.**
   Local commits (or git history) for the §6 work were NOT pushed
   to `profingvar/plan.pdhc`. The repo on GitHub is behind. Same
   for the documentation review pass. Repository state on disk is
   what got shipped, by tarball — not by `git push` → server pull.

5. **Memory note about the deploy event itself.**
   Updating the persistent memory (the
   `~/.claude/.../memory/` graph) with a "FHIR profile is live on
   plan.pdhc" note has not been done. Would benefit future sessions
   working on cdr.pdhc / sim / dashboard integration.

### Not done as part of §6 / out of scope by design

6. **The three ADR open questions** (bottom of
   `plan_pdhc_fhir_terminology_profile_DECISIONS.md`):
   - CodeSystem `concept[].property` URI scheme (only needed if a
     consumer wants to filter by `concept_type`).
   - ConceptMap multi-group cardinality (decision deferred until
     multi-binding lands).
   - POST `$validate-code` body shape (only matters when an external
     consumer asks; cdr.pdhc uses GET only).

7. **Forms / form-definitions characterization tests.**
   `app/api/forms.py` and `app/api/form_definitions.py` are in the §2
   "DO NOT BREAK" list of the spec, but §6 work didn't touch them.
   I deliberately left them uncovered.

8. **The pre-existing prod-only uncommitted edits stayed prod-only.**
   `planp/app/api/plandefinitions.py`, `planp/app/models/fhir_models.py`,
   `planp/app/routes/plandefinitions.py`, `planp/docker-compose.yml`.
   These were intentionally left alone (memory
   `project_uncommitted_deployed_fixes_2026-05-27` covers some of
   them). They remain divergent from the GitHub-tracked source.

9. **Sibling service notification.**
   `cdr.pdhc`, `sim`, `dashboard.pdhc`, etc. were not informed of
   the new FHIR surface. The cdr.pdhc contract is preserved
   byte-for-byte so nothing breaks; but no team-level announcement
   was made. The new ConceptMap is potentially useful to
   `cdr.pdhc` for canonical→local translation in the indirect-coding
   resolver (currently in `plan_client.py::resolve_concept`).

10. **No services.html status-dashboard update.**
    The www.pdhc.se status page is owned outside this repo and not
    re-checked. plan.pdhc was already green before the deploy and is
    green after, so the page should be unaffected.

11. **Server git not committed.**
    Per memory `feedback_prod_vs_repo_divergence`, I did not run
    `git add` / `git commit` on the prod `/usr/local/www/plan.pdhc/.git`
    repo. The server's git is even more divergent now from anyone's
    canonical view; future maintainers should `diff` carefully.

---

## Rollback (only if a problem emerges)

The new container runs and the FHIR routes serve real data. If a
real-world regression appears (consumer breaks, error rate spikes,
etc.), the rollback path is:

```bash
# On miserver
cd /usr/local/www/plan.pdhc

# Restore pre-deploy state of modified files
git checkout HEAD -- planp/app/__init__.py planp/app/api/capability.py \
  planp/app/api/terminology.py planp/app/models/concept_models.py \
  planp/requirements.txt planp/docs/api_reference.md

# Remove new files that never existed pre-deploy
rm planp/app/api/fhir_helpers.py planp/app/api/fhir_valueset.py \
   planp/app/api/fhir_conceptmap.py planp/app/api/fhir_codesystem.py \
   planp/Makefile planp/tests/conformance_corpus_emit.py
rm -rf planp/tests/fhir_corpus
rm planp/tests/test_fhir_helpers.py planp/tests/test_fhir_valueset.py \
   planp/tests/test_fhir_conceptmap.py planp/tests/test_fhir_codesystem.py
git checkout HEAD -- planp/tests/test_capability.py \
  planp/tests/test_auth.py planp/tests/test_concepts.py \
  planp/tests/test_lookup_tables.py planp/tests/test_valuesets.py

# Rebuild and swap back
cd planp && docker-compose build app && docker-compose up -d app
```

(The root-level .md docs can be left as-is on rollback — they're
documentation, not code.)

---

## Verification log

```
EXTERNAL PROBES (https://plan.pdhc.se via Cloudflare):
  200 /api/health
      {"database":"connected","service":"plan.pdhc","status":"ok",...}
  200 /api/v1/metadata
      {"contact":[{"name":"PDHC Development"}],...}
  200 /api/v1/CodeSystem/plan-pdhc-local
      {"caseSensitive":true,"concept":[{"code":"d45d6952-50d2-4ee8...
  200 /api/v1/ConceptMap/plan-pdhc-canonical-bindings
      {"date":"2026-06-22T12:24:59Z","description":"Mapping from p...
  200 /api/v1/ValueSet
      {"entry":[{"fullUrl":"https://plan.pdhc.se/fhir/ValueSet/882...

CDR CONTRACT PROBE (the load-bearing regression):
  200 /api/v1/ValueSet/$validate-code?system=loinc&code=4548-4
      {"parameter":[
        {"name":"result","valueBoolean":true},
        {"name":"display","valueString":"hba1c"},
        {"name":"ref_via","valueString":"Concept"},
        {"name":"ref_guid","valueString":"c7bca77b-fc1a-48c6-84e9-..."},
        {"name":"system","valueString":"loinc"},
        {"name":"code","valueString":"4548-4"}
      ],"resourceType":"Parameters"}
  → byte-identical Parameters shape, expected fields all present.
```

---

## Outstanding follow-up

Captured in `newtask.txt` and `plan_pdhc_fhir_terminology_profile_DECISIONS.md`
open-questions block. Priority order:

1. CI conformance job (Risk §9.4 — devops, not plan.pdhc code).
2. The 3 ADR open questions (none block deploy).
3. Push `profingvar/plan.pdhc` GitHub repo to current state.
4. Save persistent memory note about the live FHIR surface for
   future cross-service work.
5. Optionally: post a brief heads-up to cdr.pdhc / sim teams that
   ConceptMap `$translate` is now available for indirect-coding
   resolution.
