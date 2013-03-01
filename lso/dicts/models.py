from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relation

from ..database import engine, Base


class MonierEntry(Base):
    __tablename__ = 'mw_entries'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)  # unaccented SLP1
    location = Column(String)  # page and column number
    data = Column(Text)  # definition

    def __repr__(self):
        return "<MonierEntry('%s')>" % self.entry


def init():
    import setup
    setup.run()
