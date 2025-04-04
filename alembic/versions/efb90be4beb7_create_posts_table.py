"""create posts table

Revision ID: efb90be4beb7
Revises: 
Create Date: 2025-03-18 16:19:08.346234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efb90be4beb7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
    sa.Column('title', sa.String, nullable=False)
    )
    pass

def downgrade():
    op.drop_table('posts')
    pass