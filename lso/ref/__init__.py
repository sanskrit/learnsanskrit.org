from flask import Blueprint

ref = Blueprint('ref', __name__, static_folder='static', template_folder='templates')

import views
