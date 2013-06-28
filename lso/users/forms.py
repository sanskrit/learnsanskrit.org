from flask.ext.security import forms as F
from flask.ext.wtf import BooleanField, Email, Form, PasswordField, Required, SubmitField
from flask.ext.wtf.html5 import EmailField


class SignupForm(Form, F.UniqueEmailFormMixin, F.RegisterFormMixin, F.NewPasswordFormMixin):
    email = EmailField('Email address', [Email(), Required()])
    password = PasswordField('Password', [Required()])
    subscribe = BooleanField('Send me updates from learnsanskrit.org')


class LoginForm(F.LoginForm):
    email = EmailField('Email address', [Email(), Required()])
    password = PasswordField('Password', [Required()])
    submit = SubmitField('Sign in')