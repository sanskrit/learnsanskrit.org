#!/usr/bin/env python3

"""
Freeze the app into a static site.
"""

import glob
import os

from flask_frozen import Freezer

from lso import app


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'build')


app.debug = False
freezer = Freezer(app)
app.config['FREEZER_DESTINATION'] = OUTPUT_DIR
app.config['FREEZER_RELATIVE_URLS'] = False
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = False


@freezer.register_generator
def all_pages():
    for path in glob.glob('lso/templates/grammar/**/*', recursive=True):
        if not os.path.isdir(path):
            if path.endswith('/index.html'):
                path = path[:-len('index.html')]
            path = path[len('/lso/templates/grammar'):]
            yield f'/{path}'

    yield '/tools/ocr/'
    yield '/tools/sanscript/'


if __name__ == '__main__':
    freezer.freeze()
    print('Written to: ' + OUTPUT_DIR)

