"""create advertisement table

Revision ID: 848fa2d9976d
Revises: 3c6403debfaa
Create Date: 2021-06-24 11:24:21.880350

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '848fa2d9976d'
down_revision = '3c6403debfaa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'advertisement',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(64), index=True, unique=True, nullable=False),
        sa.Column('description', sa.Text, index=True, nullable=False, default=''),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey('user.id')),
        sa.Column('created_on', sa.DateTime(), default=datetime.utcnow)
    )


def downgrade():
    op.drop_table('advertisement')
