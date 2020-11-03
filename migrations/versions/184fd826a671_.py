"""empty message

Revision ID: 184fd826a671
Revises: eb0f0004d73d
Create Date: 2020-11-02 21:35:34.393926

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '184fd826a671'
down_revision = 'eb0f0004d73d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centros', sa.Column('lat', sa.String(length=15), nullable=True))
    op.add_column('centros', sa.Column('lng', sa.String(length=15), nullable=True))
    op.drop_column('centros', 'coordenadas')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('centros', sa.Column('coordenadas', mysql.VARCHAR(collation='latin1_spanish_ci', length=40), nullable=True))
    op.drop_column('centros', 'lng')
    op.drop_column('centros', 'lat')
    # ### end Alembic commands ###
