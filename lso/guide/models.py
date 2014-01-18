import re
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relation, relationship

from ..database import engine, Base, BaseNode, SimpleBase

class _Lesson(BaseNode):
    __tablename__ = 'lessons'
    __mp_manager__ = 'mp'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    parent_id = Column(ForeignKey('lessons.id'))

    parent = relation('_Lesson', remote_side=[id])

    @property
    def stripped_title(self):
        return re.sub('<.*?>', '', self.title)

    def __repr__(self):
        return '<_Lesson(%s,%s)>' % (self.id, self.slug)


class Lesson(SimpleBase):

    """A single lesson."""

    name = Column(String)
    slug = Column(String, unique=True)

    def __repr__(self):
        return '<Lesson(%s,%s)>' % (self.id, self.slug)

    def add_dependencies(self, *deps):
        for dep in deps:
            LessonEdge(dep, self)

    def predecessors(self):
        return [x.head for x in self.incoming_edges]

    def successors(self):
        return [x.tail for x in self.outgoing_edges]


class LessonEdge(Base):

    """A directed edge between two lessons.

    Lesson *A* points to lesson *B* if and only if *B* depends on *A*.
    """
    __tablename__ = 'lesson_edge'

    head_id = Column(ForeignKey('lesson.id'), primary_key=True)
    tail_id = Column(ForeignKey('lesson.id'), primary_key=True)

    head = relationship(Lesson, primaryjoin=head_id==Lesson.id,
                        backref='outgoing_edges')

    tail = relationship(Lesson, primaryjoin=tail_id==Lesson.id,
                        backref='incoming_edges')

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail


def init():
    BaseNode.metadata.create_all(bind=engine)
    import setup
    setup.run()
