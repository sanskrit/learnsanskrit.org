# -*- coding: utf-8 -*-
"""
    lso.ref.views
    ~~~~~~~~~~~~~

    :license: MIT and BSD
"""

from collections import OrderedDict

from flask import g, render_template, request, url_for
from sanskrit import sanscript, schema as X, sounds

from lso import ctx, simple_analyzer, simple_query
from lso.lib.readable import Readable
from . import ref
from ..database import session
from ..forms import QueryForm


# Helper functions
# ----------------

def to_slp1(q, from_script):
    """Helper function. Transliterate to SLP1."""
    return sanscript.transliterate(q, from_script, sanscript.SLP1)


def _root_result(root, results, lookup):
    """Prepare the data needed to display a root result."""

    if root.id in lookup:
        return lookup[root.id]

    id = root.id
    name = root.name

    datum = {
        'id': id,
        'name': name,
        'url': url_for('.root', name=name, from_script=sanscript.SLP1),
        'description': g.readable.root_abbr(root),
        'children': []
        }

    results.append(datum)
    lookup[id] = datum
    return datum


def _stem_result(stem, results, lookup):
    """Prepare the data needed to display a stem result."""

    if stem.id in lookup:
        return lookup[stem.id]

    id = stem.id
    name = stem.name
    pos_id = stem.pos_id
    gender_group = ctx.enum_abbr['gender_group']

    datum = {
        'id': stem.id,
        'name': name,
        'description': g.readable.stem_abbr(stem),
        'children': []
        }

    if pos_id == X.Tag.NOUN:
        genders = gender_group[stem.genders_id]
        datum['url'] = url_for('.noun', from_script=sanscript.SLP1,
                               name=name, genders=genders)
        results.append(datum)

    elif pos_id == X.Tag.PRONOUN:
        datum['url'] = url_for('.pronoun', from_script=sanscript.SLP1,
                               name=name)
        results.append(datum)

    elif pos_id == X.Tag.ADJECTIVE:
        datum['url'] = '#'
        results.append(datum)

    elif pos_id == X.Tag.PARTICIPLE:
        datum['url'] = '#'

        parent = _root_result(stem.root, results, lookup)
        parent['children'].append(datum)

    else:
        datum['url'] = '#'
        datum['description'] = None

    lookup[id] = datum
    return datum


def _form_result(form, results, lookup):
    """Prepare the data needed to display a form result."""

    pos_id = form.pos_id

    datum = {
        'name': sounds.Term(form.name).simplify(),
        'description': g.readable.form_abbr(form),
        'children': []
        }

    Tag = X.Tag
    if pos_id in (Tag.NOUN, Tag.PRONOUN, Tag.ADJECTIVE, Tag.PARTICIPLE):
        parent = _stem_result(form.stem, results, lookup)
        parent['children'].append(datum)

    elif pos_id == Tag.VERB:
        child = datum
        datum = _root_result(form.root, results, lookup)
        datum['children'].append(child)

    elif pos_id == Tag.INDECLINABLE:
        results.append(datum)


def query(q):
    """Query for any sort of Sanskrit data.

    :param q: an SLP1 string representing a single word or morpheme.
    """
    results = []
    lookup = {}
    for r in session.query(X.Root).filter(X.Root.name == q):
        _root_result(r, results, lookup)

    for r in session.query(X.Stem).filter(X.Stem.name == q):
        _stem_result(r, results, lookup)

    for r in simple_analyzer.analyze(q):
        _form_result(r, results, lookup)

    return results


# Blueprint functions
# -------------------

@ref.before_request
def make_readable():
    """Create a :class:`Readable` to translate a form's database IDs
    to a readable form.
    """
    g.readable = Readable(ctx)


@ref.route('/')
def index():
    """Display a basic query form."""
    query_form = QueryForm(request.args, csrf_enabled=False)
    results = []
    from_script = query_form.data['from_script']

    if query_form.validate():
        q = to_slp1(query_form.data['q'], from_script)
        results = query(q)
    else:
        q = None

    data = {
        'q': q,
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
