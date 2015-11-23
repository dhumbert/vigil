from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('vigil.config')
app.config.from_pyfile('application.cfg')

crypt = Bcrypt(app)
db = SQLAlchemy(app)

login = LoginManager()
login.init_app(app, add_context_processor=True)
login.login_view = "login"


@login.user_loader
def load_user(id):
    from vigil.model import User
    return User.query.get(int(id))


import views