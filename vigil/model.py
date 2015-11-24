from flask.ext.sqlalchemy import SessionBase
import time

from vigil import db, crypt


class QuestionGroup(db.Model):
    __tablename__ = 'question_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    questions = db.relationship('Question', backref=db.backref('group'))

    @property
    def active_questions(self):
        return SessionBase.object_session(self).query(Question).with_parent(self).filter(Question.active==True).order_by(Question.order).all()

    @property
    def ordered_questions(self):
        return SessionBase.object_session(self).query(Question).with_parent(self).order_by(Question.order).all()


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_group_id = db.Column(db.Integer, db.ForeignKey('question_groups.id'))
    prompt = db.Column(db.String)
    active = db.Column(db.Boolean)
    order = db.Column(db.Integer)

    answers = db.relationship('Answer')

    @property
    def ordered_answers(self):
        return SessionBase.object_session(self).query(Answer).with_parent(self).order_by(Answer.order).all()


class Answer(db.Model):
    __tablename__ = 'question_answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    text = db.Column(db.String)
    value = db.Column(db.Integer)
    order = db.Column(db.Integer)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        self.password = crypt.generate_password_hash(password)

    def __repr__(self):
        return unicode(self.username)


class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    question_answer_id = db.Column(db.Integer, db.ForeignKey('question_answers.id'))
    date = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('answers'))
    question = db.relationship('Question')
    answer = db.relationship('Answer')

    def __repr__(self):
        return self.date.strftime("%Y-%m-%d") + " - " + str(self.question_id)


class UserBurnsScore(db.Model):
    __tablename__ = 'user_burns_score'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    burns_score = db.Column(db.Integer)
    user = db.relationship('User')

    def for_display(self):
        if self.burns_score <= 5:
            status = "success"
            description = "No depression"
        elif self.burns_score <= 10:
            status = "warning"
            description = "Normal but unhappy"
        elif self.burns_score <= 25:
            status = "warning"
            description = "Mild depression"
        elif self.burns_score <= 50:
            status = "danger"
            description = "Moderate depression"
        elif self.burns_score <= 75:
            status = "danger"
            description = "Severe depression"
        else:
            status = "danger"
            description = "Extreme depression"

        return {"status": status, "description": description}


def authenticate(username, password):
    user = db.session.query(User).filter(User.username==username).first()
    if user and crypt.check_password_hash(user.password, password):
        return user

    return None


def save_answers(user, date, answers):
    # delete existing
    UserAnswer.query.filter_by(date=date, user_id=user.id).delete()

    for question_id, answer_id in answers:
        user_answer = UserAnswer()
        user_answer.user = user
        user_answer.question_id = question_id
        user_answer.question_answer_id = answer_id
        user_answer.date = date
        db.session.add(user_answer)

    db.session.commit()

    save_burns_score(user, date)


def get_answers(user, day_datetime):
    answers = UserAnswer.query.filter_by(date=day_datetime, user_id=user.id)

    return {a.question_id: a for a in answers}


def get_burns_score(user, day_datetime):
    return UserBurnsScore.query.filter_by(date=day_datetime, user_id=user.id).first()


def get_all_burns_scores(user):
    scores = []
    for score in UserBurnsScore.query.filter_by(user_id=user.id).order_by(UserBurnsScore.date).all():
        scores.append({'x': int(time.mktime(score.date.timetuple())) * 1000, 'y': score.burns_score})

    return scores


def save_burns_score(user, date):
    questions = QuestionGroup.query.filter(QuestionGroup.name == "Burn's Depression Checklist").first().questions

    score = 0
    for question in questions:
        user_answer = UserAnswer.query.filter(UserAnswer.question_id==question.id, UserAnswer.date==date).first()
        if user_answer:
            score += user_answer.answer.value

    UserBurnsScore.query.filter_by(date=date, user_id=user.id).delete()

    user_score = UserBurnsScore()
    user_score.user = user
    user_score.burns_score = score
    user_score.date = date
    db.session.add(user_score)

    db.session.commit()
