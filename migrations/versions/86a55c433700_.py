"""empty message

Revision ID: 86a55c433700
Revises: 04cfb38e0d24
Create Date: 2020-02-20 00:16:41.453640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86a55c433700'
down_revision = '04cfb38e0d24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('alunos', 'presenca',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('pontos', sa.Column('id_aluno', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'pontos', 'alunos', ['id_aluno'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'pontos', type_='foreignkey')
    op.drop_column('pontos', 'id_aluno')
    op.alter_column('alunos', 'presenca',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
