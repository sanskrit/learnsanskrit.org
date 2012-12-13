#!/usr/bin/python
# -*- encoding: utf-8 -*-

import functools

from flask import url_for
from jinja2 import Markup
from sanskrit import sanscript
from xml.etree import ElementTree as ET

from lso import app
from lso.filters import sa1, sa2


def raw_text(elem, text):
    """Insert text into an Element without escaping it."""
    text = text.replace('&', '&amp;')
    wrapper = ET.fromstring(('<w>%s</w>' % text).encode('utf-8'))
    elem.text = wrapper.text
    elem.extend(wrapper.getchildren())


def to_template(path):
    """Render the output of the decorated function into the template
    located at the given path. Paths are resolved using the Flask app,
    so any path that can be found by Flask is valid.

    :param path: the template path"""
    def decorator(func):
        @functools.wraps(func)
        def newfunc(*a, **kw):
            data = func(*a, **kw)
            return Markup(app.jinja_env.get_template(path).render(**data))
        return newfunc
    return decorator


@app.context_processor
def inject_notes():
    return {'notes': []}


@app.context_processor
def inject_functions():
    return {'ex': ex,
            'iex': iex,
            'ihex': ihex,
            'img': img,
            'lesson_url': lesson_url,
            'noun': noun,
            'verb': verb
            }


@app.template_filter()
def d(text, tag='span', to=sanscript.DEVANAGARI):
    return sa1(text, sanscript.HK, to, tag=tag)


def ex(sa=None, en=None, **kwargs):
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


@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)


@app.template_filter()
def i(text, tag='span'):
    return sa2(text, sanscript.HK, tag=tag)


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


@to_template('include/charts/noun.html')
def noun(stem, genders, cases='12345678'):
    forms = {(p, n): '[%s%s]' % (p, n) for p in cases for n in 'sdp'}
    return {'stem': stem, 'forms': forms}


@app.template_filter()
def render(text):
    return app.jinja_env.from_string(text).render()


@to_template('include/charts/verb.html')
def verb(root, vclass, mode, voice):
    forms = {(p, n): '[%s%s]' % (p, n) for p in '123' for n in 'sdp'}
    return {'root': root, 'forms': forms}
