from flask import Blueprint

site = Blueprint('site', __name__, static_folder='static', template_folder='templates')

import views
