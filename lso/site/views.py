from flask import Blueprint, render_template, request, current_app
from flask.ext.mail import Message
from lso import mail
from lso.lib import LSOBlueprint

import forms

bp = LSOBlueprint('site', __name__, url_prefix='')


@bp.route('/about')
def about():
    return render_template('site/about.html')


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():
        default_sender = current_app.config['DEFAULT_MAIL_SENDER']
        default_recipient = current_app.config['DEFAULT_MAIL_RECIPIENT']

        msg = Message(form.subject.data,
                      sender=default_sender,
                      recipients=[default_recipient],
                      reply_to=(form.email.data or None),
                      body=form.message.data)
        mail.send(msg)
        return render_template('site/contact_success.html', form=form)
    else:
        return render_template('site/contact.html', form=form)


@bp.route('/site')
def index():
    return render_template('site/index.html')


@bp.route('/settings')
def settings():
    form = forms.SettingsForm()
    if request.is_xhr:
        return render_template('js/settings.html', form=form)
    else:
        return render_template('site/settings.html', form=form)


@bp.route('/resources')
def resources():
    return render_template('site/resources.html')


@bp.route('/source')
def source():
    return render_template('site/source.html')
