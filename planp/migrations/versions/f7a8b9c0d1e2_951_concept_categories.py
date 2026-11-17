"""#951: concept categories (many per concept), import provenance, and the
`Diagnsosis ICD10` -> `Diagnosis` type rename.

Revision ID: f7a8b9c0d1e2
Revises: e5f6a7b8c9d0
Create Date: 2026-11-17

Additive only. Every existing concept keeps NULL `import_guid` and no
category: 107 concepts (measured 2026-11-17) were made before either existed,
and inventing either would be fabricating provenance.
"""
from alembic import op
import sqlalchemy as sa

revision = 'f7a8b9c0d1e2'
down_revision = 'e5f6a7b8c9d0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'concept_imports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('guid', sa.String(36), nullable=False, unique=True),
        sa.Column('operator', sa.String(255), nullable=False),
        sa.Column('filename', sa.String(500), nullable=True),
        sa.Column('sha256', sa.String(64), nullable=True),
        sa.Column('entry_point', sa.String(16), nullable=False),
        sa.Column('default_categories', sa.Text(), nullable=True),
        sa.Column('n_in', sa.Integer(), nullable=False),
        sa.Column('n_created', sa.Integer(), nullable=False),
        sa.Column('n_updated', sa.Integer(), nullable=False),
        sa.Column('n_unchanged', sa.Integer(), nullable=False),
        sa.Column('n_rejected', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'concept_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('guid', sa.String(36), nullable=False, unique=True),
        sa.Column('category_name', sa.String(255), nullable=False, unique=True),
        sa.Column('category_display_text', sa.String(500), nullable=True),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('vers_number', sa.Integer(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.Column('date_valid', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'concept_category_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('concept_guid', sa.String(36), sa.ForeignKey('concepts.guid', ondelete='CASCADE'), nullable=False),
        sa.Column('category_guid', sa.String(36), sa.ForeignKey('concept_categories.guid'), nullable=False),
        sa.Column('import_guid', sa.String(36), sa.ForeignKey('concept_imports.guid'), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('concept_guid', 'category_guid', name='uq_concept_category'),
    )
    op.create_index('ix_concept_category_links_concept_guid', 'concept_category_links', ['concept_guid'])
    op.create_index('ix_concept_category_links_category_guid', 'concept_category_links', ['category_guid'])
    with op.batch_alter_table('concepts') as b:
        b.add_column(sa.Column('import_guid', sa.String(36), nullable=True))
        b.create_foreign_key('fk_concepts_import_guid', 'concept_imports', ['import_guid'], ['guid'])

    # #951 operator decision 2026-11-17: the live type `Diagnsosis ICD10` (a
    # typo, and the 19 concepts under it are not ICD-10) becomes `Diagnosis`.
    # Keyed on the old NAME so it is a no-op on any database without it; the
    # guid is untouched, so every concept keeps its type. No code reads the
    # name (grepped across all services 2026-11-17).
    op.execute(sa.text(
        "UPDATE concept_types SET concept_type_name = 'Diagnosis', "
        "concept_type_display_text = 'Diagnosis', vers_number = COALESCE(vers_number, 1) + 1 "
        "WHERE concept_type_name = 'Diagnsosis ICD10' "
        "AND NOT EXISTS (SELECT 1 FROM concept_types WHERE concept_type_name = 'Diagnosis')"))


def downgrade():
    op.execute(sa.text(
        "UPDATE concept_types SET concept_type_name = 'Diagnsosis ICD10', "
        "concept_type_display_text = 'Diagnosis ICD10' WHERE concept_type_name = 'Diagnosis' "
        "AND guid = '6ebf3c81-f849-4452-8c32-9ad24a2628c8'"))
    with op.batch_alter_table('concepts') as b:
        b.drop_constraint('fk_concepts_import_guid', type_='foreignkey')
        b.drop_column('import_guid')
    op.drop_index('ix_concept_category_links_category_guid', 'concept_category_links')
    op.drop_index('ix_concept_category_links_concept_guid', 'concept_category_links')
    op.drop_table('concept_category_links')
    op.drop_table('concept_categories')
    op.drop_table('concept_imports')
