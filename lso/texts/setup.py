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


def run(app=None):
    app = app or lso.create_app(__name__)
    with app.app_context():
        if Language.query.count():
            print 'Texts already has data. Drop the tables first.'
        else:
            init_texts()


def drop():
    order = [SegSegAssoc, Segment, Text, Division, Author, Language, Category]
    for o in order:
        try:
            o.__table__.drop()
        except sqlalchemy.exc.ProgrammingError:
            print '(table %s does not exist.)' % o.__tablename__
