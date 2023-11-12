#DOCKER_HOST='unix:///run/user/1000/docker.sock'
#APP_VERSION='0.1'
#APP_NAME='pyzza'
#CONFIG_PATH_DEFAULT='config.ini'

import configparser, re
from models.app import CONNECTION_TYPES_MODEL
from platformdirs import *
from os import path
from utils import gen_id
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from models.data import Connection, engine, initdb
from common import getconfigpath, checkpaths
import os

class ConfigManager:
    engine: Engine = None

    configpath = None
    defaultconfig = None
    defaulttype = 'unix'
    defaultpath = '/run/user/1000/docker.sock'
    instance = None

    @staticmethod
    def init():
        checkpaths()
        configpath = getconfigpath()
        ConfigManager.configpath = configpath
        if path.isfile(configpath):
            print('config file exists at', configpath)
            ConfigManager.defaultconfig = ConfigManager.load(path=configpath)
            assert ConfigManager.defaultconfig is not None
        else:
            print('config file not found:', configpath, ', writing new file')
            ConfigManager.defaultconfig = ConfigManager.withdefault(path=configpath)
        ConfigManager.engine = engine

    @staticmethod
    def load(path=None):
        config = Config(configpath=path)
        cfg = config.config
        cfg.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
        try:
            cfg.read(path)
            config.parse()
            return config
        except Exception as e:
            print('error loading config file:', e)
            return None
    
    @staticmethod
    def withdefault(path=None):
        defaultpath = getconfigpath()
        config = Config(configpath=path or defaultpath)
        cfg = config.config
        cfg['DEFAULT'] = {
            'name': 'default',
            'type': 'unix',
            'path': '/run/user/1000/docker.sock',
        }
        config.save()
        with Session(engine) as s:
            default = Connection(name=cfg['DEFAULT']['name'], type=cfg['DEFAULT']['type'], path=cfg['DEFAULT']['path'])
            default.ctype = 1
            default.isdefault = True
            s.add(default)
            s.commit()
            config.connections['DEFAULT'] = default
        return config

class Config:
    config = configparser.ConfigParser()
    connections = dict()
    default_connection = None

    def __init__(self, configpath=None):
        self.path = configpath
        dirname = path.dirname(self.path)
        if not path.isdir(dirname):
            os.mkdir(dirname)

    def save(self):
        cfg = self.config
        for (key, value) in self.connections.items():
            old = value.old
            if old is not None:
                cfg.remove_section(old)
            if key == 'DEFAULT':
                tp = CONNECTION_TYPES_MODEL[value.ctype] or -1
                cfg['DEFAULT']['type'] = tp
                continue
            tp = CONNECTION_TYPES_MODEL[value.ctype] or -1
            cfg[value.name] = {
                'type': tp,
                'path': value.connpath or '',
            }
        with open(self.path, 'w') as configfile:
            cfg.write(configfile)

    def get_host(self, name=None):
        s = self.config[name or 'DEFAULT']
        return f'{s["type"]}://{s["path"]}'

    def check(self):
        pass

    def parse(self):
        conns = self.connections
        default = None
        with Session(engine, expire_on_commit=False) as session:
            cc = session.query(Connection).all()
            for conn in cc:
                print('[conn]:', conn.name, conn.isdefault)
                conn.old = conn.name
                conn.ctype = Config.get_index(typestr=conn.conntype)
                if conn.isdefault:
                    default = conn
                    conns['DEFAULT'] = conn
                    self.default_connection = conn
                else:
                    conns[conn.id] = conn
            if len(cc) == 0:
                cfg = self.config
                sect = cfg.sections()
                default = cfg['DEFAULT']
                assert default is not None
                tp = default['type']
                if tp.isnumeric():
                    tp = int(tp)
                else:
                    tp = Config.get_index(typestr=tp)
                id = gen_id()
                defconn = Connection(id=id, name=default['name'] or 'default', type=tp, path=default['path'] or '')
                defconn.ctype = tp
                tp = CONNECTION_TYPES_MODEL[tp]
                defconn.conntype = tp
                session.add(defconn)
                for sec in sect:
                    tp = cfg[sec]['type']
                    if tp.isnumeric():
                        tp = int(tp)
                    else:
                        tp = Config.get_index(typestr=tp)
                    id = gen_id()
                    conn = Connection(id=id, name=sec, type=tp, path=cfg[sec]['path'])
                    conn.ctype = tp
                    tp = CONNECTION_TYPES_MODEL[tp]
                    conn.conntype = tp
                    cc = session.query(Connection).filter(Connection.name==sec).first()
                    if not cc:
                        session.add(conn)
                    conns[id] = conn
                session.commit()
                defconn.setasdefault()
                conns['DEFAULT'] = defconn
                self.default_connection = defconn
        self.connections = conns

    def to_config(self):
        cfg = self.config
        conns = self.connections
        default = conns['DEFAULT']
        tp = default['dat']['type']
        tp = CONNECTION_TYPES_MODEL[tp][0]
        default['dat']['type'] = tp


    def get_index(typestr):
        try:
            return CONNECTION_TYPES_MODEL.index(typestr)
        except:
            return -1
