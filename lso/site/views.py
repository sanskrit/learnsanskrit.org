from flask import render_template
from flask.ext.mail import Message
from lso import app, mail

import forms
from . import site

@site.route('/about')
def about():
    return render_template('site/about.html')

@site.route('/contact', methods=['GET', 'POST'])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():
        default_sender = app.config['DEFAULT_MAIL_SENDER']
        default_recipient = app.config['DEFAULT_MAIL_RECIPIENT']

        msg = Message(form.subject.data,
                      sender=default_sender,
                      recipients=[default_recipient],
                      reply_to=(form.email.data or None),
                      body=form.message.data)
        mail.send(msg)
        return render_template('site/contact_success.html', form=form)
    else:
        return render_template('site/contact.html', form=form)

@site.route('/site')
def index():
    return render_template('site/index.html')

@site.route('/resources')
def resources():
    return render_template('site/resources.html')
