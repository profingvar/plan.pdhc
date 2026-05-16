"""add bounded-recurrence columns to activities

Revision ID: d4f5a6b71208
Revises: c2d6ef39a1f0
Create Date: 2026-05-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd4f5a6b71208'
down_revision = 'c2d6ef39a1f0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('activities',
        sa.Column('timing_bounds_mode', sa.String(length=20), nullable=True))
    op.add_column('activities',
        sa.Column('timing_bounds_count', sa.Integer(), nullable=True))
    op.add_column('activities',
        sa.Column('timing_bounds_duration_value', sa.Float(), nullable=True))
    op.add_column('activities',
        sa.Column('timing_bounds_duration_unit', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('activities', 'timing_bounds_duration_unit')
    op.drop_column('activities', 'timing_bounds_duration_value')
    op.drop_column('activities', 'timing_bounds_count')
    op.drop_column('activities', 'timing_bounds_mode')
