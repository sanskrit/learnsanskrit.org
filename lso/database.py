from lso import app
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlamp import DeclarativeMeta

engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
metadata = MetaData(engine)

# Base class for ordinary data
Base = declarative_base(metadata=metadata)
Base.query = session.query_property()

# Base class for tree data
BaseNode = declarative_base(metadata=metadata,
                            metaclass=DeclarativeMeta)
BaseNode.query = session.query_property()

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
            fn = blue.init
        except AttributeError:
            fn = None
        if fn is not None:
            fn()

    Base.metadata.create_all(bind=engine)
