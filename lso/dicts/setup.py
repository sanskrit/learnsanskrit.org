import os
import re
import yaml
from xml.etree import ElementTree as ET

from lso import app
from ..database import session
from .models import MonierEntry

MONIER_XML = 'monier.xml'
GREEK_YML = 'greek.yml'

def init_monier():
    """Initialize the Monier-Williams dictionary."""

    # Map from line numbers to lists of Greek words in beta code
    MONIER_DIR = app.config['MONIER_DIR']
    with open(os.path.join(MONIER_DIR, GREEK_YML)) as f:
        greek = yaml.load(f)
        greek = {x['num']: x['greek'] for x in greek}

    # MW entries are at 4 hierarchical levels, plus a "null" level.
    # All entries are wrapped in one of these levels.
    levels = {}
    for k in 'H1 H1A H1B'.split():
        levels[k] = 1
    for k in 'H2 H2A H2B'.split():
        levels[k] = 2
    for k in 'H3 H3A H3B'.split():
        levels[k] = 3
    for k in 'H4 H4A H4B'.split():
        levels[k] = 4
    levels['HPW'] = 0

    f = open(os.path.join(MONIER_DIR, MONIER_XML), 'r')
    i = 0

    for line in f.readlines():
        try:
            xml = ET.fromstring(line)
        except ET.ParseError:
            continue

        h = xml.find('h')
        body = xml.find('body')
        unaccented_entry = h.find('key1').text
        accented_entry = h.find('key2').text

        # Set beta code
        L = xml.find('tail/L').text
        betas = greek.get(L, []) or greek.get(L + '0', [])
        for b, gk in zip(betas, body.findall('.//gk')):
            gk.text = b

        data = ET.tostring(body)
        e = MonierEntry(entry=unaccented_entry, accented=accented_entry,
                        data=data, parent=None)
        session.add(e)

        i += 1
        if i % 1000 == 0:
            print "    {0}: {1}".format(i, unaccented_entry)
            session.commit()

    session.commit()
    f.close()

def run():
    if not MonierEntry.query.count():
        init_monier()
