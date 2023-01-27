"""Graph1

Revision ID: 630f4b964499
Revises: 6fb0e69725c5
Create Date: 2023-01-27 21:46:28.247643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '630f4b964499'
down_revision = '6fb0e69725c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poi',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lon', sa.Float(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('distance_list',
    sa.Column('start_id', sa.Integer(), nullable=False),
    sa.Column('end_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['end_id'], ['poi.id'], ),
    sa.ForeignKeyConstraint(['start_id'], ['poi.id'], ),
    sa.PrimaryKeyConstraint('start_id', 'end_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('distance_list')
    op.drop_table('poi')
    # ### end Alembic commands ###