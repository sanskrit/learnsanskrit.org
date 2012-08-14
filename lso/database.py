from lso import app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def init():
    # Import models from all registered blueprints
    for name in app.blueprints:
        print '    %s' % name
        try:
            path = 'lso.%s.models' % name
            blue = __import__(path, fromlist=[path])
        except ImportError:
            continue

        # If a model extends `Base`, then `create_all` will account for it.
        # For other cases, try calling a custom init function:
        try:
            blue.init()
        except AttributeError:
            pass

    Base.metadata.create_all(bind=engine)
