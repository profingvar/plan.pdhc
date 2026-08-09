# plan.pdhc/tools — bulk catalogue loader

`load_catalogue.py` — load **concepts + value sets + values** into plan.pdhc
from a single YAML manifest. It drives the plan.pdhc REST API in dependency
order and is idempotent (matches everything by name, reuses what exists, so
re-running the same manifest is a no-op).

## Why it exists

The built-in `.xlsx`/`.csv` concept importer (`flask import-concepts`, ticket
#134) loads **concepts only** — it links to pre-existing lookups and cannot
create value sets or their coded values, nor bind a concept to a value set.
This loader is the superset: one file describes the whole graph and it makes
all the calls (`/lookup/values` → `/lookup/valuesets` → `/concepts`).

It supersedes `sim.pdhc/concepts/load_to_plan.py` (concepts-only, and its
`/api/v1/canonical-libs` paths are now 404 — the real ones are under
`/api/v1/lookup/*`).

## Usage

```bash
export PLAN_LOADER_SERVICE_KEY=...          # = plan.pdhc/.env on miserver
python3 load_catalogue.py catalogue.yaml --dry-run     # resolve + report, no writes
python3 load_catalogue.py catalogue.yaml               # apply
python3 load_catalogue.py catalogue.yaml --update      # also PUT valueset/range onto
                                                        #   pre-existing concepts
python3 load_catalogue.py catalogue.yaml --base http://127.0.0.1:9030   # local
```

Auth is the service-key path (`X-Source-Service: loader.pdhc` +
`X-Service-Key`). `--dry-run` needs no key (GETs only). On apply it writes
`<manifest>.guids.json` next to the manifest with every issued GUID.

Deps: `requests`, `pyyaml`.

## CSV mode (two flat files instead of YAML)

If you'd rather work in spreadsheets, load a **concept CSV** plus an optional
**value-set CSV** directly:

```bash
python3 load_catalogue.py \
    --from-csv concept_import_template.csv,valueset_import_template.csv --dry-run
python3 load_catalogue.py \
    --from-csv concept_import_template.csv,valueset_import_template.csv
```

- **`concept_import_template.csv`** — the flat #134 columns
  (`concept_name, display_text, canonical_lib, canonical_ref, concept_type,
  response_type, unit, range_low, range_high`) **plus an optional `valueset`
  column** naming the value set a single/multiple-choice concept binds to.
  The native `flask import-concepts` importer ignores the extra column, so the
  same file still imports there (concept only, no binding).
- **`valueset_import_template.csv`** — one row per option:
  `valueset_name, valueset_display, value_name, canonical_lib, canonical_ref,
  display_text, sort_order`. Rows are grouped by `valueset_name`; `sort_order`
  orders the options.

Both CSVs are parsed into the same internal structure as the YAML manifest and
run through the identical idempotent pipeline (values → value sets → concepts,
with the concept bound to its value set). Pass only the concept CSV to skip
value sets.

## Manifest format

See `example_catalogue.yaml`. Structure:

- `default_canonical_lib` — used by any item that omits `canonical_lib`.
- `ensure:` *(optional)* — auto-create missing `canonical_libs` /
  `concept_types` / `response_types` / `units` (each `{name, display?}`;
  libs also take `url`).
- `values:` — coded values → `values_catalog`. `{name, ref?, display?,
  explanation?, canonical_lib?}`.
- `valuesets:` — `{name, display?, canonical_lib?, values: [value_name, ...]}`.
  The `values` list order becomes `sort_order` 1..n.
- `concepts:` — `{name, display?, canonical_lib?, canonical_refnumber?,
  concept_type?, response_type?, unit?, range_low?, range_high?, valueset?}`.
  `valueset` references a value set by name (bound via `concepts.valueset`).

Lookup names must match what's in plan.pdhc (or be created via `ensure`).
Check the current sets:

```bash
curl -s https://plan.pdhc.se/api/v1/lookup/canonical-libs
curl -s https://plan.pdhc.se/api/v1/lookup/{concept-types,response-types,units}
```

As of 2026-08-09 the live sets are: libs `atc,icd10,icf,kva,local,loinc,
snomed,socialstyrelsen`; concept-types `Observation, Medication, Procedure,
Diagnsosis ICD10`; response-types `Boolean, Integer, numerical, Single choice,
multiple choice, Slider, Free text`.
