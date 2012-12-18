from fabric.api import *
from sanskrit import Context

import lso


@task
def create(*tables):
    """Create tables in the database.

    :param tables: the tables to create. If blank, create all tables.
    """
    ctx = Context(lso.app.config)
    ctx.create_all()


@task
def drop(*tables):
    """Drop tables from the database.

    :param tables: the tables to create. If blank, drop all tables.
    """
    ctx = Context(lso.app.config)
    ctx.drop_all()


@task
def recreate(*tables):
    """Drop tables from the database then recreate them.

    :param tables: the tables to recreate. If blank, recreate all tables.
    """
    ctx = Context(lso.app.config)
    ctx.drop_all()
    ctx.build()


@task
def seed(*blueprints):
    """Seed tables is the database, by way of their blueprints.

    :param blueprints: the blueprints containing the tables to seed.
    """
    ctx = Context(lso.app.config)
    ctx.build()
