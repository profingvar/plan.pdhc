"""Named concept subsets (many per concept), and marking a concept for deletion.

Revision ID: c5d1e2f3a4b7
Revises: f7a8b9c0d1e2
Create Date: 2026-11-19

Additive only: two new tables and two nullable columns on `concepts`.
"""
from alembic import op
import sqlalchemy as sa

revision = 'c5d1e2f3a4b7'
down_revision = 'f7a8b9c0d1e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'concept_subsets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('guid', sa.String(36), nullable=False, unique=True),
        sa.Column('subset_name', sa.String(255), nullable=False, unique=True),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'concept_subset_links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('concept_guid', sa.String(36), sa.ForeignKey('concepts.guid', ondelete='CASCADE'), nullable=False),
        sa.Column('subset_guid', sa.String(36), sa.ForeignKey('concept_subsets.guid', ondelete='CASCADE'), nullable=False),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('concept_guid', 'subset_guid', name='uq_concept_subset'),
    )
    op.create_index('ix_concept_subset_links_concept_guid', 'concept_subset_links', ['concept_guid'])
    op.create_index('ix_concept_subset_links_subset_guid', 'concept_subset_links', ['subset_guid'])
    with op.batch_alter_table('concepts') as b:
        b.add_column(sa.Column('marked_for_deletion_at', sa.DateTime(), nullable=True))
        b.add_column(sa.Column('marked_for_deletion_by', sa.String(255), nullable=True))


def downgrade():
    with op.batch_alter_table('concepts') as b:
        b.drop_column('marked_for_deletion_by')
        b.drop_column('marked_for_deletion_at')
    op.drop_index('ix_concept_subset_links_subset_guid', 'concept_subset_links')
    op.drop_index('ix_concept_subset_links_concept_guid', 'concept_subset_links')
    op.drop_table('concept_subset_links')
    op.drop_table('concept_subsets')
