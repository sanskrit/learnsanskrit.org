from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import Text as _Text
from sqlalchemy.orm import relation, relationship
from sqlalchemy.ext.orderinglist import ordering_list

from ..database import SimpleBase, BaseNode


class Language(SimpleBase):

    """The language of some :class:`Text`"""

    name = Column(String)


class Author(SimpleBase):

    """The author of some :class:`Text`"""

    en_name = Column(String)
    sa_name = Column(String)
    #: A human-readable identifier
    slug = Column(String, unique=True)


class Text(SimpleBase):

    """A complete text, whether Sanskrit or otherwise."""

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

    language = relationship(Language)
    segments = relationship('Segment', cascade='all, delete-orphan',
                            backref='text')

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
    parent = relation('Division', remote_side=[id])

    def __repr__(self):
        return '<Division(%s, %s)>' % (self.id, self.slug)

    def __unicode__(self):
        return '%s' % self.slug


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

    division = relationship(Division)

    def __repr__(self):
        return '<Segment(%s, %s)>' % (self.id, self.slug)


Text.division = relationship(Division)
Division.segments = relationship(Segment,
                                 collection_class=ordering_list('position'),
                                 order_by=Segment.position)
