import os

# Flask settings
# --------------
DATABASE_URI = 'postgresql:///learnsanskrit'
DEBUG = True
SECRET_KEY = 'development'

# flask-mail
# ----------
DEFAULT_MAIL_SENDER = 'form@learnsanskrit.org'
DEFAULT_MAIL_RECIPIENT = 'info@learnsanskrit.org'

# flask-security
# --------------
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '$2a$10$WyxRXkzAICMHgmqhMGTlJu'
SECURITY_LOGIN_URL = '/slogin'
SECURITY_REGISTER_USER_TEMPLATE = 'users/register.html'

SECURITY_CHANGEABLE = True  # can change password
SECURITY_REGISTERABLE = True  # can register
SECURITY_RECOVERABLE = True  # can recover a lost password

# flask-sqlalchemy
# ----------------
SQLALCHEMY_DATABASE_URI = DATABASE_URI

# File uploads
# ------------
UPLOAD_DIR = '/tmp'
ALLOWED_EXTENSIONS = {'xml'}

# Large data
# ----------
_root_path = os.path.expanduser('~/projects/sanskrit-data')
DATA_PATH = os.path.join(_root_path, 'all-data')
MONIER_DIR = os.path.join(_root_path, 'monier-williams')
STATIC_DEST = 'lso/static'
