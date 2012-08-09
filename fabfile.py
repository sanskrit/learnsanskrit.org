import os
from fabric.api import *

APP_FOLDER = 'lso'

def blueprint(name):
    """Create a blueprint with some common files and folders."""
    local('./scripts/create_blueprint.sh %s %s' % (APP_FOLDER, name))

def server():
    local('python runserver.py')
