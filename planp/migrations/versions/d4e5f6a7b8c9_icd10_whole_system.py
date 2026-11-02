"""icd10 joins icd11-mms as a whole-system answer space (#872)

The deferred half of c3d4e5f6a7b8. That migration flipped `icd11-mms` and
left `icd10` FALSE on this stated reason:

    "An ICD-10-SE *diagnosis* faces the same mismatch, but `icd10` is also
     used for non-diagnosis purposes in existing plans, so flipping it is a
     separate editorial decision with its own blast radius."

**Measured against production 2026-11-01, and the blast radius is empty:**

    canonical_lib_name | concepts | values
    -------------------+----------+-------
    icd10              |        0 |      0

Nine libs exist; `local` (34 concepts, 48 values), `loinc` (35/3),
`snomed` (21/0) and `atc` (9/0) carry everything. Nothing references
`icd10` at all. The concern was reasonable as a category and false in fact.

Why flip rather than split. The alternative was a second canonical lib for
diagnoses only. That gives the same ICD-10 code two possible canonical URIs
depending on which lib it arrived through, and cdr.pdhc deduplicates
resources on `code_canonical` — so the same diagnosis would stop
deduplicating against itself. One identifier per code system is worth more
than purpose-purity here.

What this does NOT solve, stated so nobody assumes it did:

  - The flag is per-LIBRARY. Flipping it accepts ANY ICD-10 code for ANY
    purpose, diagnosis or not. If purpose-scoping is ever needed, it does
    NOT live here.
  - And it cannot live in the scoped `$validate-code` path either:
    `scoped_validate_code` walks enumerated `values_catalog` rows, so a
    ValueSet can express "one of these twelve codes" but never "any code of
    this classification". Purpose-scoping a whole classification is an open
    problem, not a solved one.
  - Per-release acceptance is untouched. Nothing stops a code being entered
    after it stops being nationally accepted (icd11.pdhc open item 19b).

Order of checks is unchanged and matters: Concept, then ValueCatalog, then
the whole-system branch. So any icd10 row added later still answers per code
with its own display and ref_guid; this flag only changes the answer for a
code that has NO row, from `false` to `true`.

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-11-01

"""
from alembic import op
from sqlalchemy import text


revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None

LIB_NAME = 'icd10'


def _report(conn, when: str) -> None:
    """Print what this library actually holds when the migration runs.

    The decision above rests on a measurement taken on 2026-11-01. This
    database may not be that one, and may not be in that state any more, so
    the migration records its own premise in the deploy log rather than
    asserting mine.
    """
    row = conn.execute(text("""
        SELECT (SELECT count(*) FROM concepts c
                  JOIN canonical_libs l ON c.canonical_lib = l.guid
                 WHERE l.canonical_lib_name = :n) AS concepts,
               (SELECT count(*) FROM values_catalog v
                  JOIN canonical_libs l ON v.canonical_lib = l.guid
                 WHERE l.canonical_lib_name = :n) AS values
    """), {"n": LIB_NAME}).first()
    if row is not None:
        print(f"[{revision}] {LIB_NAME} {when}: "
              f"{row[0]} concepts, {row[1]} values_catalog rows")


def upgrade():
    conn = op.get_bind()
    exists = conn.execute(
        text("SELECT 1 FROM canonical_libs WHERE canonical_lib_name = :n"),
        {"n": LIB_NAME},
    ).first()
    if exists is None:
        # Nothing to flip. Deliberately not an error: a fresh database that
        # has not seeded this library is a valid state, and inventing the row
        # here would create a library nobody asked for.
        print(f"[{revision}] no '{LIB_NAME}' library in canonical_libs — nothing to do")
        return
    _report(conn, "at upgrade")
    conn.execute(text("""
        UPDATE canonical_libs SET whole_system_answer_space = true
        WHERE canonical_lib_name = :n
    """), {"n": LIB_NAME})


def downgrade():
    conn = op.get_bind()
    _report(conn, "at downgrade")
    conn.execute(text("""
        UPDATE canonical_libs SET whole_system_answer_space = false
        WHERE canonical_lib_name = :n
    """), {"n": LIB_NAME})
