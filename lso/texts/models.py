# -*- coding: utf-8 -*-
"""
    lso.texts.models
    ~~~~~~~~~~~~~~~~

    Models for handling a collection of segmented texts

    :license: MIT and BSD
"""

import sqlalchemy.exc
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import Text as _Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list

from ..database import SimpleBase, BaseNode


CASCADE_ARGS = 'all,delete,delete-orphan'


class Language(SimpleBase):

    """The language of some :class:`Text`"""

    #: A human-readable name for the language, e.g. `Sanskrit`.
    name = Column(String)
    #: A slug for the language, e.g. `sanskrit`
    slug = Column(String)

    def __repr__(self):
        return "<Language(%s, '%s')>" % (self.id, self.slug)

    def __unicode__(self):
        return self.name


class Author(SimpleBase):

    """The author of some :class:`Text`"""

    # The author's name
    name = Column(String)
    #: The author's main language
    language_id = Column(ForeignKey(Language.id))
    #: A human-readable identifier for this author
    slug = Column(String, unique=True)

    language = relationship(Language)

    def __repr__(self):
        return "<Author(%s, '%s')>" % (self.id, self.name)

    def __unicode__(self):
        return self.name


class Text(SimpleBase):

    """A complete text, whether Sanskrit or otherwise."""

    id = Column(Integer, primary_key=True)

    #: A human-readable title in roman letters.
    name = Column(String)
    #: A human-readable identifier
    slug = Column(String, unique=True)
    #: An XML prefix for the text (for XML conversion)
    xmlid_prefix = Column(String, unique=True)

    #: The text's primary language
    language_id = Column(ForeignKey(Language.id))
    #: The text's author
    author_id = Column(ForeignKey(Author.id))
    #: The division tree associated with the text
    division_id = Column(Integer, ForeignKey('division.id'), nullable=True)
    #: The text's parent, if defined
    parent_id = Column(Integer, ForeignKey('text.id'), nullable=True)

    language = relationship(Language)
    author = relationship(Author)
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

    """Association between parent and child segments.

    This class supports a many-to-many relationship between segments in
    parent and child texts. For example, a Sanskrit verse could be
    translated by multiple English stanzas. Or an English verse could
    represent multiple verses in the Sanskrit.

    `text_id` refers only to the child text. This model assumes that
    parent texts and child texts have a 1:M relationship. So far, that
    assumption seems to be a good one.
    """

    #: The ID of the parent segment
    parent_id = Column(ForeignKey('segment.id'), primary_key=True)
    #: The ID of the child text.
    text_id = Column(ForeignKey('text.id'), primary_key=True)
    #: The ID of the child segment. Also, `child.text_id == text_id`.
    child_id = Column(ForeignKey('segment.id'), primary_key=True)

    parent = relationship('Segment',
                          primaryjoin='SegSegAssoc.parent_id==Segment.id',
                          foreign_keys=[parent_id],
                          backref=backref('child_assocs',
                                          cascade=CASCADE_ARGS))
    text = relationship('Text')
    child = relationship('Segment',
                         primaryjoin='SegSegAssoc.child_id==Segment.id',
                         foreign_keys=[child_id],
                         backref=backref('parent_assocs',
                                         cascade=CASCADE_ARGS))

    def __repr__(self):
        return '<SegSegAssoc(%s,%s,%s)>' % (self.parent_id, self.child_id,
                                            self.text_id)


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
    """Drop the models defined above."""

    order = [SegSegAssoc, Segment, Text, Division, Author, Language]
    for o in order:
        try:
            o.__table__.drop()
        except sqlalchemy.exc.ProgrammingError:
            print '(table %s does not exist.)' % o.__tablename__
