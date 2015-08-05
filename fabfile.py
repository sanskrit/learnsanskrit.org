from fabric.api import *
from fabric.contrib.project import rsync_project, upload_project
import production

env.hosts = [production.host]


def deploy_static():
    # without trailing slash, files are moved to `remote_dir`/static.
    rsync_project(local_dir='lso/static/',
                  remote_dir=production.static_remote_dir, delete=True)


def deploy_data():
    run('mkdir -p {}'.format(production.data_dir))
    run('mkdir -p {}'.format(production.monier_dir))

    # Data will be in `data_dir`/all-data
    # `upload_data` uses gzip, and these files are large.
    upload_project(local_dir='~/projects/sanskrit-data/all-data',
                  remote_dir=production.data_dir)

    # Data will be in `data_dir`/monier-williams
    upload_project(local_dir='~/projects/sanskrit-data/monier-williams',
                  remote_dir=production.monier_dir)
