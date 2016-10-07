"""create context table

Revision ID: 3da61acff321
Revises: 58744e4e0faf
Create Date: 2016-10-06 00:13:32.322049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da61acff321'
down_revision = '58744e4e0faf'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('context',
        sa.Column('type', sa.String(10)),
        sa.Column('audio_id', sa.Integer, sa.ForeignKey('audio.id', ondelete='CASCADE')),
        sa.Column('time_start', sa.Integer, sa.CheckConstraint('time_start > -1')),
        sa.Column('time_end', sa.Integer, nullable=False),
        sa.Column('link_uri', sa.String(1000)),
        sa.Column('img_uri', sa.String(1000)),
        sa.Column('text', sa.String(140)),
        sa.CheckConstraint('time_end > time_start')
    )
    op.create_primary_key('pk_context', 'context',
                          ['type', 'audio_id', 'time_start']
    )

def downgrade():
    pass
