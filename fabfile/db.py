from fabric.api import *

from . import FIRM_YES


@task
def create(*blueprints):
    """Create blueprint tables in the database.

    :param blueprints: the blueprints to create. If blank, create all
                       blueprints.
    """
    import lso
    lso.database.create(*blueprints)


@task
def drop(*blueprints):
    """Drop the given blueprints.

    :param blueprints: the blueprints to drop. If blank, drop all
                       blueprints.
    """
    if confirm_drop(*blueprints):
        import lso
        lso.database.drop(*blueprints)


@task
def recreate(*blueprints):
    """Drop blueprints from the database then recreate them.

    :param tables: the blueprints to recreate. If blank, recreate all
                   blueprints.
    """
    drop(*blueprints)
    create(*blueprints)


@task
def seed(*blueprints):
    """Seed blueprints in the database.

    :param blueprints: the blueprints to seed.
    """
    import lso
    lso.database.seed(*blueprints)


@task
def rebuild(*blueprints):
    """Drop tables from the given blueprints then recreate and seed them.

    :param blueprints: the blueprints to rebuild.
    """
    recreate(*blueprints)
    seed(*blueprints)


def confirm_drop(*blueprints):
    """Ask the user to confirm a table drop"""
    if blueprints:
        print 'This will drop tables for the following blueprints:'
        for t in blueprints:
            print '    {0}'.format(t)
    else:
        print 'This will drop all tables from the database.'
    return prompt("Proceed? [YES/no]") == FIRM_YES
