from flask import render_template

from . import tools

@tools.route('/')
def index():
    return render_template('tools/index.html')
