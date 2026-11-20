"""Continuous activities: expected sampling interval (2026-11-20).

Revision ID: a1c2e3f4b5d6
Revises: d6e2f3a4b5c8
Create Date: 2026-11-20

Additive only: two nullable columns. A continuous activity (timing_type
'continuous') is ordered once, runs for its duration bound and streams data
about every sample interval; see app/services/continuous_timing.py. Existing
activities keep NULL and are unaffected.
"""
from alembic import op
import sqlalchemy as sa

revision = 'a1c2e3f4b5d6'
down_revision = 'd6e2f3a4b5c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('activities', sa.Column('sample_interval_value', sa.Float(), nullable=True))
    op.add_column('activities', sa.Column('sample_interval_unit', sa.String(10), nullable=True))


def downgrade():
    op.drop_column('activities', 'sample_interval_unit')
    op.drop_column('activities', 'sample_interval_value')
