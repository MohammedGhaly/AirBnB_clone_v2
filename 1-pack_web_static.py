#!/usr/bin/python3
'''
a module containing "do_pack" function that generate .tgz archive
from the contents of webstatic directory
'''
from datetime import datetime
from fabric.api import local


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
