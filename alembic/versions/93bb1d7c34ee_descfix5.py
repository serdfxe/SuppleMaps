"""DescFix5

Revision ID: 93bb1d7c34ee
Revises: 1cc8c5f42e48
Create Date: 2023-01-29 22:50:46.132011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93bb1d7c34ee'
down_revision = '1cc8c5f42e48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('poi_description_key', 'poi', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('poi_description_key', 'poi', ['description'])
    # ### end Alembic commands ###
