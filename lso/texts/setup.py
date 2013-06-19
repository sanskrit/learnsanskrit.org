from ..database import session
from .models import Language

__all__ = ['run']


def init_texts():
    """Create initial languages."""
    languages = [('Sanskrit', 'sa'), ('English', 'en')]
    for name, slug in languages:
        session.add(Language(name=name, slug=slug))

    session.commit()
    session.remove()


def run():
    if not Language.query.count():
        init_texts()
