import os
from fabric.api import *

PROJECT_FOLDER = os.path.dirname(__file__)
APP_FOLDER = 'lso'

def blueprint(name):
    """Create a blueprint with some common files and folders."""
    path = os.path.join(PROJECT_FOLDER, 'scripts/create_blueprint.sh')
    local(path + ' %s %s' % (APP_FOLDER, name))

def server():
    local('python runserver.py')
