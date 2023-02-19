"""Broccol migration

Revision ID: 945d55e48f5d
Revises: 84b9ec380a60
Create Date: 2023-02-19 20:00:47.925532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '945d55e48f5d'
down_revision = '84b9ec380a60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('history', 'id')
    # ### end Alembic commands ###
