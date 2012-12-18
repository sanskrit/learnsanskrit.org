"""
learnsanskrit.org fabric file
"""

import os
from fabric.api import *

FIRM_YES = 'YES'
FABFILE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(FABFILE_DIR)
APP_DIR = 'lso'

import db
import pdf
import sa


@task
def blueprint(name):
    """Create a blueprint with some common files and folders."""
    path = os.path.join(PROJECT_DIR, 'scripts/create_blueprint.sh')
    local(path + ' %s %s' % (APP_DIR, name))


@task
def server():
    """Run the site locally."""
    local('python runserver.py')


@task
def test():
    """Run unit tests."""
    local('python lso_tests.py')

try:
    from production.fabfile import *
except ImportError:
    pass
