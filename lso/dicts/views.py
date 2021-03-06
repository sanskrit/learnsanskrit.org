from collections import OrderedDict
from flask import redirect, render_template, request, url_for, jsonify
from sanskrit import sanscript as S

from lso.util import LSOBlueprint
from lso.views import api
from ..forms import QueryForm
from .lib import mw_transform
from .models import MonierEntry


bp = LSOBlueprint('dicts', __name__, url_prefix='/dicts')


@bp.route('/')
def index():
    """All dictionaries."""
    return render_template('dicts/index.html')


@bp.route('/mw/')
def mw():
    """Monier-Williams index"""
    form = QueryForm(request.args, csrf_enabled=False)

    if form.validate():
        q = form.data['q']
        from_script = form.data['from_script']
        to_script = form.data['to_script']

        slp_query = S.transliterate(q, from_script, S.SLP1)
        results = mw_results([slp_query])
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
    """MW results page"""
    form = QueryForm(csrf_enabled=False)
    to_script = S.DEVANAGARI

    if from_script not in S.SCHEMES:
        return redirect(url_for('.mw'))

    slp_query = S.transliterate(q, from_script, S.SLP1)
    results = mw_results([slp_query])
    for key in results:
        results[key] = [mw_transform(x, to_script) for x in results[key]]

    return render_template('dicts/mw/index.html', form=form,
                           to_script=to_script,
                           results=results)


@bp.route('/mw/works-and-authors')
def mw_works():
    """MW works and authors"""
    return render_template('dicts/mw/works-and-authors.html')


@api.route('/mw/<list:entries>')
def mw_api(entries):
    """API for MW queries. All Sanskrit is rendered in SLP1."""
    results = mw_results(entries)
    for key in results:
        results[key] = [mw_transform(x, to_script=None) for x in results[key]]
    return jsonify(results)


def mw_results(query_list):
    """For the given (SLP1) query string, returned an OrderedDict of
    results from the Monier-Williams dictionary.

    :param query_list: a list of queries
    """
    entries = MonierEntry.query.filter(MonierEntry.name.in_(query_list))
    entries = entries.order_by('id').all()

    results = OrderedDict()
    for name in query_list:
        results[name] = []

    for entry in entries:
        results[entry.name].append(entry.content)
    return results
