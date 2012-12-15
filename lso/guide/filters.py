#!/usr/bin/python
# -*- encoding: utf-8 -*-

from xml.etree import ElementTree as ET

from flask import url_for
from jinja2 import Markup
from sanskrit import query, sanscript, sounds

from lso import app, ctx
from lso.filters import sa1, sa2

from . import guide as blue


@blue.context_processor
def inject_notes():
    return {'notes': []}


@blue.context_processor
def inject_functions():
    return {
        'ex': ex,
        'iex': iex,
        'ihex': ihex,
        'img': img,
        'lesson_url': lesson_url,
        'nominal_data': nominal_data,
        'verb_data': verb_data,
        }


@app.template_filter()
def d(text, tag='span', to=sanscript.DEVANAGARI):
    """Transliterate Harvard-Kyoto (primary)."""
    return sa1(text, sanscript.HK, to, tag=tag)


@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)


@app.template_filter()
def i(text, tag='span'):
    """Transliterate Harvard-Kyoto (secondary)."""
    return sa2(text, sanscript.HK, tag=tag)


@app.template_filter()
def render(text):
    return app.jinja_env.from_string(text).render()


def raw_text(elem, text):
    """Insert text into an Element without escaping it."""
    text = text.replace('&', '&amp;')
    wrapper = ET.fromstring(('<w>%s</w>' % text).encode('utf-8'))
    elem.text = wrapper.text
    elem.extend(wrapper.getchildren())


def ex(sa=None, en=None, **kwargs):
    """Display an example.

    :param sa: a Sanskrit string in Harvard-Kyoto
    :param en: an English string
    :key aside: a digression on the example
    :key cite: a citation
    """
    aside = kwargs.get('aside')
    cite = kwargs.get('cite')
    dev = kwargs.get('dev', True)
    iast = kwargs.get('iast')

    li = ET.Element('li')

    if sa is not None:
        if dev:
            li.append(ET.fromstring(d(sa, tag='p').encode('utf-8')))
        if iast:
            li.append(ET.fromstring(i(sa, tag='p').encode('utf-8')))

    if en is not None:
        elem = ET.SubElement(li, 'p', {'class': 'en'})
        raw_text(elem, render(en))
        if 'hint' in kwargs:
            li.attrib['class'] = 'hint'

    if aside is not None:
        elem = ET.SubElement(li, 'p')
        raw_text(elem, render(aside))
    if cite is not None:
        elem = ET.SubElement(li, 'p', {'class': 'cite'})
        raw_text(elem, render(cite))

    returned = ET.tostring(li, encoding='utf-8')
    returned = returned.decode('utf-8')
    returned = returned.replace('-&gt;', u'→').replace('&amp;', '&')
    return Markup(returned)


def iex(*args, **kwargs):
    kwargs['iast'] = True
    return ex(*args, **kwargs)


def ihex(*args, **kwargs):
    kwargs['iast'] = True
    kwargs['hint'] = True
    return ex(*args, **kwargs)


def img(filename, alt):
    full_path = url_for('guide.static', filename='img/%s' % filename)
    img = ET.Element('img', {'src': full_path, 'alt': alt})
    return Markup(ET.tostring(img))


def lesson_url(unit, lesson=None):
    """URL helper for linking to lessons and units."""
    if lesson:
        return url_for('guide.lesson', unit=unit, lesson=lesson)
    else:
        return url_for('guide.unit', unit=unit)


def nominal_data(stem, gender, cases=None):
    """Gather data for displaying a nominal paradigm.

    :param stem: the nominal stem
    :param gender: the gender to use
    """
    Q = query.SimpleQuery(ctx)
    forms = Q.noun(stem, gender)
    for key, value in forms.items():
        forms[key] = value[:-1] + sounds.simplify(value[-1])

    labels = {
        's': 'One',
        'd': 'Two',
        'p': 'Many',
        '1': 'Case 1',
        '2': 'Case 2',
        '3': 'Case 3',
        '4': 'Case 4',
        '5': 'Case 5',
        '6': 'Case 6',
        '7': 'Case 7',
        '8': 'Case 8',
    }
    return {
        'basis': stem,
        'cases': cases,
        'forms': forms,
        'labels': labels,
        }


def verb_data(root, mode, voice, vclass=None, basis=None):
    """Gather data for displaying a verb paradigm.

    :param root: the root
    :param mode: the mode to use
    :paam voice: the voice to use
    :param vclass: the verb class to use, if applicable
    :param basis: the "basis" to use when displaying the data.
                  If not provided, use the verb root.
    """
    Q = query.SimpleQuery(ctx)
    forms = Q.verb(root, mode, voice)
    for parse, form in forms.items():
        forms[parse] = form[:-1] + sounds.simplify(form[-1])

    basis = basis or root
    labels = {
        's': 'One',
        'd': 'Two',
        'p': 'Many',
        '3': '"He"',
        '2': '"You"',
        '1': '"I"',
    }
    return {
        'basis': basis,
        'forms': forms,
        'labels': labels,
        }
