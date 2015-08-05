import importlib
import os

from flask import Blueprint, Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.cache import Cache
from flask.ext.mail import Mail
from flask.ext.markdown import Markdown
#from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy
import sanskrit
import sanskrit.analyze
import sanskrit.query
import sqlalchemy

import lso.admin
import lso.database
import lso.lib.converters


# Assets (LESS CSS and assorted JavaScript)
assets = Environment()
assets.register('all-css', Bundle('css/base.less', filters='less',
                                  output='gen/style.css', debug=False))
assets.register('all-js', Bundle(
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
    output='gen/scripts.js'))


# Caching
cache = Cache()


# Mail (for contact form)
mail = Mail()


# Logging
def do_logging(app):
    import logging
    from logging import FileHandler, getLogger

    print 'Logging to:', app.config['LOGFILE']
    handler = FileHandler(app.config['LOGFILE'])
    handler.setLevel(logging.WARNING)
    for L in [app.logger, getLogger('sqlalchemy')]:
        L.addHandler(handler)


# Security (for user accounts)
#from lso.users.models import User, Role
#datastore = SQLAlchemyUserDatastore(lso.database.db, User, Role)
#security = Security(datastore=datastore)


# Converters (for fancy dictionary queries)
def add_converters(app):
    app.url_map.converters['list'] = lso.lib.converters.ListConverter


# Blueprints
def register_blueprints(app, *blueprints):
    for bp in blueprints:
        m = importlib.import_module('lso.%s.views' % bp)
        try:
            m.view_setup(bp)
        except AttributeError:
            pass
        for name in dir(m):
            item = getattr(m, name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)


# Filters
import lso.filters as f
import lso.guide.filters as gf
template_filters = [
    f.date,
    f.sa1,
    f.sa2,
    gf.d,
    gf.foot,
    gf.i,
    gf.transliterate_backticks,
    gf.render,
    gf.verb_data,
]


def create_app(name, config_object, override=None):
    """App factory.

    The factory pattern makes unit testing much saner.

    :param name: the name of the app
    :param config_object: path to config object
    """
    app = Flask(name)

    try:
        app.config.from_object(config_object)
    except ImportError:
        print 'ImportError with config object:', config_object
        pass

    if override:
        app.config.update(override)


    # Needed to locate templates and assets in various contexts (runserver,
    # testing, ...)
    # TODO: surely there's a way to avoid this?
    LSO_PATH = os.path.dirname(__file__)
    app.template_folder = os.path.join(LSO_PATH, 'templates')
    app.static_folder = os.path.join(LSO_PATH, 'static')

    # Template filters
    for _filter in template_filters:
        app.add_template_filter(_filter)

    # URL converters
    add_converters(app)

    # Extensions
    lso.admin.admin.init_app(app)

    assets.init_app(app)
    assets.app = app  # TODO: remove hack
    assets.url = '/static'
    assets.directory = app.config['STATIC_DEST']

    cache.init_app(app)

    lso.database.db.init_app(app)

    mail.init_app(app)

    md = Markdown(app, extensions=['admonition'])
    from ext_markdown import SanskritExtension
    md.register_extension(SanskritExtension)

    # security.init_app(app)

    # 'sanskrit' package
    ctx = sanskrit.Context(app.config)
    ctx.connect()
    try:
        simple_query = sanskrit.query.SimpleQuery(ctx)
        simple_analyzer = sanskrit.analyze.SimpleAnalyzer(ctx)
    except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError):
        simple_query = None
        simple_analyzer = None

    # Debug toolbar
    if app.debug:
        from flask.ext.debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)

    # Blueprints
    if app.debug:
        import debug
        app.register_blueprint(debug.debug)
    else:
        do_logging(app)

    import views
    app.register_blueprint(views.main)
    register_blueprints(app,
        'dicts',
        'guide',
        # 'ref',
        'site',
        'texts',
        'tools',
        #'users'
    )

    with app.app_context():
        lso.database.db.create_all()
    return app
