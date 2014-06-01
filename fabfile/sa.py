from fabric.api import *
from sanskrit import Context


@task
def create(*tables):
    """Create tables in the database.

    :param tables: the tables to create. If blank, create all tables.
    """
    import lso
    ctx = Context(lso.app.config)
    ctx.create_all()


@task
def drop(*tables):
    """Drop tables from the database.

    :param tables: the tables to create. If blank, drop all tables.
    """
    import lso
    ctx = Context(lso.app.config)
    ctx.drop_all()


@task
def recreate(*tables):
    """Drop tables from the database then recreate them.

    :param tables: the tables to recreate. If blank, recreate all tables.
    """
    import lso
    ctx = Context(lso.app.config)
    ctx.drop_all()
    ctx.build()


@task
def seed(*blueprints):
    """Seed Sanskrit tables.

    :param blueprints: the blueprints containing the tables to seed.
    """
    import lso
    ctx = Context(lso.app.config)
    ctx.build()
