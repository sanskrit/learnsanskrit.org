from flask import redirect, render_template, url_for

import filters
from . import guide
from .models import Lesson

@guide.route('/')
def index():
    roots = Lesson.query.filter(Lesson.parent_id==None).all()
    guide_root = next(x for x in roots if x.slug == '')

    lessons = guide_root.mp.query_descendants().all()
    unit = None
    units = []
    for L in lessons:
        if L.mp_depth == 1:
            unit = L
            units.append(unit)
            unit.children = []
        else:
            unit.children.append(L)

    return render_template('guide/index.html', units=units)

@guide.route('/<unit>')
def unit(**kwargs):
    unit_slug = kwargs.pop('unit')

    unit = Lesson.query.filter(Lesson.slug==unit_slug).first()
    if unit:
        unit.children = unit.mp.query_descendants().all()
        return render_template('guide/unit.html', unit=unit)
    else:
        return redirect(url_for('guide.index'))

@guide.route('/<unit>/<lesson>')
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
    return render_template(template, lesson=lesson, prev=prev, next=next,
                           unit=unit)
