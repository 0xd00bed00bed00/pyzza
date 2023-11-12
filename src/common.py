from platformdirs import *
from dotenv import load_dotenv
from os import path
import os

load_dotenv()

ENV=os.getenv('ENV') or 'development'
DEBUG=ENV=='development'
CTYPE_DEFAULT=int(os.getenv('CTYPE_DEFAULT') or '1')
CPATH_DEFAULT=os.getenv('CPATH_DEFAULT') or '/run/user/1000/docker.sock'
DOCKER_HOST=os.getenv('DOCKER_HOST') or 'unix:///run/user/1000/docker.sock'
APP_VERSION=os.getenv('APP_VERSION') or '0.1'
APP_NAME=os.getenv('APP_NAME') or 'pyzza'
CONFIG_PATH_DEFAULT=os.getenv('CONFIG_PATH_DEFAULT') or 'config.ini'

def getconfigdir():
    return f'{user_config_dir(APP_NAME)}'

def gettmpdir():
    return f'{getconfigdir()}/tmp'

def getconfigpath():
    return f'{getconfigdir()}/{CONFIG_PATH_DEFAULT}'

def getlogdir():
    return f'{getconfigdir()}/logs'

def checkpaths():
    configdir = getconfigdir()
    if not path.isdir(configdir):
        os.mkdir(configdir)
    dirname = gettmpdir()
    if not path.isdir(dirname):
        os.mkdir(dirname)
    logdir = getlogdir()
    if not path.isdir(logdir):
        os.mkdir(logdir)

class ModelType:
    CONTAINER = 'CONTAINER'
    IMAGE = 'IMAGE'
    VOLUME = 'VOLUME'
    NETWORK = 'NETWORK'

class FileInfo:
    name=None
    owner=None
    group=None
    size=None
    created=None
    permissions=None
    
    def __init__(self, line: str=None, name=None, owner=None, group=None, size=None, created=None, permissions=None):
        self.name=name
        self.owner=owner
        self.group=group
        self.size=size
        self.created=created
        self.permissions=permissions
        if line is not None:
            props=line.split(' ')
            if len(props)==9:
                self.name = props[8]
                self.owner = props[2]
                self.group = props[3]
                self.size = props[4]
                self.created = ' '.join(props[5:7])
                self.permissions = props[8]

    def to_list(self):
        return [
            self.name,
            '',
            self.size,
            self.created,
            self.owner,
            self.group,
            self.permissions,
        ]