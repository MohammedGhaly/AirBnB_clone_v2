#!/usr/bin/python3
''''
fabfile to pack static folder to an archive
and distribute it to web servers
'''
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["100.25.36.194", "54.89.117.225"]


def do_pack():
    '''
    generates a .tgz archive from the contents of the web_static folder
    '''

    local("mkdir -p versions")
    d = datetime.strftime(datetime.now(), "%Y%m%d%I%M%S")
    name = 'web_static_{}.tgz'.format(d)
    path = 'versions/{}'.format(name)
    result = local("tar -czvf {} web_static".format(path))
    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """uploads an archive to web servers.
    Returns:
        If the file doesn't exist or an error occurs: False
        Otherwise: True
    """

    if os.path.isfile(archive_path) is False:
        return False
    f = archive_path.split("/")[-1]
    archive_name = f.split(".")[0]

    if put(archive_path, "/tmp/{}".format(f)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(archive_name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(archive_name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(f, archive_name)).failed is True:
        return False
    if run("rm /tmp/{}".format(f)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format
           (archive_name, archive_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(archive_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(archive_name)).failed is True:
        return False
    return True


def deploy():
    '''creates and uploads an archive to a web servers'''
    file = do_pack()
    if file is not None:
        return do_deploy(file)
    return False
