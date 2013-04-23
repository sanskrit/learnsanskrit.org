from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.mail import Mail

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

# Mail
# ----
mail = Mail(app)

# Sanskrit
# --------
ctx = Context(app.config)
try:
    simple_query = query.SimpleQuery(ctx)
    simple_analyzer = analyze.SimpleAnalyzer(ctx)
except sqlalchemy.exc.ProgrammingError:
    simple_query = None
    simple_analyzer = None

# logging
# -------
if not app.debug:
    import logging
    from logging import FileHandler, getLogger
    handler = FileHandler(app.config['LOGFILE'])
    handler.setLevel(logging.WARNING)
    for L in [app.logger, getLogger('sqlalchemy')]:
        L.addHandler(handler)

# Views
# -----
import views

from dicts import dicts
from guide import guide
from ref import ref
from site import site
from tools import tools
app.register_blueprint(dicts, url_prefix='/dict')
app.register_blueprint(guide, url_prefix='/guide')
app.register_blueprint(ref, url_prefix='/ref')
app.register_blueprint(site)
app.register_blueprint(tools, url_prefix='/tools')
