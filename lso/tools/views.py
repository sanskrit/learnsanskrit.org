from chandas import Classifier
from flask import render_template

from lso.lib import LSOBlueprint
import forms

bp = LSOBlueprint('tools', __name__, url_prefix='/tools')
classifier = Classifier.from_json_file('/home/akp/projects/chandas/data/data.json')

@bp.route('/')
def index():
    return render_template('tools/index.html')


@bp.route('/meter', methods=['GET', 'POST'])
def meter():
    """Meter recognizer."""
    form = forms.MeterForm()
    if form.validate_on_submit():
        result = classifier.classify(form.input.data)
        return render_template('tools/meter.html', form=form, result=result)
    return render_template('tools/meter.html', form=form)


@bp.route('/sanscript')
def sanscript():
    """Transliterator."""
    form = forms.SanscriptForm()
    return render_template('tools/sanscript.html', form=form)
