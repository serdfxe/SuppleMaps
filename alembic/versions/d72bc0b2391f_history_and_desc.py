"""history_and_desc

Revision ID: d72bc0b2391f
Revises: 1d9013cda183
Create Date: 2023-02-03 22:39:43.996208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72bc0b2391f'
down_revision = '1d9013cda183'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('poi', sa.Column('description', sa.String(length=7000), nullable=True))
    op.add_column('poi', sa.Column('history', sa.String(length=20000), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('poi', 'history')
    op.drop_column('poi', 'description')
    # ### end Alembic commands ###
