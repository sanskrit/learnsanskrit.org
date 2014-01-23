import jinja2.exceptions

from flask import abort, redirect, render_template, url_for


from lso.guide import util
from lso.lib import LSOBlueprint
from .models import Lesson, _Lesson

bp = LSOBlueprint('guide', __name__, url_prefix='/guide')

import filters


def lesson_sort(lessons):
    """Returns a topological sort of a list of lessons.

    Ties are broken arbitrarily.

    :param lessons: a list of lessons
    """
    slug_map = {lesson.slug: lesson for lesson in lessons}
    slug_graph = {lesson.slug: [succ.slug for succ in lesson.successors()]
                  for lesson in lessons}
    sorted_slugs = util.topological_sort(slug_graph)
    return [slug_map[slug] for slug in sorted_slugs]


@bp.route('/')
def index():
    sorted_lessons = lesson_sort(Lesson.query.all())
    return render_template('guide/index.html', lessons=sorted_lessons)


@bp.route('/<slug>')
def lesson(slug):
    lesson = Lesson.query.filter(Lesson.slug==slug).first()
    if lesson:
        try:
            kw = {
                'lesson': lesson,
                'content_path': 'guide/content/{}.html'.format(lesson.slug)
            }
            return render_template('guide/lesson.html', **kw)
        except jinja2.exceptions.TemplateNotFound:
            return render_template('guide/placeholder.html', lesson=lesson)
    else:
        abort(404)
