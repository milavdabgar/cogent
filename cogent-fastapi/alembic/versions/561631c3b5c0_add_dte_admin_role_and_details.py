"""add_dte_admin_role_and_details

Revision ID: 561631c3b5c0
Revises: 2024_12_27_add_last_login
Create Date: 2024-12-27 19:41:52.866988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '561631c3b5c0'
down_revision: Union[str, None] = '2024_12_27_add_last_login'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_alembic_tmp_users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), nullable=True),
    sa.Column('date_of_birth', sa.DATE(), nullable=True),
    sa.Column('role', sa.VARCHAR(length=13), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('last_login', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
