from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

from ..database import engine, session, BaseNode

class MonierEntry(BaseNode):
    __tablename__ = 'mw_entries'
    __mp_manager__ = 'mp'

    id = Column(Integer, primary_key=True)
    entry = Column(String, index=True)  # unaccented SLP1
    accented = Column(String)  # accented SLP1
    location = Column(String)  # page and column number
    data = Column(Text)  # definition

    parent_id = Column(ForeignKey('mw_entries.id'), nullable=True)
    parent = relation('MonierEntry', remote_side=[id])

    def __repr__(self):
        return "<MonierEntry('%s')>" % self.entry


def init():
    BaseNode.metadata.create_all(bind=engine)
    import setup
    setup.run()
