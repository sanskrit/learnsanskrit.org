from flask import Blueprint, Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.mail import Mail
from flask.ext.markdown import Markdown
from flask.ext.security import Security, SQLAlchemyUserDatastore

from sanskrit import Context, analyze, query
import sqlalchemy

app = Flask(__name__)
app.config.from_object('development.config')
try:
    app.config.from_object('server.config')
except ImportError:
    pass


# Assets
# ------
assets = Environment(app)
assets.url = '/static'
assets.directory = app.config['STATIC_DEST']

less_files = ['css/%s.less' % x
              for x in 'base'.split()]
less = Bundle(*less_files, filters='less', output='gen/style.css', debug=False)
assets.register('all-css', less)

js = Bundle(
            # Plugins
            'js/jquery-plugins.js',
            'js/jquery.cookie.js',
            'js/tooltips.js',
            'js/sanscript.js',
            'js/d3-modules.js',
            # Base
            'js/models.js',
            'js/views.js',
            'js/app.js',
            'js/core.js',
            'js/util.js',
            # Setup
            'js/setup.js',
            output='gen/scripts.js')
assets.register('all-js', js)


# Admin
# -----
import admin


# Mail
# ----
mail = Mail(app)


# Markdown
# --------
md = Markdown(app, extensions=['admonition'])
from ext_markdown import SanskritExtension
md.register_extension(SanskritExtension)


# Sanskrit
# --------
ctx = Context(app.config)
try:
    simple_query = query.SimpleQuery(ctx)
    simple_analyzer = analyze.SimpleAnalyzer(ctx)
except sqlalchemy.exc.ProgrammingError:
    simple_query = None
    simple_analyzer = None


# Logging
# -------
if not app.debug:
    import logging
    from logging import FileHandler, getLogger

    print app.config['LOGFILE']
    handler = FileHandler(app.config['LOGFILE'])
    handler.setLevel(logging.WARNING)
    for L in [app.logger, getLogger('sqlalchemy')]:
        L.addHandler(handler)


# Security
# --------
from lso.users.models import User, Role
import database as db

datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, datastore)


# Converters
# ----------
from lso.lib import converters
app.url_map.converters['list'] = converters.ListConverter


# Views and blueprints
# --------------------
import views
import importlib


def register(bp):
    m = importlib.import_module('lso.%s.views' % bp)
    for name in dir(m):
        item = getattr(m, name)
        if isinstance(item, Blueprint):
            app.register_blueprint(item)


register('dicts')
register('guide')
register('ref')
register('site')
register('texts')
register('tools')
register('users')
