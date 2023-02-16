"""Broccol migration

Revision ID: ab0d3a2f7bf3
Revises: 7c10fab9d9d8
Create Date: 2023-02-16 20:19:58.928085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab0d3a2f7bf3'
down_revision = '7c10fab9d9d8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('saved_paths_name_key', 'saved_paths', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('saved_paths_name_key', 'saved_paths', ['name'])
    # ### end Alembic commands ###
