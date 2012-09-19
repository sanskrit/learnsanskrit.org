from flask import Flask
from flask.ext.assets import Bundle, Environment
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config.development')

# Assets
# ------
assets = Environment(app)
assets.url = '/static'

less_files = ['css/%s.less' % x
              for x in 'base'.split()]
less = Bundle(*less_files, filters='less', output='gen/style.css', debug=False)
assets.register('all-css', less)

js = Bundle('js/jquery-plugins.js', 'js/sanscript.js',
            'js/setup.js', output='gen/scripts.js')
assets.register('all-js', js)

# Mail
# ----
mail = Mail(app)

# Views
# -----
import views

from guide import guide
from site import site
from tools import tools
app.register_blueprint(guide, url_prefix='/guide')
app.register_blueprint(site)
app.register_blueprint(tools, url_prefix='/tools')
