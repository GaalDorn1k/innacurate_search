import os
import sys
import configparser


class Config(object):
    def __init__(self, config_path: str):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.port = int(config['default']['port'])
        self.embedder = config['default']['embedder']
        self.search_treshold = float(config['default']['search_treshold'])
        self.uno_path = config['default']['uno_path']
        self.temp_folder = config['default']['temp_folder']


def get_config() -> Config:
    return Config('config.ini')


config = get_config()
sys.path.append(config.uno_path)

if not os.path.exists(config.temp_folder):
    os.mkdir(config.temp_folder)
