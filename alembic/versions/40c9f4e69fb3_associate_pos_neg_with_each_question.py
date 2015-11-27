"""associate pos/neg with each question

Revision ID: 40c9f4e69fb3
Revises: 30dccaa4af9e
Create Date: 2015-11-26 20:39:55.595681

"""

# revision identifiers, used by Alembic.
revision = '40c9f4e69fb3'
down_revision = '30dccaa4af9e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('questions',
                  sa.Column('positive', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('questions', 'positive')
