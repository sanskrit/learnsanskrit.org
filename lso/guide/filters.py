#!/usr/bin/python
# -*- encoding: utf-8 -*-

from jinja2 import Markup
from sanskrit.letters import sanscript
from xml.etree import ElementTree as ET

from lso import app
from lso.filters import sa1, sa2

def raw_text(elem, text):
    """Insert text into an Element without escaping it."""
    wrapper = ET.fromstring(('<w>%s</w>' % text).encode('utf-8'))
    elem.text = wrapper.text
    elem.extend(wrapper.getchildren())

@app.context_processor
def inject_notes():
    return {'notes':[]}

@app.template_filter()
def d(text, tag='span'):
    return sa1(text, sanscript.HARVARD_KYOTO, tag=tag)

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
    returned = returned.decode('utf-8').replace('-&gt;', u'→')
    return Markup(returned)

@app.template_filter()
def i(text, tag='span'):
    return sa2(text, sanscript.HARVARD_KYOTO, tag=tag)

@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)

@app.template_filter()
def render(text):
    return app.jinja_env.from_string(text).render()

app.jinja_env.globals[ex.__name__] = ex
