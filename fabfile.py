from fabric.api import *
from fabric.contrib.project import rsync_project
import production

env.hosts = [production.host]


def deploy_static():
    """Deploy static assets (CSS, JS, ...)"""
    # without trailing slash, files are moved to `remote_dir`/static.
    rsync_project(local_dir='lso/static/',
                  remote_dir=production.static_remote_dir, delete=True)


def deploy_data():
    """Deploy large data files (MW dictionary, linguistic data)"""
    # Data will be in `data_dir`/all-data
    rsync_project(local_dir='~/projects/sanskrit-data/all-data',
                  remote_dir=production.data_dir)

    # Data will be in `data_dir`/monier-williams
    rsync_project(local_dir='~/projects/sanskrit-data/monier-williams',
                  remote_dir=production.monier_dir)


def deploy_all():
    deploy_static()
    deploy_data()
