from fabric.api import *

import lso
from . import FIRM_YES

@task
def create(*tables):
    """Create tables in the database.

    :param tables: the tables to create. If blank, create all tables.
    """
    lso.database.create(*tables)

@task
def drop(*tables):
    """Drop tables from the database.

    :param tables: the tables to create. If blank, drop all tables.
    """
    if confirm_drop(*tables):
        lso.database.drop(*tables)

@task
def recreate(*tables):
    """Drop tables from the database then recreate them.

    :param tables: the tables to recreate. If blank, recreate all tables.
    """
    drop(*tables)
    create(*tables)

@task
def seed(*blueprints):
    """Seed tables is the database, by way of their blueprints.

    :param blueprints: the blueprints containing the tables to seed.
    """
    lso.database.seed(*blueprints)

def confirm_drop(*tables):
    """Ask the user to confirm a table drop"""
    if tables:
        print 'This will drop the following tables from the database:'
        for t in tables:
            print '    {0}'.format(t)
    else:
        print 'This will drop all tables from the database.'
    return prompt("Proceed? [YES/no]") == FIRM_YES
