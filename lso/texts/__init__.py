from flask import Blueprint

texts = Blueprint('texts', __name__, static_folder='static', template_folder='templates')

import views
