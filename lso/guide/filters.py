from lso import app

@app.context_processor
def inject_notes():
    return {'notes':[]}

@app.template_filter()
def foot(text, notes):
    notes.append(text)
    i = len(notes)
    return '<sup><a id="fref-%s" href="#fnote-%s">[%s]</a></sup>' % (i, i, i)
