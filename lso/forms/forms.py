# -*- encoding: utf-8 -*-

from flask.ext.wtf import Form, SelectField, TextField, Required
from sanskrit.letters import sanscript as S

from optgroup import OptSelectField

__all__ = ('SanskritForm', 'QueryForm')

class SanskritForm(Form):
    """Generic form for handling Sanskrit."""
    languages = [
                    ['Roman', [
                        (S.HARVARD_KYOTO, 'Harvard-Kyoto'),
                        (S.IAST, 'IAST'),
                        (S.ITRANS, 'ITRANS'),
                        (S.KOLKATA, 'Kolkata'),
                        (S.SLP1, 'SLP1'),
                        (S.VELTHUIS, 'Velthuis')
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
    from_script = OptSelectField('From', choices=languages, default=S.ITRANS)
    to_script = OptSelectField('To', choices=languages, default=S.DEVANAGARI)
