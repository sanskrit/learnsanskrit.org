from flask import render_template

from lso import app
from lso.database import session


@app.teardown_request
def remove_session(exception=None):
    session.remove()


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
