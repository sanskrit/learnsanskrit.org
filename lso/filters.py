import datetime

from jinja2 import Markup
from sanskrit.letters import sanscript

from lso import app


@app.template_filter()
def date(format):
    date = datetime.datetime.now()
    return date.strftime(format)


@app.template_filter()
def sa1(text, _from=sanscript.SLP1, _to=sanscript.DEVANAGARI, tag='span'):
    """Return a primary Sanskrit string in the given tag."""
    sans = sanscript.transliterate(text or '', _from, _to)
    if tag:
        return Markup('<%s class="sa1">%s</%s>' % (tag, sans, tag))
    else:
        return Markup(sans)


@app.template_filter()
def sa2(text, _from=sanscript.SLP1, _to=sanscript.IAST, tag='span'):
    """Return a secondary Sanskrit string in the given tag."""
    sans = sanscript.transliterate(text or '', _from, _to)
    if tag:
        return Markup('<%s lang="sa" class="sa2">%s</%s>' % (tag, sans, tag))
    else:
        return Markup(sans)
