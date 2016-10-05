"""rename audio text to link

Revision ID: 58744e4e0faf
Revises: e68ccabaf982
Create Date: 2016-10-05 12:02:04.760863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58744e4e0faf'
down_revision = 'e68ccabaf982'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('audio', 'text_uri', new_column_name='link_uri')

def downgrade():
    pass
