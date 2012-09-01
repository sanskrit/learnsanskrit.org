from flask import render_template

import forms
from . import tools

@tools.route('/')
def index():
    return render_template('tools/index.html')

@tools.route('/sanscript')
def sanscript():
    form = forms.SanscriptForm()
    return render_template('tools/sanscript.html', form=form)
