"""empty message

Revision ID: f289fa9436d1
Revises: faf2dbe4efc3
Create Date: 2021-03-25 19:44:22.569475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f289fa9436d1'
down_revision = 'faf2dbe4efc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('issue_date', sa.Date(), nullable=True))
    op.add_column('transactions', sa.Column('return_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'return_date')
    op.drop_column('transactions', 'issue_date')
    # ### end Alembic commands ###