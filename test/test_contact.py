import pytest

import lso

def contact(app, data):
    """POST data to the contact form."""
    return app.post('/contact', data=data)


def test_subject_email_and_message(app, test_app):
    subject = 'subject'
    reply_to = 'a@example.com'
    message_body = 'body'
    sender = app.config['DEFAULT_MAIL_SENDER']

    with lso.mail.record_messages() as outbox:
        result = contact(test_app, dict(subject=subject,
                                   email=reply_to,
                                   message=message_body))
        assert len(outbox) == 1
        message = outbox[0]
        assert message.sender == sender
        assert message.subject == subject
        assert message.reply_to == reply_to
        assert message.body == message_body


def test_subject_and_message(app, test_app):
    subject = 'subject'
    message_body = 'body'
    sender = app.config['DEFAULT_MAIL_SENDER']

    with lso.mail.record_messages() as outbox:
        result = contact(test_app, dict(subject=subject,
                                        message=message_body))

        assert len(outbox) == 1
        message = outbox[0]
        assert message.sender == sender
        assert message.subject == subject
        assert message.reply_to == None
        assert message.body == message_body


def test_invalid_email(app, test_app):
    with lso.mail.record_messages() as outbox:
        result = contact(test_app, dict(subject='subject',
                                   email='aoeu',
                                   message='body'))
        assert not outbox


def test_subject_only(app, test_app):
    with lso.mail.record_messages() as outbox:
        result = contact(test_app, dict(subject='subject'))
        assert not outbox


def test_message_only(app, test_app):
    with lso.mail.record_messages() as outbox:
        result = contact(test_app, dict(message='msg'))
        assert not outbox
