"""add last_login

Revision ID: 2024_12_27_add_last_login
Revises: 2024_12_27_add_admin
Create Date: 2024-12-27 14:40:35.892766

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2024_12_27_add_last_login'
down_revision = '2024_12_27_add_admin'
branch_labels = None
depends_on = None

def upgrade():
    # Add last_login column to users table
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('last_login', sa.Date(), nullable=True))

def downgrade():
    # Remove last_login column from users table
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('last_login')
