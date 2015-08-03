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
