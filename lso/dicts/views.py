from flask import render_template

from . import dicts

@dicts.route('/')
def index():
    return render_template('dicts/index.html')

@dicts.route('/mw/')
def mw():
    return render_template('dicts/mw/index.html')
