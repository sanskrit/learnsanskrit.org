from flask.ext.security import forms
from wtforms import BooleanField, Form, PasswordField, SubmitField, validators
from flask.ext.wtf.html5 import EmailField


class SignupForm(Form, forms.UniqueEmailFormMixin, forms.RegisterFormMixin,
                 forms.NewPasswordFormMixin):
    email = EmailField('Email address', [validators.Email(),
                                         validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    subscribe = BooleanField('Send me updates from learnsanskrit.org')


class LoginForm(forms.LoginForm):
    email = EmailField('Email address', [validators.Email(),
                                         validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Sign in')
