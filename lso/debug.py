from flask import render_template
from jinja2.exceptions import TemplateNotFound

from lso import app
from lso.guide.models import Lesson

@app.route('/debug/css/')
def debug_css():
    return render_template('debug/css.html')


@app.route('/debug/guide/')
def debug_guide():
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