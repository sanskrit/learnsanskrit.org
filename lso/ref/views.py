# -*- coding: utf-8 -*-
"""
    lso.ref.views
    ~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from collections import OrderedDict

from flask import render_template, request, url_for
from sanskrit import sanscript, schema as X

from lso import ctx, simple_query
from . import ref
from ..database import session
from ..forms import QueryForm


def to_slp1(q, from_script):
    return sanscript.transliterate(q, from_script, sanscript.SLP1)


def _root_result(root, q, from_script):
    """Prepare the data needed to display a root result."""
    name = root.name
    return {
        'id': root.id,
        'name': name,
        'url': url_for('.root', name=name, from_script=from_script),
        'description': None
        }


def _stem_result(stem, q, from_script):
    """Prepare the data needed to display a stem result."""
    gender_group = ctx.enum_abbr['gender_group']
    name = stem.name
    pos_id = stem.pos_id

    if pos_id == X.Tag.NOUN:
        genders = gender_group[stem.genders_id]
        url = url_for('.noun', from_script=sanscript.SLP1,
                      name=name, genders=genders)
        description = genders + '.'

    elif pos_id == X.Tag.PRONOUN:
        url = url_for('.pronoun', from_script=sanscript.SLP1,
                      name=name)
        description = 'pronoun'
    else:
        url = '#'
        description = None

    return {
        'id': stem.id,
        'name': stem.name,
        'url': url,
        'description': description
        }


def query(q_raw, from_script):
    """Query for any sort of Sanskrit data.

    :param q: a string representing a single word or morpheme.
    :param from_script: the script used by `q`
    """
    q = to_slp1(q_raw, from_script)

    results = []
    for r in session.query(X.Root).filter(X.Root.name == q):
        results.append(_root_result(r, q_raw, from_script))

    for r in session.query(X.Stem).filter(X.Stem.name == q):
        results.append(_stem_result(r, q_raw, from_script))

    for r in session.query(X.Form).filter(X.Form.name == q):
        pos_id = r.pos_id

        if pos_id == X.Tag.NOUN or pos_id == X.Tag.PRONOUN:
            results.append(_stem_result(r.stem, q_raw, from_script))

        elif pos_id == X.Tag.VERB:
            results.append(_root_result(r.root, q_raw, from_script))

    # Remove duplicate results
    seen = set()
    add = seen.add
    return [x for x in results if x['id'] not in seen and not add(x['id'])]


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
    name = to_slp1(name, from_script)
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
    name = to_slp1(name, from_script)
    paradigm = simple_query.pronoun(name, 'm')

    data = {
        'name': name,
        'paradigm': paradigm,
        'classes': paradigm_colors(paradigm),
        }
    return render_template('ref/nominal.html', **data)


@ref.route('/root-<from_script>/<name>')
def root(name, from_script):
    """Display a summary of a root's forms"""
    name = to_slp1(name, from_script)
    forms = simple_query.verb_summary(name)

    labels = {
        'pres': 'Present',
        'ipft': 'Imperfect',
        'impv': 'Imperative',
        'opt': 'Optative',
        'sfut': 'Simple future',
        'dfut': 'Distant future',
        'fut': 'Future',
        'past': 'Past',
        'aor': 'Aorist',
        'inj': 'Injunctive',
        'ben': 'Benedictive',
        'cond': 'Conditional',
        'perf': 'Perfect',
        'P': 'Parasmaipada',
        'A': u'Ātmanepada',
        'passive': 'Passive',
    }

    verb_modes = 'pres impv ipft opt cond sfut dfut aor inj perf'.split()
    part_modes = 'fut pres past perf'.split()
    voices = 'P A passive'.split()

    data = {
        'name': name,
        'verb_modes': verb_modes,
        'part_modes': part_modes,
        'voices': voices,
        'forms': forms,
        'labels': labels,
    }

    return render_template('ref/root.html', **data)


@ref.route('/root-<from_script>/<name>/<mode>-<voice>')
def verb_paradigm(name, from_script, mode, voice):
    """Display a verb paradigm."""
    name = to_slp1(name, from_script)
    return render_template('ref/verb_paradigm.html')


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
