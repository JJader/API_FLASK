"""empty message

Revision ID: 0870443f2bef
Revises: 564a8b1b1317
Create Date: 2020-02-20 00:34:01.124233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0870443f2bef'
down_revision = '564a8b1b1317'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'pontos', 'alunos', ['id_aluno'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pontos', type_='foreignkey')
    # ### end Alembic commands ###