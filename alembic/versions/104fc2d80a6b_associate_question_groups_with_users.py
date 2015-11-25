"""Associate question groups with users

Revision ID: 104fc2d80a6b
Revises: 511b2900ed4a
Create Date: 2015-11-25 14:26:53.199776

"""

# revision identifiers, used by Alembic.
revision = '104fc2d80a6b'
down_revision = '511b2900ed4a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    connection = op.get_bind()
    # by default, all question groups will be initially owned by ME! YAY!
    users = sa.Table('users', sa.MetaData(), autoload=True, autoload_with=connection)
    user_query = users.select().where(users.c.username == 'devin')
    found_user = connection.execute(user_query).first()['id']

    op.add_column('question_groups',
                  sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True))

    # burns score user_id will be kept NULL, which means it will be for all users
    # the users will be assigned
    question_groups = sa.Table('question_groups', sa.MetaData(), autoload=True, autoload_with=connection)
    group_query = question_groups.select().where(question_groups.c.name != "Burn's Depression Checklist")
    for group in connection.execute(group_query).fetchall():
        connection.execute(
            question_groups.update().where(question_groups.c.id == group['id']).values(user_id=found_user)
        )


def downgrade():
    op.drop_column('question_groups', 'user_id')
