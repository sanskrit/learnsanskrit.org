#!/usr/bin/env python3

"""

Add Dr. Dhaval Patel's verb data to the database.

Data format:

    <f form="aMsayati"><root name="aMsa" num="10.0460"/><law/><tip/></f>

"""

import pathlib
import re
import sys

from sqlalchemy import create_engine
from xml.etree import ElementTree as ET


CONSONANTS = "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"


def num_agama(dhatu: str) -> str:
    vargas = ["kKgGN", "cCjJY", "wWqQR", "tTdDn", "pPbBm", "yrlvSzshM"]

    buf = []
    # Iterate in reverse to get vowel following vowel
    for L in dhatu[::-1]:
        if L in CONSONANTS:
            buf.append(L)
        else:
            assert buf
            next = buf[-1]
            for varga in vargas:
                if next in varga:
                    buf.append(varga[-1])
            buf.append(L)
    return "".join(buf[::-1])


def remove_its(dhatu: str) -> str:
    """it-samjna-prakaranam."""

    # Special case
    if dhatu.endswith("i!r"):
        dhatu = dhatu[:-3]
    elif dhatu[-1] in CONSONANTS:
        dhatu = dhatu[:-1]

    # Nasal vowels
    if dhatu.endswith("i!"):
        dhatu = num_agama(dhatu[:-2])
    dhatu = re.sub("[aAIuUfxeo]!", "", dhatu)

    if any(dhatu.startswith(x) for x in ("Yi", "wu", "qu")):
        dhatu = dhatu[2:]

    # dhatu-adi
    if dhatu.startswith("z"):
        dhatu = "s" + dhatu[1:]
    if dhatu.startswith("R"):
        dhatu = "n" + dhatu[1:]

    assert "!" not in dhatu, dhatu
    return dhatu


def process_f_xml(elem):
    form = elem.attrib["form"]
    headword = None
    tense_mood = None
    ending = None

    lakaras = {
        "law",
        "liw",
        "luw",
        "lfw",
        "low",
        "laN",
        "ASIrliN",
        "viDiliN",
        "luN",
        "lfN",
    }

    for child in elem.iter():
        name = child.tag
        if name == "f":
            continue
        elif name == "root":
            headword = child.attrib["name"]
        elif name in lakaras:
            tense_mood = name
        else:
            ending = name

    fields = (form, headword, tense_mood, ending)
    assert all(fields), fields
    return fields


def iter_xml(xml_path: str):
    """Yield all entries in the data file.

    :param xml_path: path to the data
    """

    ending_list = [
        "tip",
        "tas",
        "Ji",
        "sip",
        "Tas",
        "Ta",
        "mip",
        "vas",
        "mas",
        "ta",
        "AtAm",
        "Ja",
        "TAs",
        "ATAm",
        "Dvam",
        "iw",
        "vahi",
        "mahiN",
    ]
    persons = {}
    numbers = {}
    padas = {}
    for i, e in enumerate(ending_list):
        persons[e] = "321"[(i // 3) % 3]
        numbers[e] = "sdp"[i % 3]
        padas[e] = "pa"[i // 9]

    xml_root = ET.parse(xml_path).getroot()

    for child in xml_root:
        if child.tag != "f":
            continue

        form, headword, tense_mood, ending = process_f_xml(child)
        headword = remove_its(headword)
        person = persons[ending]
        number = numbers[ending]
        pada = padas[ending]
        parse = f"p:{person} n:{number} l:{tense_mood} a:{pada}"
        yield form, headword, parse


def create_db(project_dir: str, xml_path: str):
    sys.path.insert(0, project_dir)

    from lso.database import DATABASE_URI, sanskrit_words, metadata

    engine = create_engine(DATABASE_URI)
    with engine.connect() as conn:
        print("Removing old entries ...")
        sanskrit_words.drop(engine)

        print("Creating new table ...")
        metadata.create_all(engine)

        print("Adding items to the database ...")
        items = []
        for form, headword, parse in iter_xml(xml_path):
            items.append({"key": form, "headword": headword, "parse": parse})
        conn.execute(sanskrit_words.insert(), items)

    print("Done.")


def main():
    project_dir = pathlib.Path(__file__).parent.parent
    xml_path = project_dir.joinpath("db_data", "dhaval-verbs.xml")
    create_db(str(project_dir), xml_path)


if __name__ == "__main__":
    main()
