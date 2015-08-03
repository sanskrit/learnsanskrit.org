from flask.ext.security import utils

from lso import app, datastore
from ..database import session
from .models import *


def add_admin():
    session = lso.database.db.session
    role = Role(name='admin', description='Administrator privileges')
    session.add(role)
    session.flush()
    with app.app_context():
        pw = utils.encrypt_password('test')
        datastore.create_user(email='admin@learnsanskrit.org', password=pw,
                              roles=[role])
    session.commit()


def run(app=None):
    app = app or lso.create_app(__name__)
    with app.app_context():
        add_admin()


def drop():
    import sqlalchemy
    order = [UserRoleAssoc, User, Role]
    for o in order:
        try:
            o.__table__.drop()
        except sqlalchemy.exc.ProgrammingError:
            print '(table %s does not exist.)' % o.__tablename__
