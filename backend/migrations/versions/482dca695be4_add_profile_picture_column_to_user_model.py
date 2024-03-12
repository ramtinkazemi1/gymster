"""Add profile_picture column to User model

Revision ID: 482dca695be4
Revises: 276b67ebc0de
Create Date: 2024-03-11 14:10:09.031875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482dca695be4'
down_revision = '276b67ebc0de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))
        batch_op.alter_column('user_type',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=10),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('user_type',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###