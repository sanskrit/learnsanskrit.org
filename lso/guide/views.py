from flask import Blueprint, render_template

guide = Blueprint('guide', __name__,
                  static_folder='static',
                  template_folder='templates')
                  
@guide.route('/')
def index():
    print 'aoeu'
    return render_template('guide/index.html')
