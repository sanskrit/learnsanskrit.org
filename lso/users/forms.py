from flask.ext.security import forms as F
from wtforms import BooleanField, Form, PasswordField, SubmitField, validators
from flask.ext.wtf.html5 import EmailField


class SignupForm(Form, F.UniqueEmailFormMixin, F.RegisterFormMixin, F.NewPasswordFormMixin):
    email = EmailField('Email address', [validators.Email(),
                                         validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    subscribe = BooleanField('Send me updates from learnsanskrit.org')


class LoginForm(F.LoginForm):
    email = EmailField('Email address', [validators.Email(),
                                         validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Sign in')
