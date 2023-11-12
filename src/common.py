from platformdirs import *
from dotenv import load_dotenv
from os import path
import os

load_dotenv()

DOCKER_HOST=os.getenv('DOCKER_HOST') or 'unix:///run/user/1000/docker.sock'
APP_VERSION=os.getenv('APP_VERSION') or '0.1'
APP_NAME=os.getenv('APP_NAME') or 'pyzza'
CONFIG_PATH_DEFAULT=os.getenv('CONFIG_PATH_DEFAULT') or 'config.ini'

def gettmpdir():
    return f'{user_config_dir(APP_NAME)}/tmp'

def getconfigpath():
    return f'{user_config_dir(APP_NAME)}/{CONFIG_PATH_DEFAULT}'

def checkpaths():
    dirname = gettmpdir()
    if not path.isdir(dirname):
        os.mkdir(dirname)

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