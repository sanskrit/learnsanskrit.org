#!/usr/bin/env python3

"""Add the MW dictionary to the database."""

import pathlib
import sys
from sqlalchemy import create_engine
from xml.etree import ElementTree as ET


def iter_xml(mw_path: str):
    """Yield all entries in the dictionary. Keys might repeat.

    :param mw_path: path to the XML version of the dictionary
    """
    root = ET.parse(mw_path).getroot()

    for child in root:
        # Sanity check
        tag_str = (
            "H1 H1A H1B H1C H1E H2 H2A H2B H2C H2E "
            "H3 H3A H3B H3C H3E H4 H4A H4B H4C H4E"
        )
        allowed_tags = set(tag_str.split())
        assert child.tag in allowed_tags, child.tag

        key = None
        for elem in child.iter():
            if elem.tag == "key1":
                key = elem.text
                break
        value = ET.tostring(child, encoding="utf-8")

        assert key
        assert value
        yield key, value


def create_db(project_dir: str, mw_path: str):
    sys.path.insert(0, project_dir)

    from lso.database import DATABASE_URI, dict_entries, metadata

    engine = create_engine(DATABASE_URI)
    metadata.create_all(engine)

    ins = dict_entries.insert()
    print("Adding items to the database. This takes about 30 seconds ...")
    with engine.connect() as conn:
        items = [{"key": key, "value": value} for key, value in iter_xml(mw_path)]
        conn.execute(ins, items)
    print("Done.")


def main():
    project_dir = pathlib.Path(__file__).parent.parent
    mw_path = project_dir.joinpath("db_data", "monier-williams.xml")

    create_db(str(project_dir), mw_path)


if __name__ == "__main__":
    main()
