import importlib

from flask.ext.script import Manager, prompt_bool
from lso import create_app
import lso.database


app = create_app(__name__, 'development.config')
manager = Manager(app)


def _get_bp_setup(name):
    return importlib.import_module('lso.%s.setup' % name)


@manager.command
def db_create():
    """Creates all tables."""
    lso.database.db.create_all()


@manager.option('-n', '--name', help='Blueprint name')
def db_seed(name):
    """Seeds some blueprint with initial data."""
    _get_bp_setup(name).run(app)
    print 'Done.'


@manager.option('-n', '--name', help='Blueprint name')
def db_drop(name):
    """Drops all tables for some blueprint."""
    if prompt_bool('This will delete all data for `{}`. Proceed?'.format(name)):
        _get_bp_setup(name).drop(app)
        print 'Done.'


@manager.command
def db_drop_all_dangerous():
    """Drops the entire database."""
    if prompt_bool('This will drop the entire database. Proceed?'):
        lso.database.db.drop_all()


if __name__ == '__main__':
    manager.run()
