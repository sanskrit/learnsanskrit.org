from lso import app
from sqlalchemy import create_engine, Column, Integer, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
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


class SimpleBase(Base):

    """A simple base class."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def create(*names):
    """Create tables in the database.

    :param names: the tables to create. If blank, create all tables.
    """
    if names:
        for name in names:
            table = metadata.tables.get(name, None)
            if table is None:
                print '  [ ? ] {0}'.format(name)
            elif table.exists():
                print '  [ e ] {0}'.format(name)
            else:
                table.create()
                print '  [ c ] {0}'.format(name)
    else:
        extant = {t.name for t in metadata.tables.values() if t.exists()}
        metadata.create_all()
        for name in metadata.sorted_tables:
            if name not in extant:
                print '  [ c ] {0}'.format(name)


def drop(*names):
    """Drop tables from the database.

    :param names: the tables to create. If blank, drop all tables.
    """
    if names:
        for name in names:
            table = metadata.tables.get(name, None)
            if table is None:
                print '  [ ? ] {0}'.format(name)
            else:
                table.drop()
                print '  [ d ] {0}'.format(name)
    else:
        metadata.drop_all()
        for name in metadata.sorted_tables:
            print '  [ d ] {0}'.format(name)


def seed(*names):
    """Seed tables in the database, by way of their blueprints.

    For a blueprint `bp`, this function will try to call `bp.setup.run()`.

    Due to interdependencies, it's not always clear how a model should be
    initialized or where its seed code should live. So, the details of this
    are left to blueprints.

    :param blueprints: the blueprint containing the tables to seed.
    """

    names = names or app.blueprints

    for name in names:
        path = 'lso.{0}.setup'.format(name)
        run = None

        try:
            print '  {0}\n  {1}'.format(name, '-' * len(name))
            setup = __import__(path, fromlist=[path])
            setup.run()
            print
        except ImportError:
            print '  No setup code found!\n'
