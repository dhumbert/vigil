#!/usr/bin/env python2.7
from flask.ext.script import Manager
from flask.ext.alembic import ManageMigrations
from vigil import app, crypt


manager = Manager(app)
manager.add_command("migrate", ManageMigrations())


@manager.command
def debug():
    """ Run the server in debug mode"""
    app.run('0.0.0.0', debug=True, threaded=True)


@manager.command
def hash(string):
    print crypt.generate_password_hash(string)


if __name__ == "__main__":
    manager.run()
