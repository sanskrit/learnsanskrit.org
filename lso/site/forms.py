from flask.ext.wtf import (Form, TextField, TextAreaField,
                           Email, Optional, Required)
from flask.ext.wtf.html5 import EmailField

class ContactForm(Form):
    subject = TextField('Subject', [Required()])
    email = EmailField('Email', [Optional(), Email()])
    message = TextAreaField('Message', [Required()])
