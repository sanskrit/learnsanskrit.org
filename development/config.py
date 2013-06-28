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

# File uploads
# ------------
UPLOAD_DIR = '/tmp'
ALLOWED_EXTENSIONS = {'xml'}

# Large data
# ----------
DATA_PATH = os.path.expanduser('~/sanskrit/data')
MONIER_DIR = os.path.join(DATA_PATH, 'mw')
STATIC_DEST = 'lso/static'
