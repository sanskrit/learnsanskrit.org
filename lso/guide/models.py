import re
from sqlalchemy import Column, Integer, ForeignKey, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlamp import DeclarativeMeta

from ..database import engine, session

metadata = MetaData(engine)
BaseNode = declarative_base(metadata=metadata,
                            metaclass=DeclarativeMeta)
BaseNode.query = session.query_property()

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
