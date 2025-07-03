"""add location, mapset, and session_id to file

Revision ID: 888e7cdd73a6
Revises: c5f50f796a74
Create Date: 2025-07-02 21:08:22.612485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect
from alembic.runtime.migration import MigrationContext

# revision identifiers, used by Alembic.
revision: str = '888e7cdd73a6'
down_revision: Union[str, None] = 'c5f50f796a74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def has_column(table_name, column_name):
    bind = op.get_bind()
    insp = inspect(bind)
    return column_name in [col["name"] for col in insp.get_columns(table_name)]

def upgrade() -> None:
    # Only try to add columns if they don’t already exist
    with op.batch_alter_table("file") as batch_op:
        if not has_column("file", "session_id"):
            batch_op.add_column(sa.Column("session_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_file_session", "session", ["session_id"], ["id"]
            )


def downgrade() -> None:
    with op.batch_alter_table("file") as batch_op:
        batch_op.drop_constraint("fk_file_session", type_="foreignkey")
        batch_op.drop_column("session_id")

