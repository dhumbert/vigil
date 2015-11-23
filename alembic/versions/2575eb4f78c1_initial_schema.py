"""Initial Schema

Revision ID: 2575eb4f78c1
Revises: None
Create Date: 2015-11-23 09:35:34.436636

"""

# revision identifiers, used by Alembic.
revision = '2575eb4f78c1'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer()),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('question_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=False),
        sa.Column('question_group_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), default=True, server_default='true'),
        sa.ForeignKeyConstraint(['question_group_id'], ['question_groups.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('question_answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('user_answers',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('question_answer_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.ForeignKeyConstraint(['question_answer_id'], ['question_answers.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'question_id', 'date')
    )

    # now insert some data
    connection = op.get_bind()
    users = sa.Table('users', sa.MetaData(), autoload=True, autoload_with=connection)
    ins = users.insert().values(id=1, username='devin', password='$2b$12$ZLvdp1jKPhxOdsLF9wtm8eEu/25rpwLCSKqWkIhd9v8.MoKrxH9Ye')
    connection.execute(ins)

    question_groups = sa.Table('question_groups', sa.MetaData(), autoload=True, autoload_with=connection)
    burns_group_id = connection.execute(question_groups.insert().values(name="Burn's Depression Checklist")).inserted_primary_key[0]

    questions = sa.Table('questions', sa.MetaData(), autoload=True, autoload_with=connection)
    question_answers = sa.Table('question_answers', sa.MetaData(), autoload=True, autoload_with=connection)

    burns_questions = [
        'Feeling sad or down in the dumps',
        'Feeling unhappy or blue',
        'Crying spells or tearfulness',
        'Feeling discouraged',
        'Feeling hopeless',
        'Low self-esteem',
        'Feeling worthless or inadequate',
        'Guilt or shame',
        'Criticizing yourself or blaming others',
        'Difficulty making decisions',
        'Loss of interest in family, friends, or colleagues',
        'Loneliness',
        'Spending less time with family or friends',
        'Loss of motivation',
        'Loss of interest in work or other activities',
        'Avoiding work or other activities',
        'Loss of pleasure or satisfaction in life',
        'Feeling tired',
        'Difficulty sleeping or sleeping too much',
        'Decreased or increased appetite',
        'Loss of interest in sex',
        'Worrying about your health',
        'Do you have any suicidal thoughts?',
        'Would you like to end your life?',
        'Do you have a plan for harming yourself?',
    ]

    burns_opts = [(0, 'Not At All',), (1, 'Somewhat',), (2, 'Moderately',), (3, 'A Lot',), (4, 'Extremely',)]

    q_order = 0
    for burns_question in burns_questions:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=burns_group_id, prompt=burns_question)).inserted_primary_key[0]
        opt_order = 0
        for burns_opt in burns_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, text=burns_opt[1], value=burns_opt[0], order=opt_order))
            opt_order += 1
        q_order += 1

    yes_no_opts = [(0, 'No', 0,), (1, 'Yes', 1,)]

    weather_group_id = connection.execute(question_groups.insert().values(name="Weather")).inserted_primary_key[0]
    q_order = 0
    for weather_question in ['Hot', 'Cold', 'Sunny', 'Cloudy']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=weather_group_id, prompt=weather_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1

    health_group_id = connection.execute(question_groups.insert().values(name="Health")).inserted_primary_key[0]
    q_order = 0
    for health_question in ['Exercised', 'Meditated', 'Ate Healthy', 'Slept In', 'Fast Food', 'Vaped', 'Smoked', 'Alcohol', 'Modafinil', 'Other Drugs']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=health_group_id, prompt=health_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1

    emotions_group_id = connection.execute(question_groups.insert().values(name="Emotions")).inserted_primary_key[0]
    q_order = 0
    for emotion_question in ['Anger', 'Sadness', 'Depression', 'Joy', 'Optimism', 'Pessimism', 'Hopelessness', 'Frustrated', 'Jealousy', 'Apathy', 'Nostalgia', 'Loneliness']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=emotions_group_id, prompt=emotion_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1

    thoughts_group_id = connection.execute(question_groups.insert().values(name="Thoughts")).inserted_primary_key[0]
    q_order = 0
    for thought_question in ['Existential Depression', 'Quitting Job', 'Living in RV/Boat', 'Buying House', 'Moving', 'Purpose', 'Weight Anxiety', 'Desire to be Social']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=thoughts_group_id, prompt=thought_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1

    activities_group_id = connection.execute(question_groups.insert().values(name="Activities")).inserted_primary_key[0]
    q_order = 0
    for activity_question in ['Quality time with Alyssa', 'Time with friends', 'Was productive', 'Programming', 'Reading', 'Got outside', 'Time in nature', 'Cleaned', 'Organized', 'Watched a lot of TV', 'Journaled', 'Worked (Job)', 'Traveled', 'Fixed something', 'Made decision according to values or goals', 'Made decision contrary to values or goals']:
        q_id = connection.execute(questions.insert().values(order=q_order, question_group_id=activities_group_id, prompt=activity_question)).inserted_primary_key[0]
        for yes_no_opt in yes_no_opts:
            connection.execute(question_answers.insert().values(question_id=q_id, order=yes_no_opt[2], text=yes_no_opt[1], value=yes_no_opt[0]))
        q_order += 1


def downgrade():
    op.drop_table('user_answers')
    op.drop_table('question_answers')
    op.drop_table('questions')
    op.drop_table('question_groups')
    op.drop_table('users')
