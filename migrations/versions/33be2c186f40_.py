"""empty message

Revision ID: 33be2c186f40
Revises: 61578e56bd11
Create Date: 2020-02-19 23:55:08.756989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33be2c186f40'
down_revision = '61578e56bd11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alunos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('idade', sa.Integer(), nullable=False),
    sa.Column('escola', sa.String(length=100), nullable=False),
    sa.Column('turno', sa.String(length=100), nullable=False),
    sa.Column('presenca', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alunos')
    # ### end Alembic commands ###
