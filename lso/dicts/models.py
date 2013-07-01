from sqlalchemy import Column, String, Text
from ..database import SimpleBase


class MonierEntry(SimpleBase):

    """A dictionary entry from the Monier-Williams dictionary."""

    #: A word written in unaccented SLP1
    name = Column(String, index=True)
    #: The page and column number of the entry
    location = Column(String)
    #: The definition associated with this entry. This is an XML blob.
    content = Column(Text)

    def __repr__(self):
        return "<MonierEntry(%s,'%s')>" % (self.id, self.entry)

    def __unicode__(self):
        return self.name


def drop():
    """Drop the models defined above."""
    models = [MonierEntry]
    for m in models:
        m.__table__.drop()
