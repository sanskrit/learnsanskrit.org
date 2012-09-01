from flask import Flask
from flask.ext.assets import Bundle, Environment

app = Flask(__name__)
app.config.from_object('config.development')

# Assets
# ------
assets = Environment(app)
assets.url = '/static'

# Force automatic updates in development
if app.debug:
    assets.manifest = None
    assets.cache = False
    assets.updater = False

less_files = ['css/%s.less' % x
              for x in 'base'.split()]
less = Bundle(*less_files, filters='less', output='gen/style.css', debug=False)
assets.register('all-css', less)

# Views
# -----
import lso.common.views

from guide import guide
from tools import tools
app.register_blueprint(guide, url_prefix='/guide')
app.register_blueprint(tools, url_prefix='/tools')
