"""add form_definitions and form_definition_items

Revision ID: 90b8f8b2a562
Revises: dcc76e2d3060
Create Date: 2026-03-26 19:15:37.583979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b8f8b2a562'
down_revision = 'dcc76e2d3060'
branch_labels = None
depends_on = None


def upgrade():
    # Create form_definitions table
    op.create_table('form_definitions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('guid', sa.String(36), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='draft'),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('vers_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('produced_form_guid', sa.String(36), nullable=True),
        sa.Column('production_key', sa.String(255), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('date_updated', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guid'),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_form_definitions_guid', 'form_definitions', ['guid'])

    # Create form_definition_items table
    op.create_table('form_definition_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('guid', sa.String(36), nullable=False),
        sa.Column('form_definition_id', sa.Integer(), nullable=False),
        sa.Column('concept_guid', sa.String(36), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('required', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('label_override', sa.String(500), nullable=True),
        sa.Column('help_text', sa.Text(), nullable=True),
        sa.Column('date_created', sa.DateTime(), nullable=False),
        sa.Column('date_updated', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['form_definition_id'], ['form_definitions.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guid'),
    )
    op.create_index('ix_form_definition_items_guid', 'form_definition_items', ['guid'])

    # Add form_definition_guid column to plan_definitions
    op.add_column('plan_definitions',
        sa.Column('form_definition_guid', sa.String(36), nullable=True))


def downgrade():
    op.drop_column('plan_definitions', 'form_definition_guid')
    op.drop_index('ix_form_definition_items_guid', table_name='form_definition_items')
    op.drop_table('form_definition_items')
    op.drop_index('ix_form_definitions_guid', table_name='form_definitions')
    op.drop_table('form_definitions')
