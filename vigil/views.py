from datetime import datetime, timedelta
from flask import flash, render_template, request, redirect, url_for
from flask.ext.login import current_user, login_required, login_user, logout_user
from vigil import app, model, utils


@app.route("/")
@login_required
def index():
    today = datetime.now().strftime(app.config['DATE_FORMAT'])
    return redirect(url_for('edit', day=today))


@app.route("/view/<day>", methods=['GET', 'POST'])
@login_required
def view(day):
    pass


@app.route("/edit/<day>", methods=['GET', 'POST'])
@login_required
def edit(day):
    day_datetime = datetime.strptime(day, app.config['DATE_FORMAT'])
    if request.method == 'POST':
        answers = [(x.replace('question_', ''), request.form[x],) for x in request.form if x[0:8] =='question']
        model.save_answers(current_user, day_datetime, answers)
        flash('success', 'Saved!')
        return redirect(url_for('edit', day=day))

    user_answers = model.get_answers(current_user, day_datetime)
    groups = model.QuestionGroup.query.all()
    prev_day, next_day = utils.bracketing_days(day_datetime)
    return render_template('edit.html', groups=groups, day=day_datetime, user_answers=user_answers,
                           prev_day=prev_day, next_day=next_day)


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
