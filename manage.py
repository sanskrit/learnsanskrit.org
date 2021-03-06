import importlib

import lso.database
from flask.ext.script import Manager, prompt_bool
from lso import create_app
import lso.texts.lib
from sanskrit import Context


app = create_app(__name__, 'config')
manager = Manager(app)


def _get_bp_setup(name):
    """Returns a reference to `lso.{name}.setup`"""
    return importlib.import_module('lso.%s.setup' % name)


@manager.command
def cache_clear():
    """Clears the flask-cache cache."""
    from lso import cache
    cache.clear()


@manager.command
def db_create_all():
    """Creates all tables."""
    lso.database.db.create_all()


@manager.option('-n', '--name', help='Blueprint name', required=True)
def db_seed(name):
    """Seeds some blueprint with initial data."""
    _get_bp_setup(name).run(app)
    print 'Done.'


@manager.option('-n', '--name', help='Blueprint name', required=True)
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

# TODO: better name than -n ?
@manager.option('-n', '--name', help='Path to text', required=True)
def upload_text(name):
    lso.texts.lib.process_text_xml(name)


@manager.command
def sa_create_all(*tables):
    """Creates tables for `sanskrit`."""
    ctx = Context(app.config)
    ctx.create_all()


@manager.command
def sa_seed_all(*blueprints):
    """Seeds tables for `sanskrit`."""
    # TODO: fix this
    if prompt_bool('This will drop then recreate all linguistic data. Proceed?'):
        ctx = Context(app.config)
        ctx.build()


@manager.command
def sa_drop_all():
    """Drops tables for `sanskrit`."""
    if prompt_bool('This will drop all linguistic data. Proceed?'):
        ctx = Context(app.config)
        ctx.drop_all()


if __name__ == '__main__':
    manager.run()
