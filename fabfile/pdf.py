import os

from fabric.api import *
from flask.ext import weasyprint as WP

from lso import app
from lso.guide.models import Lesson


def lesson_tree():
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
    return units


@task
def create(*units):
    units = set(units)
    with app.test_request_context(base_url='http:///'):
        for unit in lesson_tree():
            if units and unit.slug not in units:
                continue
            url = '/guide/%s/all' % unit.slug
            path = 'guide/static/pdf/%s.pdf' % unit.slug
            path = os.path.join(app.root_path, path)
            page = WP.HTML(url)
            with open(path, 'w') as f:
                page.write_pdf(f)

        url = '/guide/all'
        path = os.path.join(app.root_path, 'guide/static/pdf/guide.pdf')
        page = WP.HTML(url)
        with open(path, 'w') as f:
            page.write_pdf(f)
