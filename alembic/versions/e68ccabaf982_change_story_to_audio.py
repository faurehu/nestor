"""Change story to audio

Revision ID: e68ccabaf982
Revises: 661dcc8c7420
Create Date: 2016-10-05 11:53:17.602410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e68ccabaf982'
down_revision = '661dcc8c7420'
branch_labels = None
depends_on = None

def upgrade():
    op.rename_table('story', 'audio')
    op.add_column('audio', sa.Column('type', sa.String(10), nullable=False))


def downgrade():
    pass
