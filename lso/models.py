from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

db = SQLAlchemy


class DictionaryEntry(db.Model):
    id = Column(Integer, primary_key=True)
    #: Normalized key
    key = Column(String, index=True, nullable=False)
    #: The dictionary headword as printed
    name = Column(String, nullable=False)
    #: The page and column number of the entry
    location = Column(String, nullable=False)
    #: The definition associated with this entry. This is an XML blob.
    content = Column(Text, nullable=False)
