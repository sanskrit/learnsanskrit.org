from collections import OrderedDict
from flask import render_template, request
from sanskrit.letters import sanscript as S

from ..database import session
from ..forms import QueryForm
from . import dicts
from .lib import mw_transform
from .models import MonierEntry

@dicts.route('/')
def index():
    return render_template('dicts/index.html')

@dicts.route('/mw/')
def mw():
    form = QueryForm(request.args, csrf_enabled=False)

    if form.validate():
        q = form.data['q']
        from_script = form.data['from_script']
        to_script = form.data['to_script']

        slp_query = S.transliterate(q, from_script, S.SLP1)
        results = mw_results(slp_query)
        for key in results:
            results[key]  = [mw_transform(x, to_script) for x in results[key]]

        return render_template('dicts/mw/index.html', form=form,
                                                      to_script=to_script,
                                                      results=results)
    else:
        return render_template('dicts/mw/index.html', form=form)

def mw_results(q):
    """For the given (SLP1) query string, returned an OrderedDict of results
    from the Monier-Williams dictionary.
    """
    q_list = q.replace('+', ' ').replace(',', ' ').split()

    entries = MonierEntry.query.filter(MonierEntry.entry.in_(q_list))
    entries = entries.order_by('id').all()

    results = OrderedDict()
    for entry in q_list:
        results[entry] = []

    for e in entries:
        results[e.entry].append(e.data)
    return results
