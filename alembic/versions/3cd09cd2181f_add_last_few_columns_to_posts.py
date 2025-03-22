"""add last few columns to posts

Revision ID: 3cd09cd2181f
Revises: 7fc91485ce74
Create Date: 2025-03-21 17:59:08.187392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cd09cd2181f'
down_revision = '7fc91485ce74'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='True', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
