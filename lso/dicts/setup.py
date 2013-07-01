import os
import re
import yaml
from xml.etree import ElementTree as ET

from lso import app
from ..database import session, engine
from .models import MonierEntry

MONIER_DIR = app.config['MONIER_DIR']
MONIER_XML = os.path.join(MONIER_DIR, 'monier.xml')
MW_FINAL = os.path.join(MONIER_DIR, 'mw-final.xml')
GREEK_YML = os.path.join(MONIER_DIR, 'greek.yml')


def preprocess():
    # Map from line numbers to lists of Greek words in beta code
    with open(GREEK_YML) as f:
        greek = yaml.load(f)
        greek = {x['num']: x['greek'] for x in greek}

    f = open(os.path.join(MONIER_XML), 'r')
    g = open(os.path.join(MW_FINAL), 'w')
    i = 0

    for line in f.readlines():
        try:
            xml = ET.fromstring(line)
        except ET.ParseError:
            g.write(line)
            continue

        h = xml.find('h')
        body = xml.find('body')
        name = h.find('key1').text

        # Set beta code
        L = xml.find('tail/L').text
        betas = greek.get(L, []) or greek.get(L + '0', [])
        for b, gk in zip(betas, body.findall('.//gk')):
            gk.text = b

        g.write(ET.tostring(xml))
        g.write("\n")

        i += 1
        if i % 1000 == 0:
            print "    {0}: {1}".format(i, name)

    f.close()
    g.close()


def init_monier():
    """Initialize the Monier-Williams dictionary."""

    if not os.path.isfile(MW_FINAL):
        preprocess()

    session_add = session.add
    re_entry = re.compile('<key1>(.*)</key1>.*(<body>.*</body>)')

    with open(MW_FINAL) as f:
        id = 1

        # MW entries are at 4 hierarchical levels, plus a "null"
        # level. All entries are wrapped in one of these levels.
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

        for line in f:
            results = re_entry.search(line)
            if results is None:
                continue

            name = results.group(1)
            content = results.group(2)

            e = MonierEntry(id=id, name=name, content=content)
            session_add(e)

            id += 1
            if id % 1000 == 0:
                print "    {0}: {1}".format(id, name)
                session.flush()

    session.commit()


def run():
    if not MonierEntry.query.count():
        init_monier()
