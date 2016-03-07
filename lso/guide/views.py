import json
import os

import jinja2.exceptions
from flask import abort, current_app, Response, redirect, render_template, url_for

from lso import cache
from lso.guide import util
from lso.util import LSOBlueprint
from .models import Lesson, Unit

import filters


bp = LSOBlueprint('guide', __name__, url_prefix='/guide')


def exercises_path_for_slug(slug):
    """Given `slug`, return the path where we expect to find exercises.

    The path is not guaranteed to exist.

    :param slug: a lesson slug
    """
    exercises_tail = 'guide/exercises/{}.json'.format(slug)
    return os.path.join(current_app.template_folder, exercises_tail)


@bp.route('/')
@cache.cached(timeout=86400)
def index():
    """This function checks whether a lesson has exercises by reading
    a bunch of files. This is obviously hacky and slow. But it's good
    enough for now.
    """
    units = Unit.query.order_by(Unit.position).all()
    parts = {}
    for u in units:
        parts.setdefault(u.part_name, []).append(u)
    return render_template('guide/index.html', parts=parts)


@bp.route('/<slug>')
@cache.cached(timeout=86400)
def lesson(slug):
    lesson = Lesson.query.filter(Lesson.slug == slug).first()
    if lesson is not None:
        try:
            exercises_tail = 'guide/exercises/{}.json'.format(lesson.slug)
            ex_path = os.path.join(current_app.template_folder, exercises_tail)
            with open(ex_path) as f:
                exercises = json.load(f)
        except IOError:
            exercises = None

        kw = {
            'lesson': lesson,
            'content_path': 'guide/content/{}.html'.format(lesson.slug),
            'exercises': exercises
        }
        return render_template('guide/lesson.html', **kw)

    else:
        abort(404)


@bp.route('/<slug>:exercises')
def exercises(slug):
    try:
        ex_path = exercises_path_for_slug(slug)
        with open(ex_path) as f:
            exercises = json.load(f)
            return Response(json.dumps(exercises), mimetype='application/json')
    except IOError:
        return Response('{}', mimetype='application/json')
