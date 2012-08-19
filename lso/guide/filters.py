from sanskrit.letters import sanscript

from lso import app
from lso.filters import sa1, sa2

@app.context_processor
def inject_notes():
    return {'notes':[]}

@app.template_filter()
def d(text, tag='span'):
    return sa1(text, sanscript.HARVARD_KYOTO, tag=tag)

@app.template_filter()
def i(text, tag='span'):
    return sa2(text, sanscript.HARVARD_KYOTO, tag=tag)

@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)
