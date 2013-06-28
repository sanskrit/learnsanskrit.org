from collections import OrderedDict
from flask import redirect, render_template, request, url_for, jsonify
from sanskrit import sanscript as S

from lso import app
from lso.lib import LSOBlueprint
from ..forms import QueryForm
from .lib import mw_transform
from .models import MonierEntry


bp = LSOBlueprint('dicts', __name__, url_prefix='/dicts')


@bp.route('/')
def index():
    return render_template('dicts/index.html')


@bp.route('/mw/')
def mw():
    form = QueryForm(request.args, csrf_enabled=False)

    if form.validate():
        q = form.data['q']
        from_script = form.data['from_script']
        to_script = form.data['to_script']

        slp_query = S.transliterate(q, from_script, S.SLP1)
        results = mw_results(slp_query)
        for key in results:
            results[key] = [mw_transform(x, to_script) for x in results[key]]

        return render_template('dicts/mw/index.html',
                               form=form,
                               to_script=to_script,
                               results=results)
    else:
        return render_template('dicts/mw/index.html', form=form)


@bp.route('/mw/q-<from_script>/<q>')
def mw_pretty(from_script, q):
    form = QueryForm(csrf_enabled=False)
    to_script = S.DEVANAGARI

    if from_script not in S.SCHEMES:
        return redirect(url_for('.mw'))

    slp_query = S.transliterate(q, from_script, S.SLP1)
    results = mw_results(slp_query)
    for key in results:
        results[key] = [mw_transform(x, to_script) for x in results[key]]

    return render_template('dicts/mw/index.html', form=form,
                           to_script=to_script,
                           results=results)


@bp.route('/mw/works-and-authors')
def mw_works():
    return render_template('dicts/mw/works-and-authors.html')


@app.route('/api/mw/<slp_query>')
def mw_api(slp_query):
    results = mw_results(slp_query)
    for key in results:
        results[key] = [mw_transform(x, None) for x in results[key]]
    return jsonify(results)


def mw_results(q):
    """For the given (SLP1) query string, returned an OrderedDict of
    results from the Monier-Williams dictionary.
    """
    q_list = q.replace('+', ' ').replace(',', ' ').split()

    entries = MonierEntry.query.filter(MonierEntry.name.in_(q_list))
    entries = entries.order_by('id').all()

    results = OrderedDict()
    for entry in q_list:
        results[entry] = []

    for e in entries:
        results[e.name].append(e.data)
    return results
