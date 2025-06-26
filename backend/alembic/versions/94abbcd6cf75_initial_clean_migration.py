# Migration script to create the five required tables

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import String, Integer, DateTime

# revision identifiers, used by Alembic.
revision = '94abbcd6cf75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the "user" table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('preferences', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_preferences', 'user', ['preferences'], unique=False)

    # Create the "session" table
    op.create_table(
        'session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_token', sa.String(), nullable=False),
        sa.Column('login_time', sa.DateTime(), nullable=False),
        sa.Column('logout_time', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_session_user_id', 'session', ['user_id'], unique=False)
    op.create_index('ix_session_session_token', 'session', ['session_token'], unique=True)

    # Create the "job" table
    op.create_table(
        'job',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('job_name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_user_id', 'job', ['user_id'], unique=False)
    op.create_index('ix_job_job_name', 'job', ['job_name'], unique=False)
    op.create_index('ix_job_status', 'job', ['status'], unique=False)

    # Create the "file" table
    op.create_table(
        'file',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('uploaded_time', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_file_user_id', 'file', ['user_id'], unique=False)
    op.create_index('ix_file_file_name', 'file', ['file_name'], unique=False)

    # Create the "result" table
    op.create_table(
        'result',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('sharing_permission', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_result_user_id', 'result', ['user_id'], unique=False)
    op.create_index('ix_result_job_id', 'result', ['job_id'], unique=False)
    op.create_index('ix_result_file_name', 'result', ['file_name'], unique=False)


def downgrade() -> None:
    # In case we want to undo the migration and remove the tables in the future
    op.drop_table('result')
    op.drop_table('file')
    op.drop_table('job')
    op.drop_table('session')
    op.drop_table('user')




