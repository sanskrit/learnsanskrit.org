from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlamp import DeclarativeMeta


db = SQLAlchemy()

Base = db.Model

# Base class for tree data
BaseNode = declarative_base(metadata=db.metadata,
                            metaclass=DeclarativeMeta)
BaseNode.query = db.session.query_property()


class SimpleBase(Base):

    """A simple base class."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def drop(*names):
    """Drop blueprint tables from the database.

    :param names: the blueprints to drop. If blank, drop all blueprints.
    """
    if names:
        for name in names:
            path = 'lso.{0}.models'.format(name)
            models = __import__(path, fromlist=[path])
            models.drop()
            print '  [ d ] {0}'.format(name)

    else:
        metadata.drop_all()
        for name in metadata.sorted_tables:
            print '  [ d ] {0}'.format(name)


def seed(*names):
    """Seed blueprints in the database.

    :param blueprints: the blueprint to seed.
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
