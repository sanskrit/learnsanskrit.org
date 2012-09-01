from flask import Blueprint

tools = Blueprint('tools', __name__, static_folder='static',
                  template_folder='templates')

import views
