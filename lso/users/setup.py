from flask.ext.security import utils

from lso import app, datastore
from ..database import session
from .models import *


def run():
    role = Role(name='admin', description='Administrator privileges')
    session.add(role)
    session.flush()
    with app.app_context():
        pw = utils.encrypt_password('test')
        datastore.create_user(email='admin@learnsanskrit.org', password=pw,
                              roles=[role])
    session.commit()
