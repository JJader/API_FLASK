"""empty message

Revision ID: 5e0bbe07ffda
Revises: 4f7200b17595
Create Date: 2020-02-23 01:49:55.951508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e0bbe07ffda'
down_revision = '4f7200b17595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chegada', sa.Column('status', sa.Integer(), nullable=False))
    op.alter_column('chegada', 'lat',
               existing_type=sa.FLOAT(),
               nullable=False)
    op.alter_column('chegada', 'lon',
               existing_type=sa.FLOAT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chegada', 'lon',
               existing_type=sa.FLOAT(),
               nullable=True)
    op.alter_column('chegada', 'lat',
               existing_type=sa.FLOAT(),
               nullable=True)
    op.drop_column('chegada', 'status')
    # ### end Alembic commands ###
