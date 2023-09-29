DOCKER_HOST='unix:///run/user/1000/docker.sock'
APP_VERSION='0.1'
APP_NAME='pyzza'
CONFIG_PATH_DEFAULT='config.ini'

import configparser, string, random, uuid, re
from models.data import CONNECTION_TYPES_MODEL

class ConfigManager:
    def __init__(self):
        pass

class Config:
    config = configparser.ConfigParser()
    connections = dict()
    default_connection = None

    def __init__(self, path=None):
        self.path = path

    def load(path=CONFIG_PATH_DEFAULT):
        config = Config()
        cfg = config.config
        cfg.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        try:
            cfg.read(path)
            return config
        except Exception as e:
            print('error loading config file:', e)
            return None
        
    def save(self):
        pass

    def get_host(self, name=None):
        pass

    def check(self):
        pass

    def from_config(self):
        cfg = self.config
        sect = cfg.sections()
        default = cfg['DEFAULT']
        assert default is not None
        conns = self.connections
        tp = default['type']
        if tp.isnumeric():
            tp = int(tp)
        else:
            tp = Config.get_index(typestr=tp)
        id = self.gen_id()
        conns['DEFAULT'] = {
            'dat': {
                'name': default['name'] or 'default',
                'type': tp,
                'path': default['path'] or '',
            },
            'old': default['name'],
            'cfg': default,
            'id': id,
        }
        self.default_connection = conns['DEFAULT']
        for sec in sect:
            tp = cfg[sec]['type']
            if tp.isnumeric():
                tp = int(tp)
            else:
                tp = Config.get_index(typestr=tp)
                id = Config.gen_id()
                self.connections[id] = {
                    'dat': {
                        'name': sec,
                        'type': tp,
                        'path': cfg[sec]['path'],
                    },
                    'old': sec,
                    'id': id,
                }

    def to_config(self):
        cfg = self.config
        sect = cfg.sections()
        conns = self.connections
        default = conns['DEFAULT']
        tp = default['dat']['type']
        tp = CONNECTION_TYPES_MODEL[tp][0]
        default['dat']['type'] = tp


    def gen_id():
        rnd = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        uid = uuid.uuid5(uuid.NAMESPACE_DNS, rnd)
        id = str(uid)
        return id
    
    def get_index(typestr):
        try:
            return CONNECTION_TYPES_MODEL.index(typestr)
        except:
            return -1
