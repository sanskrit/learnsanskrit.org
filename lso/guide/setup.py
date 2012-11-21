#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import re
import yaml

from ..database import session
from .models import Lesson

__all__ = ['run']

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(title):
    """Slugify a title. This title might contain IAST characters or HTML."""

    iast = u'ā ī ū ṛ ṝ ṅ ñ ṭ ḍ ṇ ś ṣ'.split()
    readable = 'a i u r r n n t d n sh sh'.split()
    trans = dict(zip(iast, readable))

    # Remove HTML and clean up IAST
    preslug = re.sub('<.*?>', '', title).lower().replace('-', '')
    preslug = ''.join([trans.get(x, x) for x in preslug])

    returned = []
    for w in _punct_re.split(preslug):
        returned.append(w)
    return '-'.join(returned).lower()


def init_lessons(filename):
    def handle(stubs, parent=None):
        lesson = None
        for stub in stubs:
            title = stub['title']
            try:
                slug = stub['slug']
            except KeyError:
                slug = slugify(title)

            lesson = Lesson(parent=parent,
                            slug=slug,
                            title=title)
            session.add(lesson)

            try:
                handle(stub['children'], lesson)
            except KeyError:
                pass

    data = yaml.load(open(os.path.join(DATA_DIR, filename)))
    handle(data)
    session.commit()


def run():
    if not Lesson.query.count():
        init_lessons('guide.yml')
