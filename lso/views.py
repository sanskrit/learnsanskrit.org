import os

from flask import Blueprint, after_this_request, render_template, request

from lso import data


bp = Blueprint('site', __name__)


def get_folder(url_rule) -> str:
    tokens = str(url_rule).split('/')
    for t in tokens:
        if t:
            return t


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/about/')
def about():
    return render_template('about.html')


@bp.route('/contact/')
def contact():
    return render_template('contact.html')


@bp.route('/preferences/')
def preferences():
    return render_template('preferences.html')


@bp.route('/resources/')
def resources():
    return render_template('resources.html')


@bp.route('/supp/')
def supp():
    return render_template('supp.html')


@bp.route('/tools/')
def tools():
    return render_template('tools.html')


@bp.route('/use/')
def use():
    return render_template('use.html')


@bp.route('/grammar/')
def grammar():
    toc = data.TABLE_OF_CONTENTS
    return render_template('grammar/index.html', toc=toc)


@bp.route('/ends/')
@bp.route('/grammar/')
@bp.route('/introduction/')
@bp.route('/monier/')
@bp.route('/nouns/')
@bp.route('/panini/')
@bp.route('/prosody/')
@bp.route('/references/')
@bp.route('/sounds/')
@bp.route('/start/')
@bp.route('/supp/')
@bp.route('/texts/')
@bp.route('/tools/')
@bp.route('/verbs/')
def grammar_index_pages():
    folder = get_folder(request.url_rule)
    path = os.path.join('grammar', folder, 'index.html')
    return render_template(path)


@bp.route('/ends/<path:filepath>')
@bp.route('/grammar/<path:filepath>')
@bp.route('/introduction/<path:filepath>')
@bp.route('/monier/<path:filepath>')
@bp.route('/nouns/<path:filepath>')
@bp.route('/panini/<path:filepath>')
@bp.route('/prosody/<path:filepath>')
@bp.route('/references/<path:filepath>')
@bp.route('/sounds/<path:filepath>')
@bp.route('/start/<path:filepath>')
@bp.route('/supp/<path:filepath>')
@bp.route('/verbs/<path:filepath>')
def all_pages(filepath):
    folder = get_folder(request.url_rule)
    path = os.path.join('grammar', folder, filepath, 'index.html')
    return render_template(path)


@bp.route('/tools/<name>/')
def tools_legacy(name):
    return render_template(f'tools/{name}.html')


@bp.route('/texts/ashtadhyayi/book1-1/')
def ashtadhyayi_legacy():
    return render_template('texts/ashtadhyayi/book1-1.html')
