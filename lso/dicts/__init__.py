from flask import Blueprint

dicts = Blueprint('dicts', __name__, static_folder='static', template_folder='templates')

import views
