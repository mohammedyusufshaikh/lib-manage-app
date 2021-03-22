"""empty message

Revision ID: 38c7f4782de7
Revises: 621d51d582ff
Create Date: 2021-03-19 17:45:21.688318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c7f4782de7'
down_revision = '621d51d582ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('book_status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'book_status')
    # ### end Alembic commands ###
