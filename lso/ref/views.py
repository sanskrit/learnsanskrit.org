from collections import OrderedDict

from flask import render_template, request, url_for
from sanskrit import sanscript, schema as X

from lso import ctx, simple_query
from . import ref
from ..database import session
from ..forms import QueryForm


def query(q_raw, from_script):
    """Query for any sort of Sanskrit data.

    :param q: a string representing a single word or morpheme.
    :param from_script: the script used by `q`
    """
    q = sanscript.transliterate(q_raw, from_script, sanscript.SLP1)
    gender_group = ctx.enum_abbr['gender_group']

    results = []
    for r in session.query(X.Stem).filter(X.Stem.name == q):
        pos_id = r.pos_id

        if pos_id == X.Tag.NOUN:
            genders = gender_group[r.genders_id]
            url = url_for('.noun', from_script=from_script,
                          name=q_raw, genders=genders)
            description = genders

        elif pos_id == X.Tag.PRONOUN:
            url = url_for('.pronoun', from_script=from_script,
                          name=q_raw)
            description = 'pronoun'
        else:
            url = '#'
            description = None

        data = {
            'name': r.name,
            'url': url,
            'description': description
            }
        results.append(data)

    return results


@ref.route('/')
def index():
    """Display a basic query form."""
    query_form = QueryForm(request.args, csrf_enabled=False)
    results = []
    from_script = query_form.data['from_script']

    if query_form.validate():
        results = query(query_form.data['q'], from_script)

    data = {
        'form': query_form,
        'results': results,
    }
    return render_template('ref/index.html', **data)


@ref.route('/nouns-<from_script>/<name>-<genders>')
def noun(name, from_script, genders=None):
    """Display a noun paradigm."""
    name = sanscript.transliterate(name, from_script, sanscript.SLP1)
    paradigm = simple_query.noun(name, genders)

    data = {
        'name': name,
        'paradigm': paradigm,
        'classes': paradigm_colors(paradigm),
        }
    return render_template('ref/nominal.html', **data)


@ref.route('/pronouns-<from_script>/<name>')
def pronoun(name, from_script, genders=None):
    """Display a pronoun paradigm."""
    name = sanscript.transliterate(name, from_script, sanscript.SLP1)
    paradigm = simple_query.pronoun(name, 'm')

    data = {
        'name': name,
        'paradigm': paradigm,
        'classes': paradigm_colors(paradigm),
        }
    return render_template('ref/nominal.html', **data)


def paradigm_colors(paradigm):
    """Map parses to colors."""
    # 1. Cluster identical forms
    returned = {}
    rev_colors = OrderedDict()
    for parse, name in paradigm.iteritems():
        rev_colors.setdefault(name, set()).add(parse)

    # 2. Assign a color class to each cluster
    i = 1
    for parses in rev_colors.itervalues():
        if len(parses) > 1:
            for parse in parses:
                returned[parse] = 'c' + str(i)
            i += 1
    return returned
