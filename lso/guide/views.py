from flask import render_template

from . import guide
                  
@guide.route('/')
def index():
    return render_template('guide/index.html')
