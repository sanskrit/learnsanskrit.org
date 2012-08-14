from flask import Blueprint

guide = Blueprint('guide', __name__,
                  static_folder='static',
                  template_folder='templates')

import views
