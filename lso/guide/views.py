from flask import render_template

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
def unit(unit):
    pass

@guide.route('/<unit>/<lesson>')
def lesson(unit, lesson):
    pass
