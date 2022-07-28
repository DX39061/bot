from nonebot import on_notice, NoticeSession
from config.global_config import config_welcome
import time

group_id = config_welcome['group_id']
self_id = config_welcome['self_id']
freezing_time = config_welcome['freezing_time']
greeting = config_welcome['greeting']
last_welcome = 0


@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.event.group_id not in group_id:
        return
    global last_welcome
    if time.time() - last_welcome > freezing_time:
        last_welcome = time.time()
        await session.send(greeting)

