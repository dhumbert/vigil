from functools import wraps
from flask import Flask, make_response
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


def content_type(content_type):
    """Adds Content-type header to requests"""
    def decorator(func):
        @wraps(func)
        def do_output(*args, **kwargs):
            response = make_response(func(*args, **kwargs))
            response.headers['Content-type'] = content_type
            return response
        return do_output
    return decorator


import views