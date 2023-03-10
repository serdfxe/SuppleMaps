"""PoiType2

Revision ID: ccfa173825e9
Revises: 81950d3a575b
Create Date: 2023-01-29 21:23:56.356202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccfa173825e9'
down_revision = '81950d3a575b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('poi', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'poi', 'poi_type', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'poi', type_='foreignkey')
    op.drop_column('poi', 'type_id')
    # ### end Alembic commands ###
