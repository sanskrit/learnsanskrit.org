"""
learnsanskrit.org fabric file
"""

import lso
import os
from fabric.api import *
try:
    from production.fabfile import *
except ImportError:
    pass

PROJECT_DIR = os.path.dirname(__file__)
APP_DIR = 'lso'

def blueprint(name):
    """Create a blueprint with some common files and folders."""
    path = os.path.join(PROJECT_DIR, 'scripts/create_blueprint.sh')
    local(path + ' %s %s' % (APP_DIR, name))

def db(command):
    """
    Run the command in `command` on the database. Possible values include:
    
    - init: initialize all models connected to the app.
    
    """
    from lso import database
    if command == 'init':
        database.init()
    else:
        raise Exception('Unknown database command "%s"' % command)

def server():
    """Run the site locally."""
    local('python runserver.py')

def test():
    """Run unit tests."""
    local('python lso_tests.py')
