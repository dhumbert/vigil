from datetime import datetime, timedelta
from flask import flash, render_template, request, redirect, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user
import json
from vigil import app, model, utils, content_type


@app.route("/")
@login_required
def index():
    today = datetime.now().strftime(app.config['DATE_FORMAT'])
    return redirect(url_for('day_view', day=today))


@app.route("/day/<day>", methods=['GET', 'POST'])
@login_required
def day_view(day):
    day_datetime = datetime.strptime(day, app.config['DATE_FORMAT'])
    if request.method == 'POST':
        answers = [(x.replace('question_', ''), request.form[x],) for x in request.form if x[0:8] =='question']
        model.save_answers(current_user, day_datetime, answers)
        flash('success', 'Saved!')
        return redirect(url_for('day_view', day=day))

    user_answers = model.get_answers(current_user, day_datetime)
    burns_score = model.get_burns_score(current_user, day_datetime)
    groups = model.QuestionGroup.query.all()
    prev_day, next_day = utils.bracketing_days(day_datetime)

    edit = False
    if ('edit' in request.args and request.args['edit'] == 'true') or not user_answers:
        edit = True

    template = 'edit.html' if edit else 'view.html'

    return render_template(template, groups=groups, day=day_datetime, user_answers=user_answers,
                           burns_score=burns_score, day_raw=day,
                           prev_day=prev_day, next_day=next_day)


@app.route("/ajax/burns")
@login_required
@content_type("application/json")
def ajax_burns():
    current_date = request.args.get('date', None)
    if current_date:
        current_date_datetime = datetime.strptime(current_date, app.config['DATE_FORMAT'])
    else:
        current_date_datetime = datetime.now()

    return json.dumps(model.get_all_burns_scores(current_user, current_date_datetime))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = model.authenticate(request.form['username'], request.form['password'])
        if user:
            login_user(user, remember=True)
            url = request.form['next'] if 'next' in request.form else '/'
            return redirect(url)
        else:
            flash('Invalid login', 'error')
            return redirect('/login')
    return render_template('login.html', next=request.args.get('next'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/login')
