import os

from flask import Flask, after_this_request, render_template, request


app = Flask(__name__, static_url_path='/static', static_folder='snapshot/static')


def get_folder(url_rule) -> str:
    tokens = str(url_rule).split('/')
    for t in tokens:
        if t:
            return t


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/preferences/')
def preferences():
    return render_template('preferences.html')


@app.route('/resources/')
def resources():
    return render_template('resources.html')


@app.route('/supp/')
def supp():
    return render_template('supp.html')


@app.route('/tools/')
def tools():
    return render_template('tools.html')


@app.route('/use/')
def use():
    return render_template('use.html')


@app.route('/ends/')
@app.route('/grammar/')
@app.route('/introduction/')
@app.route('/monier/')
@app.route('/nouns/')
@app.route('/nouns/')
@app.route('/panini/')
@app.route('/prosody/')
@app.route('/references/')
@app.route('/sounds/')
@app.route('/start/')
@app.route('/supp/')
@app.route('/texts/')
@app.route('/tools/')
@app.route('/verbs/')
def indices():
    folder = get_folder(request.url_rule)
    abspath = os.path.join('snapshot', folder, 'index.html')
    with open(abspath) as f:
        return f.read()


@app.route('/ends/<path:filepath>')
@app.route('/grammar/<path:filepath>')
@app.route('/introduction/<path:filepath>')
@app.route('/monier/<path:filepath>')
@app.route('/nouns/<path:filepath>')
@app.route('/panini/<path:filepath>')
@app.route('/prosody/<path:filepath>')
@app.route('/references/<path:filepath>')
@app.route('/sounds/<path:filepath>')
@app.route('/start/<path:filepath>')
@app.route('/supp/<path:filepath>')
@app.route('/texts/<path:filepath>')
@app.route('/tools/<path:filepath>')
@app.route('/verbs/<path:filepath>')
def all_pages(filepath):
    folder = get_folder(request.url_rule)
    abspath = os.path.join('snapshot', folder, filepath)
    if os.path.isdir(abspath):
        abspath = os.path.join(abspath, 'index.html')

    with open(abspath) as f:
        return f.read()


if __name__ == '__main__':
    app.run(debug=True)
