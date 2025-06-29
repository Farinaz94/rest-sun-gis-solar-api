"""Add session table

Revision ID: 2889197397c1
Revises: your_revision_id
Create Date: 2025-06-29 14:48:55.764834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2889197397c1'
down_revision: Union[str, None] = 'your_revision_id'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('invalidated_by_admin', sa.Boolean(), nullable=False, server_default=sa.text('false'))
    )


    
def downgrade() -> None:
    op.drop_table('session')

