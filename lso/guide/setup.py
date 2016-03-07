#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
import os
import re

import lso.database
from lso.util.json import json_minify
from .models import Lesson, LessonEdge, Unit

__all__ = ['run']

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def load_and_add_slugs(filename):
    """Load the given JSON file and add missing slugs."""
    with open(os.path.join(DATA_DIR, filename)) as f:
        json_data = json.loads(json_minify(f.read()))
        for datum in json_data:
            if 'slug' not in datum:
                datum['slug'] = slugify(datum['name'])
        return json_data



def build_graph():
    """Load the lesson graph and populate any missing fields."""
    return load_and_add_slugs('guide.json')


def load_units():
    """Load the units list and populate any missing fields."""
    return load_and_add_slugs('units.json')


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


def add_lessons(graph_data, unit_data, session):
    """Store the lesson DAG in the database.

    :param graph_data: the lesson DAG, as Python data
    :param sessionclass: some session class
    """
    # slug -> Lesson
    lesson_map = {}

    for datum in graph_data:
        lesson = Lesson(name=datum['name'], slug=datum['slug'])
        session.add(lesson)
        lesson_map[datum['slug']] = lesson

    for datum in graph_data:
        slug = datum['slug']
        deps = [lesson_map[dep] for dep in datum['deps']]
        lesson_map[slug].add_dependencies(*deps)

    for u, datum in enumerate(unit_data):
        unit = Unit(name=datum['name'],
                    part_name=datum['part'],
                    position=u)
        session.add(unit)
        for i, slug in enumerate(datum['lessons']):
            lesson_map[slug].unit = unit
            lesson_map[slug].position = i

    session.commit()


def drop(app):
    with app.app_context():
        LessonEdge.__table__.drop(lso.database.db.engine)
        Lesson.__table__.drop(lso.database.db.engine)
        Unit.__table__.drop(lso.database.db.engine)


def run(app=None):
    app = app or lso.create_app(__name__)
    with app.app_context():
        if Lesson.query.count():
            print '`guide` already has data. Exiting...'
        else:
            graph_data = build_graph()
            unit_data = load_units()
            add_lessons(graph_data, unit_data, lso.database.db.session)
