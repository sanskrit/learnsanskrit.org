import sqlamp

from ..database import engine, session
from sqlalchemy import Column, Integer, ForeignKey, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

metadata = MetaData(engine)
BaseNode = declarative_base(metadata=metadata,
                            metaclass=sqlamp.DeclarativeMeta)
BaseNode.query = session.query_property()

class Lesson(BaseNode):
    __tablename__ = 'lessons'
    __mp_manager__ = 'mp'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    parent_id = Column(ForeignKey('lessons.id'))

    parent = relation('Lesson', remote_side=[id])

    def __repr__(self):
        return '<Lesson(%s,%s)>' % (self.id, self.slug)


def init():
    BaseNode.metadata.create_all(bind=engine)
    import setup
    setup.run()
