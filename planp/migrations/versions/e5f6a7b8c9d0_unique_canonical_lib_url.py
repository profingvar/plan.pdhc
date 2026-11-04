"""canonical_lib_url becomes UNIQUE (#875)

The column was not unique, and two libraries held the same value: `icd10`
carried a copy of `snomed`'s URL (the SNOMED-SE browser address). Measured
in production 2026-11-02 and repaired 2026-11-04; this migration is the half
that stops it recurring.

WHY A CONSTRAINT AND NOT JUST A FIX. `resolve_canonical_lib` queried this
column with `.first()`, so two matching rows collapsed into one and the
answer depended on row order. The cost was measured on the day it was found:

  - `$validate-code` answered FALSE for 89 correctly-stored ICD-10 codes,
    because `scoped_validate_code` skips a row whose `lib.guid` differs from
    the resolved target, and the resolved target was `snomed`.
  - `_build_compose` groups values by this column, so plan SERVED those
    ICD-10 codes under the SNOMED CT system URI. `Z94.1` is not a SNOMED
    code. That is wrong FHIR published outward, and it is the worse half.

The failure mode is the point: it answered CONFIDENTLY with the wrong
library, and nothing in the response said "ambiguous". A constraint turns
the next such drift into a refusal at write time.

HOW IT GOT IN, since the question matters for whether a constraint is
enough. No migration in this directory writes `canonical_lib_url` at all —
checked 2026-11-04 — so the production value did not come from the migration
history. It came from one of FOUR unguarded write paths: the JSON API create
and update (`app/api/lookup_tables.py`) and the HTML admin create and update
(`app/routes/lookup_tables.py`). Every one of them already checked
`canonical_lib_name` for uniqueness. The name was protected in two layers
and the URL in none. All four now check, and this constraint is the backstop
under them.

NULLABLE AND UNIQUE IS DELIBERATE. Postgres permits many NULLs under a
UNIQUE, so any number of libraries may lack a URL while two claiming the
same one is refused. Empty strings do NOT behave that way — two `''` values
collide — so this migration normalises `''` to NULL before adding the
constraint, and `services/canonical_libs.normalise_lib_url` keeps new writes
doing the same.

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-11-04

"""
from alembic import op
from sqlalchemy import text


revision = 'e5f6a7b8c9d0'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None

CONSTRAINT = 'uq_canonical_libs_canonical_lib_url'


def upgrade():
    conn = op.get_bind()

    # 1. '' means "no URL" and must become NULL, or two blank rows collide
    #    under the constraint and this migration fails on data that is not
    #    actually in conflict.
    blanks = conn.execute(text("""
        UPDATE canonical_libs SET canonical_lib_url = NULL
         WHERE canonical_lib_url IS NOT NULL
           AND btrim(canonical_lib_url) = ''
        RETURNING canonical_lib_name
    """)).fetchall()
    if blanks:
        print(f"[{revision}] normalised '' -> NULL for: "
              f"{', '.join(r[0] for r in blanks)}")

    # 2. Report the premise rather than asserting the measurement taken
    #    elsewhere. This database may not be the one that was measured, and
    #    a duplicate here is a repair decision, not something a migration
    #    should make on someone's behalf.
    dupes = conn.execute(text("""
        SELECT canonical_lib_url,
               string_agg(canonical_lib_name, ', ' ORDER BY id) AS libs,
               count(*) AS n
          FROM canonical_libs
         WHERE canonical_lib_url IS NOT NULL
      GROUP BY canonical_lib_url
        HAVING count(*) > 1
      ORDER BY n DESC
    """)).fetchall()

    if dupes:
        lines = "\n".join(
            f"    {r[2]} libraries share {r[0]!r}: {r[1]}" for r in dupes)
        raise RuntimeError(
            f"[{revision}] REFUSING to add the UNIQUE constraint: "
            f"{len(dupes)} duplicate canonical_lib_url value(s) exist.\n"
            f"{lines}\n"
            "  Nothing has been changed. Decide which library owns each URL "
            "and correct the others FIRST -- a migration must not pick, "
            "because picking by row order is the #875 defect itself. The "
            "seed migration c2d6ef39a1f0 records each library's intended "
            "URL if you need the original values."
        )

    print(f"[{revision}] no duplicates; adding {CONSTRAINT}")
    op.create_unique_constraint(
        CONSTRAINT, 'canonical_libs', ['canonical_lib_url'])


def downgrade():
    op.drop_constraint(CONSTRAINT, 'canonical_libs', type_='unique')
