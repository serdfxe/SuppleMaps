"""Broccol migration

Revision ID: 7db1fb9cb7e6
Revises: cdcc4be364b9
Create Date: 2023-02-20 20:45:56.738823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7db1fb9cb7e6'
down_revision = 'cdcc4be364b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saved_paths')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saved_paths',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=5000), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('path', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('length', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('full_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('walk_time', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='saved_paths_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='saved_paths_pkey')
    )
    # ### end Alembic commands ###