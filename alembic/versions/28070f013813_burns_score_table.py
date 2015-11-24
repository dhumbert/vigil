"""burns score table

Revision ID: 28070f013813
Revises: 2575eb4f78c1
Create Date: 2015-11-23 14:26:02.661726

"""

# revision identifiers, used by Alembic.
revision = '28070f013813'
down_revision = '2575eb4f78c1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user_burns_score',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('burns_score', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'date')
    )


def downgrade():
    op.drop_table('user_burns_score')
