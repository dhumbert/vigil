"""Question group order

Revision ID: 30dccaa4af9e
Revises: 104fc2d80a6b
Create Date: 2015-11-25 14:43:37.213361

"""

# revision identifiers, used by Alembic.
revision = '30dccaa4af9e'
down_revision = '104fc2d80a6b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('question_groups',
                  sa.Column('order', sa.Integer(), nullable=True))

    connection = op.get_bind()
    question_groups = sa.Table('question_groups', sa.MetaData(), autoload=True, autoload_with=connection)
    group_query = question_groups.select()
    order = 2
    for group in connection.execute(group_query).fetchall():
        if group.name == "Burn's Depression Checklist":
            t_order = 1
        else:
            t_order = order
            order += 1

        connection.execute(
            question_groups.update().where(question_groups.c.id == group['id']).values(order=t_order)
        )


def downgrade():
    op.drop_column('question_groups', 'order')
