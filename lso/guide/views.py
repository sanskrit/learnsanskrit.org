from flask import Blueprint, render_template

from lso import app

guide = Blueprint('guide', __name__, static_folder='static', template_folder='templates')
