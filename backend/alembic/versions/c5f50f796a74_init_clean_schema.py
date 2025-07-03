"""init clean schema

Revision ID: c5f50f796a74
Revises: 
Create Date: 2025-07-02 18:38:15.522664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c5f50f796a74'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, index=True, unique=True),
        sa.Column('role', sa.String(), nullable=False, index=True, default="user"),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('groups', sa.JSON(), nullable=True),
    )

    op.create_table(
        'session',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('session_token', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('login_time', sa.DateTime(), nullable=False),
        sa.Column('logout_time', sa.DateTime(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('invalidated_by_admin', sa.Boolean(), nullable=False, default=False),
    )

    op.create_table(
        'file',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('file_name', sa.String(), nullable=False, index=True),
        sa.Column('uploaded_time', sa.DateTime(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=True),
        sa.Column('format', sa.String(), nullable=True),
        sa.Column('epsg', sa.Integer(), nullable=True),
        sa.Column('valid', sa.Boolean(), nullable=False, default=True),
    )

    op.create_table(
        'job',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('job_name', sa.String(), nullable=False, index=True),
        sa.Column('status', sa.String(), nullable=False, index=True),
    )

    op.create_table(
        'result',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('job_id', sa.Integer(), nullable=False, index=True),
        sa.Column('file_name', sa.String(), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('sharing_permission', sa.String(), nullable=False, default="private"),
    )


def downgrade() -> None:
    op.drop_table('result')
    op.drop_table('job')
    op.drop_table('file')
    op.drop_table('session')
    op.drop_table('user')