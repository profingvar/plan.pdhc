"""canonical_libs.whole_system_answer_space + the icd11-mms library

Why this exists, measured 2026-10-21 from icd11.pdhc's first live Condition
projection.

`$validate-code` answers "is this CODE adopted?" by looking for a Concept or
ValueCatalog row whose `canonical_refnumber` equals the code. That is the right
question for a MEASUREMENT vocabulary -- an unplanned LOINC code is meaningless,
so requiring a row is the gate working.

It is the wrong question for a CLASSIFICATION. An ICD-11 diagnosis is chosen
from ~85 000 codes at the point of care, and the adopted set is the whole
classification by design and by the 1 Jan 2029 national reporting obligation.
It cannot be enumerated in advance, so cdr.pdhc rejected every projected
Condition with `plan_miss`.

`whole_system_answer_space` lets a library say so. Default FALSE, so all five
existing libraries (loinc, socialstyrelsen, icd10, atc, snomed) keep exactly
their current behaviour.

**This is not a loosening of cdr's write gate.** cdr still asks plan.pdhc and
still believes only `result: true`; plan still answers `false` for a library it
does not know. What changes is the GRANULARITY at which plan declares adoption,
for the libraries where per-code adoption is not a meaningful concept.

Note `icd10` is deliberately left FALSE here. An ICD-10-SE *diagnosis* faces the
same mismatch, but `icd10` is also used for non-diagnosis purposes in existing
plans, so flipping it is a separate editorial decision with its own blast
radius -- not something to bundle into this migration.

Idempotent: the column add is guarded, and the library insert is guarded on
`canonical_lib_name`.

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-10-21

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None

LIB_NAME = 'icd11-mms'
LIB_DISPLAY = 'ICD-11 Mortality and Morbidity Statistics (WHO)'
# termbank is where the platform RESOLVES a code (Rule 6). WHO remains the
# source of ICD-11 itself (icd11.pdhc plan §2.a); termbank holds a used-concept
# mirror, not the classification.
LIB_URL = 'https://termbank.pdhc.se/CodeSystem/icd11-mms'


def upgrade():
    conn = op.get_bind()
    cols = {c['name'] for c in sa.inspect(conn).get_columns('canonical_libs')}
    if 'whole_system_answer_space' not in cols:
        op.add_column('canonical_libs', sa.Column(
            'whole_system_answer_space', sa.Boolean(),
            nullable=False, server_default='false'))

    exists = conn.execute(
        text("SELECT 1 FROM canonical_libs WHERE canonical_lib_name = :n"),
        {"n": LIB_NAME},
    ).first()
    if exists is None:
        conn.execute(text("""
            INSERT INTO canonical_libs (
                guid, canonical_lib_name, canonical_lib_display_text,
                canonical_lib_url, author, vers_number,
                whole_system_answer_space, date_created, date_valid
            ) VALUES (
                gen_random_uuid()::text, :n, :d, :u, :a, 1,
                true, now(), now()
            )
        """), {"n": LIB_NAME, "d": LIB_DISPLAY, "u": LIB_URL,
               "a": "migration c3d4e5f6a7b8"})
    else:
        # The library was created by hand before this migration ran. Set the
        # flag rather than leaving it at the column default, or the row exists
        # and still refuses every code.
        conn.execute(text("""
            UPDATE canonical_libs SET whole_system_answer_space = true
            WHERE canonical_lib_name = :n
        """), {"n": LIB_NAME})


def downgrade():
    conn = op.get_bind()
    # The library row is left in place: a Concept may already reference it, and
    # dropping it would orphan that reference. Only the flag is reverted, which
    # restores per-code adoption for it.
    conn.execute(text("""
        UPDATE canonical_libs SET whole_system_answer_space = false
        WHERE canonical_lib_name = :n
    """), {"n": LIB_NAME})
    cols = {c['name'] for c in sa.inspect(conn).get_columns('canonical_libs')}
    if 'whole_system_answer_space' in cols:
        op.drop_column('canonical_libs', 'whole_system_answer_space')
