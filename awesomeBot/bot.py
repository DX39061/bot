import nonebot
from config import global_config
from os import path

if __name__ == '__main__':
    nonebot.init(global_config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins', 'WeeklyReport'), 'plugins.WeeklyReport')
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins', 'Welcome'), 'plugins.Welcome')
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins', 'Teach'), 'plugins.Teach')
    nonebot.run()
