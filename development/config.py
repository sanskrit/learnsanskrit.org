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

# File uploads
# ------------
UPLOAD_DIR = '/tmp'
ALLOWED_EXTENSIONS = {'xml'}

# Large data
# ----------
DATA_PATH = os.path.expanduser('~/sanskrit/data')
MONIER_DIR = os.path.join(DATA_PATH, 'mw')
STATIC_DEST = 'lso/static'
