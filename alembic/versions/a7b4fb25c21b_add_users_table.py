"""add users table

Revision ID: a7b4fb25c21b
Revises: 7bae3080fe6d
Create Date: 2025-03-18 17:49:14.165835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

# revision identifiers, used by Alembic.
revision = 'a7b4fb25c21b'
down_revision = '7bae3080fe6d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, nullable=False),
        Column('email', String, unique=True, nullable=False),
        Column('password', String, nullable=False),
        Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
