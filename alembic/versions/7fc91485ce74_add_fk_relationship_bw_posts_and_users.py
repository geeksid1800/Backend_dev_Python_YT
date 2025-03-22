"""add FK relationship bw posts and users

Revision ID: 7fc91485ce74
Revises: a7b4fb25c21b
Create Date: 2025-03-20 16:40:28.336306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey, Column, Integer

# revision identifiers, used by Alembic.
revision = '7fc91485ce74'
down_revision = 'a7b4fb25c21b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', Column('user_id', Integer, nullable=False))
    op.create_foreign_key('posts_user_fk', source_table ='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_user_fk', table_name = 'posts')
    op.drop_column('posts', 'user_id')
    pass
