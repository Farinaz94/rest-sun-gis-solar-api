"""Add groups column to user

Revision ID: 4721e5c88a9e
Revises: 93e670e51e55
Create Date: 2025-06-28 10:39:41.857513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import json


# revision identifiers, used by Alembic.
revision = 'your_revision_id'
down_revision = '93e670e51e55'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user',
        sa.Column('groups', postgresql.JSON(astext_type=sa.Text()), nullable=True)
    )


    conn = op.get_bind()
    conn.execute(
        sa.text("""
            UPDATE "user"
            SET groups = :groups
            WHERE username = :username
        """),
        [{"groups": json.dumps(["solar_team"]), "username": "admin"}]
    )



def downgrade():
    op.drop_column('user', 'groups')
