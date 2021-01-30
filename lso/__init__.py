from flask import Flask

from lso.views import bp


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.register_blueprint(bp)
