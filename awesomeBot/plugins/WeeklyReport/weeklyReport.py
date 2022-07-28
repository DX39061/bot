from nonebot import on_command, CommandSession
import requests
from config.global_config import config_weeklyReport

group_id = config_weeklyReport['group_id']
self_id = config_weeklyReport['self_id']
url = config_weeklyReport['url']


@on_command('status', only_to_me=False)
async def status(session: CommandSession):
    if session.event.group_id not in group_id:
        return
    submitted_users, unsubmitted_users = await get_user_list()
    message = f"{len(submitted_users)}人已提交周报"
    await session.send(message)


@on_command('remind', only_to_me=False)
async def remind(session: CommandSession):
    if session.event.group_id not in group_id:
        return
    submitted_users, unsubmitted_users = await get_user_list()
    if not len(unsubmitted_users):
        message = f"终于有一次全员交齐了"
    else:
        message = f"仍然有{len(unsubmitted_users)}名铁憨憨没有交周报\n他们分别是:\n"
        for user in unsubmitted_users:
            message += f"{user}  "
        message += "\n清退警告⚠️"
    await session.send(message)


async def get_user_list():
    resp = requests.get(url=url)
    data_dict = resp.json()

    submitted_users = data_dict["submitted"]
    unsubmitted_users = data_dict["unsubmitted"]

    return submitted_users, unsubmitted_users
