"""#787.1: enforce three of the four unenforced GUID references.

The #786 item-5 inventory found four columns that name a row in another table
with nothing in the database enforcing it, while every other GUID reference
inside plan.pdhc has a real FK. Four separate silences is not a decision, so
#787 asked for one per column. Measured on production 2026-10-13 before
deciding, and all four currently hold **zero dangling values**, which is why
this is cheap today and would not be later.

## Three get the FK

| column | -> target | rows set / dangling |
|---|---|---|
| plan_definitions.form_definition_guid | form_definitions.guid | 0 / 0 |
| plandefinition_goals.target_value_guid | values_catalog.guid | 0 / 0 |
| form_definition_items.concept_guid | concepts.guid | 32 / 0 |

All three targets are UNIQUE, all three references are intra-service, and all
three are the shape #787 complained about: delete a concept and
`form_definition_items.concept_guid` still names it, with nothing complaining
at delete time and the failure surfacing later in a rendered questionnaire,
far from the cause.

ON DELETE is left at the default (NO ACTION / RESTRICT) deliberately, and that
is the point of the ticket rather than an incidental choice. RESTRICT makes the
database refuse to delete a concept that a form item still references, so the
error arrives at the moment of the mistake and names it. CASCADE would have
been worse than the status quo: it would silently delete form items when a
concept went, turning a dangling reference into missing content. SET NULL would
turn it into a form item with no concept, which is the same invalid state the
FK exists to prevent, just spelled NULL.

## The fourth does NOT get one, and this is the recorded reason

`form_definitions.produced_form_guid` -> `questionnaires.form_guid` cannot take
an FK, and not because of an oversight:

* `questionnaires.form_guid` is NOT unique, and must not be. The model is
  **(form_guid, version)** -- `app/api/forms.py:157` and `:177` look up
  `filter_by(form_guid=..., version=version)`, and `:163`/`:183` fall back to
  `filter_by(form_guid=...).order_by(...)` for the latest. So the reference
  points at a COLLECTION of versions, not at a row, and an FK is the wrong
  tool for it.
* It looks 1:1 in today's data (7 questionnaires, 7 distinct form_guid, max 1
  per form_guid) purely because nothing has been versioned yet. Adding UNIQUE
  to make the FK possible would have silently forbidden a second version --
  breaking the feature the column exists for, on the evidence of a dataset
  that has not exercised it.

What cleans up a dangling one, since #787 asked: the delete path already
exists -- `app/routes/forms.py:290` does
`Questionnaire.query.filter_by(form_guid=form_guid).delete()`, removing every
version for a form together. The remaining exposure is the reverse direction (a
`form_definitions` row naming a `form_guid` whose questionnaires were all
deleted), which is a report-level concern, not an integrity one, because the
renderer treats "no questionnaire for this form" as a state it must handle
anyway.

Revision ID: e5a6b7c8d901
Revises: d4f5a6b71208
Create Date: 2026-10-13
"""
from alembic import op
import sqlalchemy as sa

revision = "e5a6b7c8d901"
down_revision = "d4f5a6b71208"
branch_labels = None
depends_on = None

# (constraint name, table, column, target table, target column)
FKS = [
    ("fk_plan_definitions_form_definition_guid",
     "plan_definitions", "form_definition_guid", "form_definitions", "guid"),
    ("fk_plandefinition_goals_target_value_guid",
     "plandefinition_goals", "target_value_guid", "values_catalog", "guid"),
    ("fk_form_definition_items_concept_guid",
     "form_definition_items", "concept_guid", "concepts", "guid"),
]


def _existing(insp, table):
    try:
        return {fk.get("name") for fk in insp.get_foreign_keys(table)}
    except Exception:
        return set()


def upgrade():
    bind = op.get_bind()
    # SQLite cannot ALTER TABLE ADD CONSTRAINT, and the test suite runs on it.
    # Skipping there rather than batch-rebuilding four tables: the constraint
    # being tested is a Postgres-side guarantee, and a batch rebuild of live
    # tables is a far bigger risk than the coverage is worth.
    if bind.dialect.name == "sqlite":
        return
    insp = sa.inspect(bind)
    tables = set(insp.get_table_names())
    for name, table, col, ref_table, ref_col in FKS:
        if table not in tables or ref_table not in tables:
            continue
        if col not in {c["name"] for c in insp.get_columns(table)}:
            continue
        if name in _existing(insp, table):
            continue
        op.create_foreign_key(name, table, ref_table, [col], [ref_col])


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        return
    insp = sa.inspect(bind)
    tables = set(insp.get_table_names())
    for name, table, _col, _rt, _rc in FKS:
        if table in tables and name in _existing(insp, table):
            op.drop_constraint(name, table, type_="foreignkey")
