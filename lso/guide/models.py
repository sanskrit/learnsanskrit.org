import re
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

from ..database import engine, session, BaseNode

class Lesson(BaseNode):
    __tablename__ = 'lessons'
    __mp_manager__ = 'mp'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    parent_id = Column(ForeignKey('lessons.id'))

    parent = relation('Lesson', remote_side=[id])

    @property
    def stripped_title(self):
        return re.sub('<.*?>', '', self.title)

    def __repr__(self):
        return '<Lesson(%s,%s)>' % (self.id, self.slug)


def init():
    BaseNode.metadata.create_all(bind=engine)
    import setup
    setup.run()
