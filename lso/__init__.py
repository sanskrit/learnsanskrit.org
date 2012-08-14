from flask import Flask

app = Flask(__name__)
app.config.from_object('config.development')

import lso.common.views

from guide import guide
app.register_blueprint(guide, url_prefix='/guide')
