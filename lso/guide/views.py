from flask import redirect, render_template, url_for

from lso.lib import LSOBlueprint
from .models import Lesson

bp = LSOBlueprint('guide', __name__, url_prefix='/guide')

import filters


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


@bp.route('/')
def index():
    roots = Lesson.query.filter(Lesson.parent_id==None).all()
    units = lesson_tree(roots[0])
    supp = lesson_tree(roots[1])
    return render_template('guide/index.html', units=units, supp=supp)


@bp.route('/help')
def help():
    return render_template('guide/help.html')


@bp.route('/<unit>')
def unit(**kwargs):
    unit_slug = kwargs.pop('unit')

    unit = Lesson.query.filter(Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
        template = 'guide/%s/index.html' % unit_slug
        return render_template(template, cur=unit, unit=unit)
    else:
        return redirect(url_for('guide.index'))


@bp.route('/<unit>/<lesson>')
def lesson(**kwargs):
    unit_slug = kwargs.pop('unit')
    lesson_slug = kwargs.pop('lesson')

    unit = Lesson.query.filter(Lesson.slug==unit_slug).first()
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

    unit = Lesson.query.filter(Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
        return render_template('guide/dump.html', units=[unit])
    else:
        return redirect(url_for('guide.index'))


@bp.route('/all')
def guide_dump(**kwargs):
    root = Lesson.query.filter(Lesson.parent_id==None).first()
    units = lesson_tree(root)
    return render_template('guide/dump.html', units=units)
