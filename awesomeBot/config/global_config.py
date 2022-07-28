from nonebot.default_config import *
import yaml

with open('/usr/src/app/awesomeBot/config/config.yaml', 'r') as f:
    cfg = yaml.load(f, yaml.FullLoader)

config_weeklyReport = cfg['weeklyReport']
config_welcome = cfg['welcome']
config_teach = cfg['teach']
config_global = cfg['global']

SUPERUSERS = set(config_global['super_users'])
COMMAND_START = set(config_global['command_start'])
HOST = config_global['host']
PORT = config_global['port']
DEBUG = False



