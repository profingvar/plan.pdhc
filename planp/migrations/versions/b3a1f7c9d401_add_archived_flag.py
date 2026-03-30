"""add archived flag to plan_definitions, questionnaires, form_definitions

Revision ID: b3a1f7c9d401
Revises: 90b8f8b2a562
Create Date: 2026-03-30 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a1f7c9d401'
down_revision = '90b8f8b2a562'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('plan_definitions',
        sa.Column('archived', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('questionnaires',
        sa.Column('archived', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('form_definitions',
        sa.Column('archived', sa.Boolean(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('form_definitions', 'archived')
    op.drop_column('questionnaires', 'archived')
    op.drop_column('plan_definitions', 'archived')
