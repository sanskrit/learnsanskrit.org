from fabric.api import *
from fabric.contrib.project import rsync_project
import production

env.hosts = [production.host]


def deploy_static():
    # without trailing slash, files are moved to `remote_dir`/static.
    rsync_project(local_dir='lso/static/',
                  remote_dir=production.static_remote_dir, delete=True)
