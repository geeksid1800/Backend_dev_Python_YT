"""create column content to posts table'


Revision ID: 7bae3080fe6d
Revises: efb90be4beb7
Create Date: 2025-03-18 17:11:24.788844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bae3080fe6d'
down_revision = 'efb90be4beb7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False)
    )
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
