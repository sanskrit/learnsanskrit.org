from flask.ext.wtf import (Form, TextField, TextAreaField,
                           Optional, Required)
from flask.ext.wtf.html5 import EmailField

class ContactForm(Form):
    subject = TextField('Subject', [Required()])
    email = EmailField('Email', [Optional()])
    message = TextAreaField('Message', [Required()])
