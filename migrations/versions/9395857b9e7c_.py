"""empty message

Revision ID: 9395857b9e7c
Revises: a61dbd85b472
Create Date: 2020-10-22 14:50:39.611494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9395857b9e7c'
down_revision = 'a61dbd85b472'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centros', sa.Column('protocolo', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('centros', 'protocolo')
    # ### end Alembic commands ###
