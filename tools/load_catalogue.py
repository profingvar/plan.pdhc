#!/usr/bin/env python3
"""One-file bulk loader for plan.pdhc: concepts + value sets + values.

Give it ONE YAML manifest describing a catalogue and it makes the right
plan.pdhc API calls, in dependency order, idempotently:

    1. ensure lookups          (canonical_libs / concept_types /
                                 response_types / units)   -- optional block
    2. create coded values     -> values_catalog           (POST /lookup/values)
    3. create value sets       -> valuesets + valueset_values
                                   (POST /lookup/valuesets, values inline)
    4. create concepts         -> concepts, bound to their value set
                                   (POST /concepts with `valueset`)

It is a superset of sim.pdhc/concepts/load_to_plan.py (which only did
concepts). Everything is matched BY NAME and reused if it already exists --
plan.pdhc's create endpoints auto-suffix duplicate names, so this script
never blind-POSTs; re-running the same manifest is a no-op.

Auth: the service-key path on plan.pdhc --
  X-Source-Service: loader.pdhc   +   X-Service-Key: $PLAN_LOADER_SERVICE_KEY
(the PLAN_LOADER_SERVICE_KEY value is in plan.pdhc/.env on miserver).

Usage:
    export PLAN_LOADER_SERVICE_KEY=...            # required
    python3 load_catalogue.py catalogue.yaml            # apply
    python3 load_catalogue.py catalogue.yaml --dry-run  # resolve + report only
    python3 load_catalogue.py catalogue.yaml --update   # also PUT valueset/fields
                                                         #   onto pre-existing concepts
    python3 load_catalogue.py catalogue.yaml --base https://plan.pdhc.se

Deps: requests, pyyaml (same as load_to_plan.py).
Writes <manifest>.guids.json next to the manifest with every issued GUID.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
import yaml

SOURCE_SERVICE = "loader.pdhc"

# plan.pdhc API paths (lookup CRUD lives under /api/v1/lookup/*; the older
# top-level /api/v1/canonical-libs paths the sim loader used are 404 on prod)
P_LIBS   = "/api/v1/lookup/canonical-libs"
P_TYPES  = "/api/v1/lookup/concept-types"
P_RESPS  = "/api/v1/lookup/response-types"
P_UNITS  = "/api/v1/lookup/units"
P_VALUES = "/api/v1/lookup/values"
P_VSETS  = "/api/v1/lookup/valuesets"
P_CONCEPTS = "/api/v1/concepts"


# --------------------------------------------------------------------------
# HTTP helpers
# --------------------------------------------------------------------------
class LoaderError(SystemExit):
    pass


def _headers(key: str) -> dict[str, str]:
    return {"X-Source-Service": SOURCE_SERVICE,
            "X-Service-Key": key,
            "Content-Type": "application/json"}


def _items(payload: Any) -> list[dict[str, Any]]:
    """Normalise a list endpoint that may be a bare list or {items:[...]}."""
    if isinstance(payload, dict) and "items" in payload:
        return payload["items"]
    return payload if isinstance(payload, list) else []


class Client:
    def __init__(self, base: str, key: str, dry_run: bool):
        self.base = base.rstrip("/")
        self.h = _headers(key)
        self.dry = dry_run

    def get_all(self, path: str) -> list[dict[str, Any]]:
        """GET a (possibly paginated) list endpoint and return all rows."""
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            r = requests.get(f"{self.base}{path}",
                             params={"page": page, "per_page": 200},
                             headers=self.h, timeout=20)
            r.raise_for_status()
            body = r.json()
            rows = _items(body)
            out.extend(rows)
            # bare-list endpoints aren't paginated -> stop after one pass
            if not isinstance(body, dict) or len(rows) < (body.get("per_page") or 200):
                break
            page += 1
            if page > 100:
                raise LoaderError(f"safety stop: >100 pages on {path}")
        return out

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if self.dry:
            return {"guid": f"<dry-run:{path}>", "_dry": True}
        r = requests.post(f"{self.base}{path}", headers=self.h, json=body, timeout=30)
        if r.status_code not in (200, 201):
            raise LoaderError(f"POST {path} -> {r.status_code}: {r.text[:300]}")
        return r.json()

    def put(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if self.dry:
            return {"_dry": True}
        r = requests.put(f"{self.base}{path}", headers=self.h, json=body, timeout=30)
        if r.status_code not in (200, 201):
            raise LoaderError(f"PUT {path} -> {r.status_code}: {r.text[:300]}")
        return r.json()


# --------------------------------------------------------------------------
# Loader
# --------------------------------------------------------------------------
def _by(rows: list[dict[str, Any]], field: str) -> dict[str, str]:
    return {(r.get(field) or "").strip(): r["guid"] for r in rows if r.get("guid")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", nargs="?", help="path to the catalogue YAML")
    ap.add_argument("--from-csv", metavar="CONCEPTS.csv[,VALUESETS.csv]",
                    help="load the flat concept CSV (+ optional value-set CSV) "
                         "instead of a YAML manifest")
    ap.add_argument("--base", default=os.environ.get("PLAN_PDHC_BASE_URL",
                                                      "https://plan.pdhc.se"))
    ap.add_argument("--dry-run", action="store_true",
                    help="resolve names + report; make no writes")
    ap.add_argument("--update", action="store_true",
                    help="also PUT valueset/fields onto pre-existing concepts")
    args = ap.parse_args()

    key = os.environ.get("PLAN_LOADER_SERVICE_KEY")
    if not key and not args.dry_run:
        print("ERROR: PLAN_LOADER_SERVICE_KEY not set", file=sys.stderr)
        return 2

    if args.from_csv:
        parts = [p.strip() for p in args.from_csv.split(",") if p.strip()]
        concept_csv = Path(parts[0]).resolve()
        valueset_csv = Path(parts[1]).resolve() if len(parts) > 1 else None
        spec = _spec_from_csv(concept_csv, valueset_csv)
        man_path = concept_csv
    elif args.manifest:
        man_path = Path(args.manifest).resolve()
        spec = yaml.safe_load(man_path.read_text())
        if not isinstance(spec, dict):
            print("ERROR: manifest must be a YAML mapping", file=sys.stderr)
            return 2
    else:
        ap.error("provide a catalogue YAML, or --from-csv CONCEPTS.csv[,VALUESETS.csv]")

    cli = Client(args.base, key or "", args.dry_run)
    default_lib = spec.get("default_canonical_lib")
    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"=== load_catalogue [{mode}] {man_path.name} -> {cli.base} ===")

    # --- 1. lookups (resolve, then ensure any declared-missing) ------------
    libs  = _by(cli.get_all(P_LIBS),  "canonical_lib_name")
    types = _by(cli.get_all(P_TYPES), "concept_type_name")
    resps = _by(cli.get_all(P_RESPS), "response_type_name")
    units = _by(cli.get_all(P_UNITS), "unit_name")
    print(f"lookups: libs={len(libs)} types={len(types)} "
          f"resps={len(resps)} units={len(units)}")

    ensure = spec.get("ensure") or {}
    _ensure_lookup(cli, ensure.get("canonical_libs"), libs, P_LIBS,
                   "canonical_lib_name", "canonical_lib_display_text",
                   extra={"canonical_lib_url": "url"})
    _ensure_lookup(cli, ensure.get("concept_types"), types, P_TYPES,
                   "concept_type_name", "concept_type_display_text")
    _ensure_lookup(cli, ensure.get("response_types"), resps, P_RESPS,
                   "response_type_name", "response_type_display_text")
    _ensure_lookup(cli, ensure.get("units"), units, P_UNITS,
                   "unit_name", "unit_display_text")

    def lib_guid(name: str | None) -> str | None:
        name = name or default_lib
        return libs.get(name) if name else None

    # --- 2. values ---------------------------------------------------------
    values_by = _by(cli.get_all(P_VALUES), "value_name")
    v_created = 0
    for v in spec.get("values") or []:
        vname = v["name"].strip()
        if vname in values_by:
            continue
        lg = lib_guid(v.get("canonical_lib"))
        if not lg:
            raise LoaderError(f"value {vname!r}: canonical_lib unresolved "
                              f"({v.get('canonical_lib') or default_lib!r})")
        res = cli.post(P_VALUES, {
            "value_name": vname,
            "canonical_lib": lg,
            "canonical_refnumber": v.get("ref"),
            "value_display_text": v.get("display"),
            "value_explanation": v.get("explanation"),
            "author": SOURCE_SERVICE,
        })
        values_by[vname] = res["guid"]
        v_created += 1
    print(f"values: {v_created} created, {len(values_by)} total known")

    # --- 3. value sets (with inline values + sort_order) -------------------
    vsets_by = _by(cli.get_all(P_VSETS), "valueset_name")
    vs_created = 0
    for vs in spec.get("valuesets") or []:
        vsname = vs["name"].strip()
        member_names = vs.get("values") or []
        missing = [m for m in member_names if m not in values_by]
        if missing:
            raise LoaderError(f"valueset {vsname!r} references unknown "
                              f"value(s): {', '.join(missing)}")
        members = [{"value_guid": values_by[m], "sort_order": i}
                   for i, m in enumerate(member_names, start=1)]
        if vsname in vsets_by:
            # already exists: converge missing links (409 = already there = ok)
            vg = vsets_by[vsname]
            for mem in members:
                try:
                    cli.post(f"{P_VSETS}/{vg}/values", mem)
                except LoaderError as e:
                    if "409" not in str(e):
                        raise
            continue
        lg = lib_guid(vs.get("canonical_lib"))
        if not lg:
            raise LoaderError(f"valueset {vsname!r}: canonical_lib unresolved")
        res = cli.post(P_VSETS, {
            "valueset_name": vsname,
            "canonical_lib": lg,
            "valueset_display_text": vs.get("display"),
            "valueset_explanation": vs.get("explanation"),
            "author": SOURCE_SERVICE,
            "values": members,
        })
        vsets_by[vsname] = res["guid"]
        vs_created += 1
    print(f"valuesets: {vs_created} created, {len(vsets_by)} total known")

    # --- 4. concepts -------------------------------------------------------
    concepts_by = _by(cli.get_all(P_CONCEPTS), "concept_name")
    c_created = c_updated = c_skipped = 0
    out_concepts: dict[str, dict[str, Any]] = {}
    for c in spec.get("concepts") or []:
        cname = c["name"].strip()
        vs_guid = vsets_by.get(c["valueset"].strip()) if c.get("valueset") else None
        if c.get("valueset") and not vs_guid:
            raise LoaderError(f"concept {cname!r}: valueset "
                              f"{c['valueset']!r} not found")

        if cname in concepts_by:
            guid = concepts_by[cname]
            if args.update:
                patch: dict[str, Any] = {}
                if vs_guid:
                    patch["valueset"] = vs_guid
                if c.get("range_low") is not None:
                    patch["range_low"] = c["range_low"]
                if c.get("range_high") is not None:
                    patch["range_high"] = c["range_high"]
                if patch:
                    cli.put(f"{P_CONCEPTS}/{guid}", patch)
                    c_updated += 1
                else:
                    c_skipped += 1
            else:
                c_skipped += 1
            out_concepts[cname] = {"guid": guid, "status": "existing"}
            continue

        lg = lib_guid(c.get("canonical_lib"))
        if not lg:
            raise LoaderError(f"concept {cname!r}: canonical_lib unresolved")
        body: dict[str, Any] = {
            "concept_name": cname,
            "concept_display_text": c.get("display"),
            "canonical_lib": lg,
            "canonical_refnumber": c.get("canonical_refnumber"),
            "status": c.get("status", "draft"),
        }
        for field, table in (("concept_type", types), ("response_type", resps),
                             ("unit", units)):
            if c.get(field) is not None:
                g = table.get(c[field])
                if not g:
                    raise LoaderError(f"concept {cname!r}: {field} "
                                      f"{c[field]!r} not found")
                body[field] = g
        if vs_guid:
            body["valueset"] = vs_guid
        for rng in ("range_low", "range_high"):
            if c.get(rng) is not None:
                body[rng] = c[rng]

        res = cli.post(P_CONCEPTS, body)
        concepts_by[cname] = res["guid"]
        out_concepts[cname] = {"guid": res["guid"], "status": "created",
                               "valueset": c.get("valueset")}
        c_created += 1

    print(f"concepts: {c_created} created, {c_updated} updated, "
          f"{c_skipped} existing-skipped")

    # --- summary -----------------------------------------------------------
    summary = {
        "manifest": man_path.name,
        "version": spec.get("version"),
        "base": cli.base,
        "dry_run": args.dry_run,
        "canonical_lib_guids": libs,
        "value_guids": values_by,
        "valueset_guids": vsets_by,
        "concepts": out_concepts,
        "stats": {"values_created": v_created, "valuesets_created": vs_created,
                  "concepts_created": c_created, "concepts_updated": c_updated,
                  "concepts_skipped": c_skipped},
    }
    if not args.dry_run:
        out = man_path.with_suffix(man_path.suffix + ".guids.json")
        out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        print(f"guids written: {out}")
    print("=== done ===")
    return 0


def _cell(row: dict, key: str):
    v = row.get(key)
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _spec_from_csv(concept_csv: Path, valueset_csv: "Path | None") -> dict:
    """Build the same spec dict the YAML path produces, from the two CSVs.

    concept CSV  = the flat #134 columns + an optional `valueset` column
                   (the native importer ignores the extra column).
    valueset CSV = one row per option:
                   valueset_name, valueset_display, value_name,
                   canonical_lib, canonical_ref, display_text, sort_order
    """
    spec: dict[str, Any] = {"version": "csv", "values": [],
                            "valuesets": [], "concepts": []}

    with open(concept_csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = _cell(row, "concept_name")
            if not name:
                continue
            c: dict[str, Any] = {"name": name}
            for col, key in (("display_text", "display"),
                             ("canonical_lib", "canonical_lib"),
                             ("canonical_ref", "canonical_refnumber"),
                             ("concept_type", "concept_type"),
                             ("response_type", "response_type"),
                             ("unit", "unit"),
                             ("valueset", "valueset")):
                val = _cell(row, col)
                if val is not None:
                    c[key] = val
            for rng in ("range_low", "range_high"):
                val = _cell(row, rng)
                if val is not None:
                    c[rng] = float(val)
            spec["concepts"].append(c)

    if valueset_csv:
        seen_values: dict[str, dict] = {}
        vsets: dict[str, dict] = {}
        with open(valueset_csv, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                vsname = _cell(row, "valueset_name")
                vname = _cell(row, "value_name")
                if not vsname or not vname:
                    continue
                lib = _cell(row, "canonical_lib")
                if vname not in seen_values:
                    val = {"name": vname}
                    if _cell(row, "canonical_ref"):
                        val["ref"] = _cell(row, "canonical_ref")
                    if _cell(row, "display_text"):
                        val["display"] = _cell(row, "display_text")
                    if lib:
                        val["canonical_lib"] = lib
                    seen_values[vname] = val
                    spec["values"].append(val)
                vs = vsets.setdefault(vsname, {"name": vsname, "_rows": []})
                if _cell(row, "valueset_display") and "display" not in vs:
                    vs["display"] = _cell(row, "valueset_display")
                if lib and "canonical_lib" not in vs:
                    vs["canonical_lib"] = lib
                try:
                    order = int(_cell(row, "sort_order") or 0)
                except ValueError:
                    order = 0
                vs["_rows"].append((order, vname))
        for vs in vsets.values():
            entry: dict[str, Any] = {
                "name": vs["name"],
                "values": [n for _, n in sorted(vs["_rows"], key=lambda t: t[0])],
            }
            if "display" in vs:
                entry["display"] = vs["display"]
            if "canonical_lib" in vs:
                entry["canonical_lib"] = vs["canonical_lib"]
            spec["valuesets"].append(entry)

    return spec


def _ensure_lookup(cli: "Client", decls, name_map: dict[str, str], path: str,
                   name_field: str, display_field: str,
                   extra: dict[str, str] | None = None) -> None:
    """Create any declared lookup rows that don't already exist (by name)."""
    for d in decls or []:
        nm = d["name"].strip()
        if nm in name_map:
            continue
        body = {name_field: nm, "author": SOURCE_SERVICE}
        if d.get("display"):
            body[display_field] = d["display"]
        for body_key, decl_key in (extra or {}).items():
            if d.get(decl_key):
                body[body_key] = d[decl_key]
        res = cli.post(path, body)
        name_map[nm] = res.get("guid", f"<dry:{nm}>")
        print(f"  + ensured {path.rsplit('/', 1)[-1]}: {nm}")


if __name__ == "__main__":
    sys.exit(main())
