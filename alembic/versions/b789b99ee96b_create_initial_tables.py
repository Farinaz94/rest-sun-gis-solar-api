"""create initial tables

Revision ID: b789b99ee96b
Revises: 
Create Date: 2025-06-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b789b99ee96b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Example tables — edit or add your own below
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    # Add more table creation blocks here if needed
    # DO NOT drop any PostGIS Tiger tables!


def downgrade():
    op.drop_table('projects')
    op.drop_table('users')
