"""create story table

Revision ID: 661dcc8c7420
Revises:
Create Date: 2016-10-04 15:12:20.559483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '661dcc8c7420'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('story',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(140), nullable=False),
    sa.Column('author', sa.String(140), nullable=False),
    sa.Column('description', sa.String(140), nullable=False),
    sa.Column('text_uri', sa.String(1000), nullable=False),
    sa.Column('audio_uri', sa.String(1000), nullable=False)
    )


def downgrade():
    pass
