from flask import render_template
from flask.ext.security import login_required, current_user as u

import forms as f
from lso import security
from lso.lib import LSOBlueprint

bp = LSOBlueprint('users', __name__)

security._state.login_form = f.LoginForm
security._state.register_form = f.SignupForm


@login_required
@bp.route('/home')
def home():
    print u.roles
    return render_template('users/home.html')


@login_required
@bp.route('/settings')
def settings():
    return render_template('users/settings.html')

@bp.route('/login')
def login():
    login_form = f.LoginForm()
    signup_form = f.SignupForm()
    return render_template('users/login.html', login_form=login_form,
                           signup_form=signup_form)
# def logout
# def register
