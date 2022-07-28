from nonebot import on_natural_language, NLPSession
from nonebot import on_command, CommandSession
from nonebot.permission import SUPERUSER
import sqlite3
import time
from plugins.Teach.db import *
from config.global_config import config_teach

group_id = config_teach['group_id']
admin_group = config_teach['admin_group']
self_id = config_teach['self_id']
banned_msg = config_teach['banned_msg']
banned_user = config_teach['banned_user']
freezing_time = config_teach['freezing_time']
conn = sqlite3.connect(config_teach['database'])
db_create_table(conn)


@on_command("teach", shell_like=True, only_to_me=False, permission=SUPERUSER)
async def teach_question(session: CommandSession):
    if session.event.group_id not in admin_group:
        return
    argv = session.argv
    if len(argv) != 4:
        msg = "format: /teach <question> <kw-score-kw-score> <answer> <required_score>"
        await session.send(msg)
        return
    db_update(conn, argv[0], argv[1], argv[2], argv[3], 0)
    msg = "谢谢你，我学会了"
    await session.send(msg)


@on_command("delete", shell_like=True, only_to_me=False, permission=SUPERUSER)
async def delete_question(session: CommandSession):
    if session.event.group_id not in admin_group:
        return
    argv = session.argv
    if len(argv) != 1:
        msg = "format: /delete <key>"
        await session.send(msg)
        return
    msg = "我，忘掉了什么？"
    db_delete(conn, argv[0])
    await session.send(msg)


@on_natural_language(keywords=None, only_to_me=False)
async def _(session: NLPSession):
    if session.event.group_id not in group_id and session.event.group_id not in admin_group:
        return
    if session.event.user_id in banned_user:
        return
    # print("In natural language handler")
    text = session.msg_text
    # print("text: ",text)
    question_list = db_get_all(conn)
    # print("question_list: ",question_list)
    max_score = 0
    max_question = question_list[0]
    msg = ""
    for question in question_list:
        score = 0
        q = question[0]
        kws = question[1].split("-")
        ans = question[2]
        required_score = eval(question[3])
        last_time = eval(question[4])
        # print("q: ",q,"ans: ",ans,"kws: ",kws,"required_score: ",required_score,"last_time: ",last_time)
        for i in range(0, len(kws) - 1, 2):
            # print(kws[i])
            if kws[i].lower() in text.lower():
                score += eval(kws[i + 1])
        if score >= required_score and score > max_score and (time.time() - last_time) >= freezing_time:
            # print("last_time: ",last_time, "now: ", time.time())
            max_score = score
            max_question = question
            msg = "Q: " + q + "\nA: " + ans
    if max_score > 0:
        db_update(conn, max_question[0], max_question[1], max_question[2], max_question[3], time.time())
        await session.send(msg)


@on_command("list", shell_like=True, only_to_me=False)
async def list_brief(session: CommandSession):
    if session.event.group_id not in group_id and session.event.group_id not in admin_group:
        return
    question_list = db_get_all(conn)
    msg = ""
    for question in question_list:
        msg += "Q: " + question[0] + "\n" + "A: " + question[2] + "\n\n"
    if msg.strip() == "":
        msg = "我什么都不记得了"
    await session.send(msg.rstrip())


@on_command("list_full", shell_like=True, only_to_me=False, permission=SUPERUSER)
async def list_full(session: CommandSession):
    if session.event.group_id not in admin_group:
        return
    question_list = db_get_all(conn)
    msg = ""
    for question in question_list:
        msg += "Q: " + question[0] + "\n" + "kw: " + question[1] + "\n" + "A: " + question[
            2] + "\n" + "required_score: " + question[3] + "\n" + "last_time: " + question[4] + "\n\n"
    if msg.strip() == "":
        msg = "我什么都不记得了"
    await session.send(msg.rstrip())


@on_command("ban", shell_like=True, only_to_me=False, permission=SUPERUSER)
async def ban(session: CommandSession):
    if session.event.group_id not in admin_group:
        return
    argv = session.argv
    if len(argv) != 1:
        msg = "format: /ban <key>"
    else:
        banned_msg.append(argv[0])
        msg = "ban " + argv[0]
    await session.send(msg)


@on_command("help", shell_like=True, only_to_me=False, permission=SUPERUSER)
async def help_menu(session: CommandSession):
    if session.event.group_id not in admin_group:
        return
    msg = "/help: 列出所有命令\n/teach <key> <value>：教我做事\n/delete <key>：施加遗忘术\n/list：读取我的记忆\n/listFull: 列出详细信息\n/ban " \
          "<key>：ban message "
    await session.send(msg)