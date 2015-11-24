"""Added sailing to activities

Revision ID: 2d2bd87323d2
Revises: 28070f013813
Create Date: 2015-11-23 21:31:48.376336

"""

# revision identifiers, used by Alembic.
revision = '2d2bd87323d2'
down_revision = '28070f013813'

from alembic import op
import sqlalchemy as sa


def upgrade():
    connection = op.get_bind()
    questions = sa.Table('questions', sa.MetaData(), autoload=True, autoload_with=connection)
    question_groups = sa.Table('question_groups', sa.MetaData(), autoload=True, autoload_with=connection)
    question_answers = sa.Table('question_answers', sa.MetaData(), autoload=True, autoload_with=connection)

    yes_no_opts = [(0, 'No', 0,), (1, 'Yes', 1,)]

    group_query = question_groups.select().where(question_groups.c.name == 'Activities')
    found_group = connection.execute(group_query).first()

    activities_group_id = found_group.id
    q_order = 16
    for activity_question in ['Sailing']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=activities_group_id, prompt=activity_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1


def downgrade():
    pass
