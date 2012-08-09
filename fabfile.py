from fabric.api import *

def server():
    local('python runserver.py')
