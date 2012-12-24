#!/usr/bin/python
# -*- encoding: utf-8 -*-

from xml.etree import ElementTree as ET

from flask import url_for
from jinja2 import Markup
from sanskrit import sanscript

from lso import app, simple_query
from lso.filters import sa1, sa2

from . import guide as blue


@blue.context_processor
def inject_notes():
    return {'notes': []}


@blue.context_processor
def inject_functions():
    return {
        'img': img,
        'lesson_url': lesson_url,
        'nominal_data': nominal_data,
        'verb_data': verb_data,
        }


@app.template_filter()
def d(text, tag='span', to=sanscript.DEVANAGARI):
    """Transliterate Harvard-Kyoto (primary)."""
    return sa1(Markup(text), sanscript.HK, to, tag=tag, safe=True)


@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)


@app.template_filter()
def i(text, tag='span'):
    """Transliterate Harvard-Kyoto (secondary)."""
    return sa2(Markup(text), sanscript.HK, tag=tag, safe=True)


@app.template_filter()
def render(text):
    return app.jinja_env.from_string(text).render()


def raw_text(elem, text):
    """Insert text into an Element without escaping it."""
    text = text.replace('&', '&amp;')
    wrapper = ET.fromstring(('<w>%s</w>' % text).encode('utf-8'))
    elem.text = wrapper.text
    elem.extend(wrapper.getchildren())


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
    forms = simple_query.noun(stem, gender)
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
    forms = simple_query.verb(root, mode, voice, vclass=vclass)
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
