import lso.database
from .models import Category, Language

__all__ = ['run']


def init_texts(session):
    """Create initial languages."""
    languages = [('Sanskrit', 'sa'), ('English', 'en')]
    for name, slug in languages:
        session.add(Language(name=name, slug=slug))

    categories = [('Original', 'original'),
                  ('Translation', 'translation'),
                  ('Commentary', 'commentary')]
    for name, slug in categories:
        session.add(Category(name=name, slug=slug))

    session.commit()


def run():
    if not Language.query.count():
        init_texts(lso.database.db.session)
