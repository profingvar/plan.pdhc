"""#839 — constrain Concept.status to the three values it has always claimed

`concepts.status` is a bare `String(20)` with `default='draft'` and no
constraint, while `fhir_codesystem.py` advertises it to FHIR clients as
"Concept editorial status (draft, active, retired)". Any string fitted in 20
characters was accepted, so the documented value set was a comment rather than
a rule.

Verified against production before writing this: all 99 concepts hold exactly
one distinct value, `draft`, and **0 rows** violate the constraint, so this is
additive and cannot fail on live data.

NULL is deliberately still allowed. The column is nullable and a Postgres CHECK
passes when its expression evaluates to NULL, so this adds no NOT NULL
behaviour by stealth — tightening nullability is a separate decision with a
separate blast radius.

Revision ID is 12 characters: `alembic_version` is `varchar(32)` and an id over
that length fails on Postgres while passing on SQLite, so the tests would not
catch it.

Revision ID: a1b2c3d4e5f6
Revises: e5a6b7c8d901
"""
from alembic import op

revision = 'a1b2c3d4e5f6'
down_revision = 'e5a6b7c8d901'
branch_labels = None
depends_on = None

CONSTRAINT = 'ck_concepts_status'
ALLOWED = ('draft', 'active', 'retired')


def upgrade():
    op.create_check_constraint(
        CONSTRAINT,
        'concepts',
        "status IS NULL OR status IN ('draft', 'active', 'retired')",
    )


def downgrade():
    op.drop_constraint(CONSTRAINT, 'concepts', type_='check')
