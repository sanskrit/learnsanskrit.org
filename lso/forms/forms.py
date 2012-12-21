# -*- encoding: utf-8 -*-

from flask.ext.wtf import Form, TextField, Required
from sanskrit import sanscript as S

from optgroup import OptSelectField

__all__ = ('SanskritForm', 'QueryForm')


class SanskritForm(Form):

    """Generic form for handling Sanskrit."""

    languages = [
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
    from_script = OptSelectField('From', choices=languages, default=S.HK)
    to_script = OptSelectField('To', choices=languages, default=S.DEVANAGARI)


class QueryForm(SanskritForm):

    """Form for fetching Sanskrit data from the database.

    Some scripts have ambiguities, so we should remove them from the
    list of input choices.
    """

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
            (S.DEVANAGARI, u'Devanagari (अ)'),
            (S.GUJARATI, u'Gujarati (અ)'),
            (S.KANNADA, u'Kannada (ಅ)'),
            (S.MALAYALAM, u'Malayalam (അ)'),
            (S.TELUGU, u'Telugu (అ)')
        ]],
        ['Variants', [
            ('itrans_dravidian', 'ITRANS (Dravidian)')
        ]]
        ]
    from_script = OptSelectField('From', choices=inputs, default=S.HK)
    q = TextField(validators=[Required()])
