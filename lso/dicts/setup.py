import os
import re

from lso import app
from ..database import session
from .models import MonierEntry

def init_monier():
    """Initialize the Monier-Williams dictionary."""

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

    entry_tags = levels.keys()

    exp_key1 = re.compile('<key1>(.*?)</key1>')
    exp_key2 = re.compile('<key2>(.*?)</key2>')
    exp_body = re.compile('<body>.*</body>')

    f = open(app.config['MONIER_XML'], 'r')
    i = 0

    for line in f.readlines():
        try:
            unaccented_entry = exp_key1.search(line).group(1)
            accented_entry = exp_key2.search(line).group(1)
            data = exp_body.search(line).group(0)
        except AttributeError:
            continue

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
