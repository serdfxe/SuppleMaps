"""Graph_finally_2

Revision ID: 31420ec9fbba
Revises: b2a2d3f5acb6
Create Date: 2023-01-27 22:59:23.738318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31420ec9fbba'
down_revision = 'b2a2d3f5acb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('distance_list', sa.Column('distance', sa.Integer(), nullable=False))
    op.drop_column('distance_list', 'time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('distance_list', sa.Column('time', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('distance_list', 'distance')
    # ### end Alembic commands ###
