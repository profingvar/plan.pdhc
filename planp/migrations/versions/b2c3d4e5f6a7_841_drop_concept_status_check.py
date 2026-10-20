"""#841 — drop the Concept.status CHECK constraint; the column is retired

#839 added `ck_concepts_status` to enforce the three values
`fhir_codesystem.py` advertised for `concepts.status`. #841 then established
that the column was never meant to gate adoption: nothing in plan could move a
Concept out of `draft` — no promote/publish/activate/retire route, no control
in `concepts/create.html` or `concepts/edit.html`, and the importer hardcodes
`status='draft'` — so all 99 rows held the column default and a FHIR resource
status derived from it could only ever report `draft`.

The operator's decision (2026-10-20): **status is not meant to gate adoption.**
So the field is retired. It is removed from `to_dict()`, from the API write
surface, and from the CodeSystem property list, and the three terminology
wrappers now carry an explicit resource-level status again
(`fhir_helpers.RESOURCE_PUBLICATION_STATUS`).

**The column itself is deliberately KEPT.** It holds exactly one distinct
value, so dropping it would lose no information, and keeping it avoids an
irreversible schema change on the platform's semantic authority — plan's
Concepts validate every CDR write through the canonicaliser's plan-Concept
tier. What goes is the constraint, because a constraint on a field nothing
reads or writes is machinery guarding nothing, and leaving it would imply the
three values still mean something.

Reversible in both directions: `downgrade()` restores the constraint. Verified
before writing: all 99 live rows hold `draft`, so the downgrade cannot fail on
current data either.

Revision ID is 12 characters: `alembic_version` is `varchar(32)` and an id
over that length fails on Postgres while passing on SQLite, so the tests would
not catch it.

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
"""
from alembic import op

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None

CONSTRAINT = 'ck_concepts_status'


def upgrade():
    op.drop_constraint(CONSTRAINT, 'concepts', type_='check')


def downgrade():
    op.create_check_constraint(
        CONSTRAINT,
        'concepts',
        "status IS NULL OR status IN ('draft', 'active', 'retired')",
    )
