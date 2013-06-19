import sqlalchemy.exc
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import Text as _Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list

from ..database import SimpleBase, BaseNode


CASCADE_ARGS = 'all,delete,delete-orphan'


class Language(SimpleBase):

    """The language of some :class:`Text`"""

    name = Column(String)


# class Author(SimpleBase):

#     """The author of some :class:`Text`"""

#     en_name = Column(String)
#     sa_name = Column(String)
#     #: A human-readable identifier
#     slug = Column(String, unique=True)


class Text(SimpleBase):

    """A complete text, whether Sanskrit or otherwise."""

    id = Column(Integer, primary_key=True)

    #: A human-readable title in roman letters. Sanskrit texts will use
    #: titles in SLP1.
    name = Column(String)
    #: A human-readable identifier
    slug = Column(String, unique=True)
    #: An XML prefix for the text (for XML conversion)
    xmlid_prefix = Column(String, unique=True)

    #: The text's primary language
    language_id = Column(ForeignKey(Language.id))
    #: The division tree associated with the text
    division_id = Column(Integer, ForeignKey('division.id'), nullable=True)
    #: The text's parent, if defined
    parent_id = Column(Integer, ForeignKey('text.id'), nullable=True)

    language = relationship(Language)
    division = relationship('Division', cascade=CASCADE_ARGS)
    parent = relationship('Text', remote_side=[id], backref='children')
    segments = relationship('Segment', cascade=CASCADE_ARGS, backref='text')

    def __unicode__(self):
        return '%s' % self.slug


class Division(BaseNode):

    """A textual division"""

    __tablename__ = 'division'
    __mp_manager__ = 'mp'

    #: Primary key
    id = Column(Integer, primary_key=True)
    #: A human-readable identifier
    slug = Column(String, nullable=True)

    parent_id = Column(Integer, ForeignKey('division.id'), nullable=True)
    parent = relationship('Division', remote_side=[id])

    def __repr__(self):
        return '<Division(%s, %s)>' % (self.id, self.slug)

    def __unicode__(self):
        return '%s' % self.slug


class SegSegAssoc(SimpleBase):
    parent_id = Column(ForeignKey('segment.id'), primary_key=True)
    child_id = Column(ForeignKey('segment.id'), primary_key=True)
    text_id = Column(ForeignKey('text.id'), primary_key=True)

    parent = relationship('Segment',
                          primaryjoin='SegSegAssoc.parent_id==Segment.id',
                          foreign_keys=[parent_id],
                          backref='child_assocs')

    child = relationship('Segment',
                         primaryjoin='SegSegAssoc.child_id==Segment.id',
                         foreign_keys=[child_id],
                         backref='parent_assocs')

    text = relationship('Text')


class Segment(SimpleBase):

    """A discrete piece of some text."""

    #: A human-readable identifier
    slug = Column(String, index=True)
    #: The content contained in this segment
    content = Column(_Text)
    #: The segment's position within the division
    position = Column(Integer)
    #: The :class:`Text` that owns this segment
    text_id = Column(ForeignKey(Text.id), index=True)
    #: The :class:`Division` that contains this segment
    division_id = Column(ForeignKey(Division.id))

    division = relationship(Division, cascade=CASCADE_ARGS, single_parent=True)
    children = association_proxy('child_assocs', 'child')
    parents = association_proxy('parent_assocs', 'parent')

    def __repr__(self):
        return '<Segment(%s, %s)>' % (self.id, self.slug)


Text.division = relationship(Division)
Division.segments = relationship(Segment,
                                 collection_class=ordering_list('position'),
                                 order_by=Segment.position)


def drop():
    order = [SegSegAssoc, Segment, Text, Division, Language]
    for o in order:
        try:
            o.__table__.drop()
        except sqlalchemy.exc.ProgrammingError:
            print '(table %s does not exist.)' % o.__tablename__
