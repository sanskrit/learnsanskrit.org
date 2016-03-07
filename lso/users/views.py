from flask import render_template
from flask.ext.security import login_required, current_user

import forms
from lso import security
from lso.util import LSOBlueprint


bp = LSOBlueprint('users', __name__, url_prefix='')


@login_required
@bp.route('/home/')
def home():
    return render_template('users/home.html')


@login_required
@bp.route('/settings/')
def settings():
    return render_template('users/settings.html')


@bp.route('/login/')
def login():
    login_form = forms.LoginForm()
    signup_form = forms.SignupForm()
    return render_template('users/login.html', login_form=login_form,
                           signup_form=signup_form)


# def logout
# def register
