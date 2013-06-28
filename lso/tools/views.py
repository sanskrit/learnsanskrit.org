from flask import Blueprint, render_template

from lso.lib import LSOBlueprint
import forms

bp = LSOBlueprint('tools', __name__, url_prefix='/tools')


@bp.route('/')
def index():
    return render_template('tools/index.html')


@bp.route('/sanscript')
def sanscript():
    form = forms.SanscriptForm()
    return render_template('tools/sanscript.html', form=form)
