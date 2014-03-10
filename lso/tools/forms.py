from flask.ext.wtf import TextAreaField

from lso.forms import SanskritForm


class SanscriptForm(SanskritForm):
    input = TextAreaField()
    output = TextAreaField()


class MeterForm(SanskritForm):
    input = TextAreaField()
