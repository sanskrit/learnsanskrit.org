from flask import Flask

app = Flask(__name__)
app.config.from_object('config.development')

import lso.common.views

from guide.views import guide
app.register_blueprint(guide, url_prefix='/guide')

print app.url_map
