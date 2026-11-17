# Concept catalogue bulk import (ticket #134)

This is the endpoint a new provider hits when onboarding under the
provider integration guide (vers2 Phase 2–3): submit a single file of
concepts to plan.pdhc and get back an accepted/rejected report.

Three entry points share the same import logic in
`app/services/concept_importer.py`:

- **HTTP**: `POST /api/v1/concepts/import` (multipart upload, admin only)
- **CLI**:  `flask import-concepts <path>`
- **Web UI**: `/concepts/import` (SU admin only)

## File format

`.xlsx` or `.csv`, UTF-8, one concept per row. The first row is the
header. Column order does not matter.

| Column          | Required | Notes                                                                 |
|-----------------|----------|-----------------------------------------------------------------------|
| `concept_name`  | yes      | Globally unique. lowercase letters, digits, and hyphens only.         |
| `display_text`  | yes      | Free text; UI label.                                                  |
| `canonical_lib` | yes      | Name (`LOINC`, `SNOMED`, `PDHC`, ...) or GUID. Must exist.            |
| `canonical_ref` | yes      | The reference in that library (e.g. LOINC code). Identity field.     |
| `concept_type`  | yes      | Name or GUID. Must exist in `concept_types`.                          |
| `response_type` | yes      | Name or GUID. Must exist in `response_types`.                         |
| `unit`          | yes      | Unit name (`L/min`, `mmHg`, …) or GUID. Empty for unitless concepts.  |
| `range_low`     | no       | Float. Required when `range_high` is set.                             |
| `range_high`    | no       | Float. Must be ≥ `range_low`.                                        |

The unit lives on the **concept**, not the transaction (PDHC information
model — see `[[feedback_unit_lives_on_concept]]`). Provider report
payloads will be resolved against this catalogue's unit.

## Idempotency

Re-uploading the same file is safe: rows are upserted on
`concept_name`. A re-import bumps `vers_number` and updates the
non-identity fields (`display_text`, `concept_type`, `response_type`,
`unit`, `range_low`, `range_high`).

### Identity fields

`canonical_lib` and `canonical_ref` are **append-only** — once a
concept has them set, an import that tries to change them is reported
as a conflict (and the row is rejected) rather than silently
overwriting. To rename a concept's identity you must edit it
individually through the single-concept PUT endpoint, which is
treated as a curatorial action.

## Response shape

The HTTP endpoint and the CLI both return:

```json
{
  "accepted": ["peak-flow-am", "peak-flow-pm"],
  "rejected": [
    {"row": 4, "concept_name": "peak Flow", "reason": "concept_name must be lowercase letters, digits, and hyphens (got 'peak Flow')"}
  ],
  "summary": {
    "n_in": 3,
    "n_accepted": 2,
    "n_rejected": 1,
    "n_created": 2,
    "n_updated": 0,
    "dry_run": false
  },
  "operator": "alice@hospital.se",
  "filename": "medituner_concepts_v1.xlsx",
  "sha256": "8f2a..."
}
```

HTTP status is `200` when every row was accepted, `207 Multi-Status`
when some were rejected, `400` when the file itself failed to parse.

## Dry run

Add `dry_run=true` (form field on the HTTP/UI flow, `--dry-run` on the
CLI) to validate only — the same report is returned but the
transaction is rolled back. Use this when handing a catalogue off to
plan.pdhc for review before committing.

## Categories (#951)

A concept has any number of **categories** (e.g. the guideline its terms came
from). Categories live in `/api/v1/lookup/concept-categories` (read needs a
login; a category name can name a guideline) and are created there, never by an
import.

- `--category NAME[; NAME]` (CLI), form field `category` (API and web page):
  the batch default for every row without its own cell. An unknown one
  **refuses the whole file**.
- optional column `category`: `;`-separated names for that row; it beats the
  batch default. An unknown one **rejects that row** by name; nothing is created.
- imports only ADD categories. Replacing the set is a hand edit
  (`PUT /api/v1/concepts/<guid>` with `categories`, or the edit form).
- `GET /api/v1/concepts?category=NAME|GUID` filters (several, `;`-joined, = any of);
  an unknown category is a 400, not an empty list.

Optional column `concept_explain` is importable too: plan's own explanation,
e.g. the guideline section a term came from.

## Re-import is a no-op (#951 D.3)

A row identical to what plan stores is counted `n_unchanged` and bumps no
`vers_number`. So export -> re-import changes nothing (tested).

## Export (#951)

`GET /api/v1/concepts/export.xlsx` (role `read_only`) and
`flask export-concepts out.xlsx [--category X]` write the catalogue in this
format: template column order, lookups by name, a local concept with a blank
`canonical_lib`, categories `; `-joined, review columns blank. Takes the list's
filters. Only plan's own `concept_display_text` is written, never SNOMED text.

## Import record (#951)

Every real (non-dry) run is stored as an immutable `concept_imports` row:
operator, filename, sha256, entry point (cli/api/web), batch categories and the
counts. A concept CREATED by an import carries its `import_guid` (an update does
not move it); each category link carries the import that added it.
`GET /api/v1/concept-imports` and `/<guid>` (role `read_only`; the latter lists the
concepts created and links added).

## Audit

Every import run is logged via `app.logger` with operator, filename,
SHA-256, and the rolled-up counts:

```
concept_import operator=alice@hospital.se filename=medituner_v1.xlsx
sha256=8f2a... n_in=42 n_accepted=40 n_rejected=2 n_created=18
n_updated=22 dry_run=False
```

Per-row rejections are returned in the response body, not the log,
because the file SHA-256 is enough to reproduce them deterministically
from the saved input.

## CLI

```
flask import-concepts /path/to/file.xlsx [--dry-run] [--json-out] [--operator <id>] [--category <name>[; <name>]]
flask export-concepts /path/to/out.xlsx [--category <name|guid>]
```

Exit code `0` on a clean run, `1` when any row was rejected, `2` on
parse failure.

## Permission

`requires_role('admin')` — SU admin only. This is bulk plan-catalogue
curation, not provider-facing.
