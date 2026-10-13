"""#771 — PlanDefinition carries TWO independent identifiers, deliberately.

The question asked was: "sort out the difference between FHIR GUID and Careplan
Guid — if they are 1:1 they should merge." They ARE 1:1. The decision, taken
2026-10-13, is **not to merge**, and this module exists so nobody has to
re-derive the measurements that settled it.

## What was measured on production

    plan_definition rows        3
    distinct guid               3
    fhir_id set                 3
    distinct fhir_id            3
    rows where guid = fhir_id   0      <- two independent uuid4 values
    fhir_id NULL                0

So they are 1:1 in cardinality, both always present, and never equal.

## Why they do not merge

Each is load-bearing in a different plane, and a merge in either direction
breaks the other:

* `guid` is the INTERNAL identifier. Every downstream store holds it:
  `clinical_context.plan_definition_guid` on cdr1/cdr2/cdr3 (40,941 rows
  measured 2026-10-13), `service_requests.plan_definition_guid` in
  request.pdhc (27 rows), and cdr_6's observation table. Merging onto
  `fhir_id` means rewriting all of them.

* `fhir_id` is the PUBLISHED FHIR identifier. It is the resource id in
  `/fhir/PlanDefinition/<fhir_id>`, and it is what `fhir_canonical_url()`
  builds `resource['url']` and bundle `fullUrl` from
  (`app/api/fhir_plandefinitions.py`). FHIR canonical URLs are specified to be
  stable, and a provider may hold one. Merging onto `guid` changes them.

This is the ordinary FHIR distinction between a business identifier and a
resource id, not an accident. The duplication costs one extra column; unifying
it costs either ~41,000 row rewrites or a published-URL break.

## What these tests are for

To make the invariant the decision rests on impossible to lose quietly. If a
future change makes the two columns diverge in cardinality, or lets one go
NULL, the premise of "don't merge" is gone and someone should revisit it — and
these fail rather than the question being silently re-opened.
"""
from __future__ import annotations

import uuid


def _model():
    from app.models.fhir_models import PlanDefinition
    return PlanDefinition


def test_both_columns_exist_and_are_separately_UNIQUE():
    """The 1:1 claim rests on the database enforcing uniqueness on each, not
    on the current data happening to look that way."""
    cols = _model().__table__.c
    for name in ("guid", "fhir_id"):
        assert name in cols, f"PlanDefinition lost its {name} column"
        assert cols[name].unique, f"{name} is no longer UNIQUE"


def test_neither_column_is_NULLABLE():
    """A NULL on either side would mean a PlanDefinition reachable by one
    identifier and not the other — the 1:1 premise gone, silently."""
    cols = _model().__table__.c
    assert not cols["guid"].nullable, "guid became nullable"
    assert not cols["fhir_id"].nullable, "fhir_id became nullable"


def test_they_are_INDEPENDENTLY_generated_and_so_never_equal():
    """Measured on production: 0 of 3 rows have guid = fhir_id. That is
    because each column defaults to its own uuid4. If one were ever defaulted
    FROM the other, this stops being two identifiers and the merge question
    changes — so the independence is asserted, not assumed."""
    cols = _model().__table__.c

    # Deliberately NOT `PlanDefinition()`. Instantiating it configures the
    # mapper, which needs PlanDefinitionGoal imported, which happens only
    # because some OTHER test module imported it first — so this file passed
    # in the full suite and failed when run alone. That is the same
    # order-dependence #810 was about, and a test that only passes with
    # neighbours is not a test. Calling the column defaults directly needs
    # neither a mapper nor a database.
    def mint(name):
        return cols[name].default.arg(None)

    a_guid, a_fhir = mint("guid"), mint("fhir_id")
    b_guid, b_fhir = mint("guid"), mint("fhir_id")

    assert a_guid != a_fhir, (
        "guid and fhir_id now generate the same value — if that is deliberate, "
        "#771's merge question should be re-opened rather than achieved by "
        "accident")
    assert a_guid != b_guid and a_fhir != b_fhir
    for v in (a_guid, a_fhir):
        uuid.UUID(v)              # both are real uuids
        assert len(v) <= 36       # both fit String(36)


def test_the_FHIR_surface_still_keys_on_fhir_id_not_guid():
    """Half of the reason not to merge. If the FHIR routes ever switch to
    `guid`, then `fhir_id` stops being externally published and the merge
    becomes cheap — which is exactly when this decision should be revisited.
    """
    import inspect
    from app.api import fhir_plandefinitions as m

    src = inspect.getsource(m)
    assert "filter_by(fhir_id=fhir_id)" in src, (
        "the FHIR read route no longer looks up by fhir_id")
    assert "fhir_canonical_url('PlanDefinition', pd.fhir_id)" in src, (
        "the published canonical URL is no longer built from fhir_id — "
        "re-check #771, the cost of merging may have changed")
