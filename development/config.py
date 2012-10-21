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

# Large data
SANSKRIT_PATH = os.path.expanduser('~/sanskrit/data')
MONIER_DIR = os.path.join(SANSKRIT_PATH, 'mw')
