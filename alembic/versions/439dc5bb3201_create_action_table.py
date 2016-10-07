"""create action table

Revision ID: 439dc5bb3201
Revises: 3da61acff321
Create Date: 2016-10-06 13:53:53.594275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '439dc5bb3201'
down_revision = '3da61acff321'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('action',
        sa.Column('type', sa.String(10), nullable=False),
        sa.Column('audio_point', sa.Integer, nullable=False),
        sa.Column('timestamp', sa.Date, nullable=False),
        sa.Column('audio_id', sa.Integer, sa.ForeignKey('audio.id'), nullable=False),
        sa.Column('client_id', sa.Integer, nullable=False),
        sa.Column('id', sa.Integer, primary_key=True)
    )


def downgrade():
    pass
