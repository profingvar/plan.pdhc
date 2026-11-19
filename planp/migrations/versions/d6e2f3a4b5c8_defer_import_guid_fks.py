"""Check the two `import_guid` foreign keys at COMMIT, not per statement.

Revision ID: d6e2f3a4b5c8
Revises: c5d1e2f3a4b7
Create Date: 2026-11-19

The importer writes the concepts first and its ConceptImport record last,
because the record holds the final counts and may never be updated
(ConceptImportImmutable). With an immediate FK the first autoflush of a
concept pointing at the not-yet-written record failed on PostgreSQL, so no
real import has ever succeeded there (concept_imports empty, 2026-11-19).
SQLite does not enforce FKs in the test suite, which is why 767 tests were
green. Deferred, the check runs once at commit, when both rows exist.
"""
from alembic import op

revision = 'd6e2f3a4b5c8'
down_revision = 'c5d1e2f3a4b7'
branch_labels = None
depends_on = None

FKS = (('concepts', 'fk_concepts_import_guid'),
       ('concept_category_links', 'concept_category_links_import_guid_fkey'))


def _recreate(deferred: bool):
    if op.get_bind().dialect.name != 'postgresql':
        return       # SQLite (tests) does not enforce these FKs anyway
    for table, name in FKS:
        op.drop_constraint(name, table, type_='foreignkey')
        op.create_foreign_key(name, table, 'concept_imports', ['import_guid'], ['guid'],
                              **({'deferrable': True, 'initially': 'DEFERRED'} if deferred else {}))


def upgrade():
    _recreate(True)


def downgrade():
    _recreate(False)
