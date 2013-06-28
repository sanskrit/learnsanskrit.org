from flask import Blueprint, g, render_template
from flask.ext.security import login_required, current_user as u

import forms as f
from ..database import session
from lso import app, security
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
