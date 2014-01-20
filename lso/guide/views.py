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
            content_path = 'guide/{}.html'.format(lesson.slug)
            return render_template('guide/lesson.html', **kw)
        except jinja2.exceptions.TemplateNotFound:
            return render_template('guide/placeholder.html', lesson=lesson)
    else:
        abort(404)


@bp.route('/help')
def help():
    return render_template('guide/help.html')


def lesson_tree(root):
    lessons = root.mp.query_descendants().all()
    unit = None
    units = []
    for L in lessons:
        if L.mp_depth == 1:
            unit = L
            units.append(unit)
            unit.children = []
        else:
            unit.children.append(L)
    return units


@bp.route('/unit/<unit>')
def _unit(**kwargs):
    unit_slug = kwargs.pop('unit')

    unit = _Lesson.query.filter(_Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
        template = 'guide/%s/index.html' % unit_slug
        return render_template(template, cur=unit, unit=unit)
    else:
        return redirect(url_for('guide.index'))


@bp.route('/<unit>/<lesson>')
def _lesson(**kwargs):
    unit_slug = kwargs.pop('unit')
    lesson_slug = kwargs.pop('lesson')

    unit = _Lesson.query.filter(_Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
    else:
        return redirect(url_for('guide.index'))

    lesson = prev = next = None
    for L in unit.children:
        if lesson:
            next = L
            break
        elif L.slug == lesson_slug:
            lesson = L
        else:
            prev = L

    if not lesson:
        return redirect(url_for('guide.unit', unit=unit_slug))

    template = 'guide/%s/%s.html' % (unit.slug, lesson.slug)
    return render_template(template,
                           cur=lesson, prev=prev, next=next,
                           unit=unit)


@bp.route('/<unit>/all')
def unit_dump(**kwargs):
    unit_slug = kwargs.pop('unit')

    unit = _Lesson.query.filter(_Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
        return render_template('guide/dump.html', units=[unit])
    else:
        return redirect(url_for('guide.index'))


@bp.route('/all')
def guide_dump(**kwargs):
    root = _Lesson.query.filter(_Lesson.parent_id==None).first()
    units = lesson_tree(root)
    return render_template('guide/dump.html', units=units)
