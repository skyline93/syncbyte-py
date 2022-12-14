"""4

Revision ID: b07c3f9ccb5f
Revises: 80d7aa98ca72
Create Date: 2022-09-12 14:15:39.230972

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b07c3f9ccb5f'
down_revision = '80d7aa98ca72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('backup_job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('is_valid', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.Column('storage_id', sa.Integer(), nullable=True),
    sa.Column('dataset_name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sync_job')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sync_job',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='sync_job_pkey')
    )
    op.drop_table('backup_job')
    # ### end Alembic commands ###
