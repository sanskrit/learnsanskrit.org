import csv
import os
import re
import xml.etree.cElementTree as ET

import lso
import lso.database
from .models import MonierEntry


def get_filenames(app):
    monier_dir = app.config['MONIER_DIR']
    return {
        'monier-raw': os.path.join(monier_dir, 'monier.xml'),
        'monier-final': os.path.join(monier_dir, 'mw-final.xml'),
        'greeklist': os.path.join(monier_dir, 'greeklist.csv')
    }


def preprocess(app):
    files = get_filenames(app)

    # Map from line numbers to lists of Greek words in beta code
    greek = {}
    with open(files['greeklist']) as f:
        reader = csv.DictReader(f)
        for row in reader:
            greek[(row['L'], int(row['index']) - 1)] = row['betacode']

    mw_in = open(files['monier-raw'], 'r')
    mw_out = open(files['monier-final'], 'w')
    count = 0

    for line in mw_in.readlines():
        try:
            xml = ET.fromstring(line)
        except ET.ParseError:
            mw_out.write(line)
            continue

        h = xml.find('h')
        body = xml.find('body')
        name = h.find('key1').text

        # Set beta code
        L = xml.find('tail/L').text
        # betas = greek.get(L, []) or greek.get(L + '0', [])
        for i, gk in enumerate(body.findall('.//gk')):
            gk.text = greek.get((L, i)) or greek.get((L + '0', i))

        mw_out.write(ET.tostring(xml))
        mw_out.write("\n")

        count += 1
        if count % 1000 == 0:
            print "    {0}: {1}".format(count, name)

    mw_in.close()
    mw_out.close()


def init_monier(app):
    """Initialize the Monier-Williams dictionary."""

    files = get_filenames(app)
    if not os.path.isfile(files['monier-final']):
        preprocess(app)

    re_entry = re.compile('<key1>(.*)</key1>.*(<body>.*</body>)')
    session = lso.database.db.session

    with open(files['monier-final']) as f:
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
            session.add(e)

            id += 1
            if id % 1000 == 0:
                print "    {0}: {1}".format(id, name)
                session.flush()

    session.commit()


def run(app=None):
    app = app or lso.create_app(__name__)
    with app.app_context():
        if MonierEntry.query.count():
            print 'Queries already exist. Drop the table first.'
        else:
            init_monier(app)


def drop():
    models = [MonierEntry]
    for m in models:
        m.__table__.drop()
