from chandas import Classifier
from chandas.wrappers import iter_blocks
from flask import render_template

import forms
from lso.lib import LSOBlueprint

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
        blocks = list(iter_blocks(form.input.data))
        results = []
        for block in blocks:
            result = classifier.classify(block.raw)
            if result is None:
                line_result = classifier.classify_lines(form.input.data)
            else:
                line_result = None
            results.append((result, line_result))
        data = dict(
            form=form,
            blocks=blocks,
            results=results,
        )
        return render_template('tools/meter.html', **data)
    return render_template('tools/meter.html', form=form)


@bp.route('/sanscript')
def sanscript():
    """Transliterator."""
    form = forms.SanscriptForm()
    return render_template('tools/sanscript.html', form=form)
