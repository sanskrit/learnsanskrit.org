import itertools
from typing import List, Dict
from dataclasses import dataclass

from flask import Blueprint, jsonify

from sqlalchemy import create_engine
from sqlalchemy.sql import *
import lso.database as db
from lso.api.util import normalize_key
from lso.api.xml_transform import transform_mw


bp = Blueprint("api", __name__, url_prefix="/api")


@dataclass
class DhavalWord:
    headword: str
    parse: Dict[str, str]


@dataclass
class MWEntry:
    content: str


def query_mw(key: str) -> List[MWEntry]:
    """Query the MW dictionary data."""

    engine = create_engine(db.DATABASE_URI)
    with engine.connect() as conn:
        table = db.dict_entries
        q = select([table]).where(table.c.key == key)
        rows = conn.execute(q).fetchall()

    # Manual group-by. TODO: can this be done in sqla?
    res = []
    for row in rows:
        payload = transform_mw(row.value.decode("utf-8"))
        res.append(MWEntry(content=payload))
    return res


def query_parses(key: str) -> List[DhavalWord]:
    """Query the Sanskrit word data."""

    engine = create_engine(db.DATABASE_URI)
    with engine.connect() as conn:
        # Select unique for queries like `kariSyati` which have multiple
        # realizations. This is simpler but good for beginners.
        c = db.sanskrit_words.c
        q = select([c.key, c.headword, c.parse]).where(c.key == key).distinct()
        rows = conn.execute(q).fetchall()

    res = []
    for r in rows:
        parse_dict = {}
        for entry in r.parse.split():
            k, v = entry.split(":")
            parse_dict[k] = v
        parse_dict["type"] = "v"

        res.append(
            DhavalWord(
                headword=r.headword,
                parse=parse_dict,
            )
        )

    return res


def query_paradigms(key: str):
    engine = create_engine(db.DATABASE_URI)
    with engine.connect() as conn:
        # Select unique for queries like `kariSyati` which have multiple
        # realizations. This is simpler but good for beginners.
        c = db.sanskrit_words.c
        q = select([c.key, c.headword, c.parse]).where(c.headword == key)
        rows = conn.execute(q).fetchall()

    res = []
    for r in rows:
        parse_dict = {}
        for entry in r.parse.split():
            k, v = entry.split(":")
            parse_dict[k] = v
        parse_dict["type"] = "v"

        res.append(
            DhavalWord(
                headword=r.headword,
                parse=parse_dict,
            )
        )

    return res


@bp.route("/pandit/<q>")
def pandit(q):
    """
    Main API call. Words to check on for quality:

    - kariSyati
    - tena
    """
    key = q.strip()
    if not key:
        return {}

    parses = query_parses(key)
    mw = query_mw(key)

    return jsonify(
        {
            "key": key,
            "parses": parses,
            "mw": mw,
        }
    )
