import jinja2.exceptions

from flask import abort, redirect, render_template, url_for

from lso.guide import util
from lso.lib import LSOBlueprint
from .models import Lesson

import filters


bp = LSOBlueprint('guide', __name__, url_prefix='/guide')


@bp.route('/')
def index():
    sorted_lessons = util.lesson_sort(Lesson.query.all())
    return render_template('guide/index.html', lessons=sorted_lessons)


@bp.route('/<slug>')
def lesson(slug):
    lesson = Lesson.query.filter(Lesson.slug == slug).first()
    if lesson is not None:
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
