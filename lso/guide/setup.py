#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
import os
import re
import yaml

import lso.database
import lso.util
from .models import _Lesson, Lesson

__all__ = ['run']

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def build_graph():
    """Load the lesson graph and populate any missing fields."""
    with open(os.path.join(DATA_DIR, 'guide.json')) as f:
        json_data = json.loads(lso.util.json_minify(f.read()))
        for lesson in json_data:
            if 'slug' not in lesson:
                lesson['slug'] = slugify(lesson['name'])
        return json_data


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
        if w:
            returned.append(w)
    return '-'.join(returned).lower()


def add_lessons(graph_data, sessionclass=None):
    """Store the lesson DAG in the database.

    :param graph_data: the lesson DAG, as Python data
    :param sessionclass: some session class
    """
    lesson_map = {}
    session = sessionclass() if sessionclass else lso.database.session

    for datum in graph_data:
        lesson = Lesson(name=datum['name'], slug=datum['slug'])
        session.add(lesson)
        lesson_map[datum['slug']] = lesson

    for datum in graph_data:
        slug = datum['slug']
        deps = [lesson_map[dep] for dep in datum['deps']]
        lesson_map[slug].add_dependencies(*deps)

    session.commit()


def init_lessons(filename):
    session = lso.database.session
    def handle(stubs, parent=None):
        lesson = None
        for stub in stubs:
            title = stub['title']
            try:
                slug = stub['slug']
            except KeyError:
                slug = slugify(title)

            lesson = _Lesson(parent=parent,
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
    if not _Lesson.query.count():
        init_lessons('guide.yml')
