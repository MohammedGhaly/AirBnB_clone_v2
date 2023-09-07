#!/usr/bin/python3
"""
a script that distributes an archive to web servers using (do_deploy)
"""

from fabric.api import run, put, env
import os

env.hosts = ['100.25.36.194', '54.89.117.225']


def do_deploy(archive_path):
    """
    uploads an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return(False)
    try:
        if put(archive_path, '/tmp/').failed is True:
            return False
        file = archive_path.split('/')[-1]
        archive_name = file.split('.')[0]

        if run('mkdir -p /data/web_static/releases/{}'.format
                (archive_name)).failed is True:
            return False
        if run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
           (file, archive_name)).failed is True:
            return False
        if run('rm /tmp/{}'.format(file)).failed is True:
            return False
        if run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format
           (archive_name, archive_name)).failed is True:
            return False
        if run('rm -rf /data/web_static/releases/{}/web_static'
           .format(archive_name)).failed is True:
            return False
        if run('rm -rf /data/web_static/current').failed is True:
            return False
        if run('ln -s /data/web_static/releases/{} /data/web_static/current'
           .format(archive_name)).failed is True:
            return False
        return(True)
    except Exception as e:
        return(False)
