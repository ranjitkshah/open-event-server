"""empty message

Revision ID: 6b3498cc0457
Revises: 3f0ae16c8c11
Create Date: 2021-06-22 04:39:20.072925

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '6b3498cc0457'
down_revision = '3f0ae16c8c11'


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_group_user', 'user_follow_groups', ['group_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_group_user', 'user_follow_groups', type_='unique')
    # ### end Alembic commands ###
