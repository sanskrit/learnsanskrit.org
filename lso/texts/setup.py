import lso.database
from .models import Category, Language


def init_texts():
    """Create initial languages."""
    session = lso.database.db.session
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
    app = app or lso.create_app(__name__)
    with app.app_context():
        if force:
            Language.query.delete()

        if not Language.query.count():
            init_texts()
