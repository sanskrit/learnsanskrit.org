from ..database import session
from .models import Language, Text, Division, Segment

__all__ = ['run']


def init_texts():
    """Create initial languages."""
    languages = ['sanskrit', 'english']
    for lang in languages:
        session.add(Language(name=lang))

    text = Text(name='Sanskrit Grammar', slug='sanskrit-grammar',
        xmlid_prefix='SG')

    session.add(text)
    session.flush()

    session.commit()
    session.remove()


def run():
    if not Language.query.count():
        init_texts()
