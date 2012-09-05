from flask import render_template

from . import site

@site.route('/about')
def about():
    return render_template('site/about.html')

@site.route('/contact')
def contact():
    return render_template('site/contact.html')

@site.route('/site')
def index():
    return render_template('site/index.html')

@site.route('/resources')
def resources():
    return render_template('site/resources.html')
