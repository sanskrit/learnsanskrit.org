from flask import Flask
from flask_assets import Environment, Bundle

from lso.views import bp


app = Flask(__name__)

assets = Environment(app)
css = Bundle('css/style.css', 'css/style-new.css', output='gen/style.css')
assets.register('css_all', css)

app.register_blueprint(bp)
