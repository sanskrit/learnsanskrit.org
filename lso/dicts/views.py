from flask import render_template

from lso.forms import QueryForm
from . import dicts

@dicts.route('/')
def index():
    return render_template('dicts/index.html')

@dicts.route('/mw/')
def mw():
    form = QueryForm()
    return render_template('dicts/mw/index.html', form=form)
