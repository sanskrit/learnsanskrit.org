import pathlib
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


DATABASE_URI = "sqlite:///database.db"

metadata = MetaData()

dict_entries = Table(
    "dict_entries",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("key", String, index=True, nullable=False),
    Column("value", String, nullable=False),
)

sanskrit_words = Table(
    "sanskrit_words",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("key", String, index=True, nullable=False),
    Column("headword", String, nullable=False),
    Column("parse", String, nullable=False),
)
