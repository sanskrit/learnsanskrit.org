from flask import Blueprint, current_app as app, render_template
from jinja2.exceptions import TemplateNotFound

from lso.guide.models import Lesson

debug = Blueprint('debug', __name__, url_prefix='/debug')


@debug.route('/css/')
def css():
    return render_template('debug/css.html')


@debug.route('/guide/')
def guide():
    def has_template(lesson):
        path = 'guide/content/{}.html'.format(lesson.slug)
        try:
            app.jinja_env.get_or_select_template(path)
            return True
        except TemplateNotFound:
            return False

    all_lessons = Lesson.query.all()
    finished = [L for L in all_lessons if has_template(L)]
    todo = [L for L in all_lessons if not has_template(L)]

    return render_template('debug/guide.html', finished=finished, todo=todo)
