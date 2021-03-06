# -*- coding: utf-8 -*-

from wtforms import (TextField, TextAreaField, validators)
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField

from lso.forms.optgroup import OptSelectField
from sanskrit import sanscript as S


class ContactForm(Form):
    subject = TextField('Subject', [validators.Required()])
    email = EmailField('Email', [validators.Optional(), validators.Email()])
    message = TextAreaField('Message', [validators.Required()])


class SettingsForm(Form):
    languages = [
        ['Indian', [
            (S.BENGALI, u'Bengali (অ)'),
            (S.DEVANAGARI, u'Devanagari (अ)'),
            (S.GUJARATI, u'Gujarati (અ)'),
            (S.GURMUKHI, u'Gurmukhi (ਅ)'),
            (S.KANNADA, u'Kannada (ಅ)'),
            (S.MALAYALAM, u'Malayalam (അ)'),
            (S.ORIYA, u'Oriya (ଅ)'),
            (S.TAMIL, u'Tamil (அ)'),
            (S.TELUGU, u'Telugu (అ)')
        ]],
        ['Roman', [
            (S.IAST, 'IAST'),
            (S.KOLKATA, 'Kolkata'),
        ]],
    ]

    inputs = [
        ['Roman', [
            (S.HK, 'Harvard-Kyoto'),
            (S.IAST, 'IAST'),
            (S.ITRANS, 'ITRANS'),
            (S.KOLKATA, 'Kolkata'),
            (S.SLP1, 'SLP1'),
            (S.VELTHUIS, 'Velthuis'),
            (S.WX, 'WX')
        ]],
        ['Indian', [
            (S.BENGALI, u'Bengali (অ)'),
            (S.DEVANAGARI, u'Devanagari (अ)'),
            (S.GUJARATI, u'Gujarati (અ)'),
            (S.GURMUKHI, u'Gurmukhi (ਅ)'),
            (S.KANNADA, u'Kannada (ಅ)'),
            (S.MALAYALAM, u'Malayalam (അ)'),
            (S.ORIYA, u'Oriya (ଅ)'),
            (S.TAMIL, u'Tamil (அ)'),
            (S.TELUGU, u'Telugu (అ)')
        ]],
        ['Variants', [
            ('itrans_dravidian', 'ITRANS (Dravidian)')
        ]]
    ]

    sa1 = OptSelectField('Main script', choices=languages,
                         default=S.DEVANAGARI)
    sa2 = OptSelectField('Secondary script', choices=languages,
                         default=S.IAST)
    input = OptSelectField('Input script', choices=inputs,
                           default=S.HK)
