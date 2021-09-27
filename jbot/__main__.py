#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import json
from . import jdbot, chat_id, logger, LOG_DIR, BOT_SET_JSON_FILE_USER, BOT_SET_JSON_FILE, BOT_SET, BOT_DIR
from .utils import load_module
import os
import random
from .bot.update import version, botlog
BOT_UP_LOG = f'{LOG_DIR}/bot/up.log'
BOT_M_DIR = f'{BOT_DIR}/bot/'
BOT_D_DIR = f'{BOT_DIR}/diy/'
BOT_U_DIR = f'{BOT_DIR}/user/'
logger.info('loading bot module...')
load_module('bot', BOT_M_DIR)
logger.info('loading diy module...')
load_module('diy', BOT_D_DIR)
logger.info('loading user module...')
load_module('user', BOT_U_DIR)

async def new_ver():
    info = '[项目地址](https://github.com/SuMaiKaDe/) \t| \t[交流频道](https://t.me/tiangongtong) '
    if os.path.exists(BOT_UP_LOG):
        is_new = False
        with open(BOT_UP_LOG, 'r', encoding='utf-8') as f:
            logs = f.read()
        if version in logs:
            is_new = True
            return
        if not is_new:
            with open(BOT_UP_LOG, 'a', encoding='utf-8') as f:
                f.writelines([version, botlog])
            await jdbot.send_message(chat_id, f'[机器人上新了](https://github.com/SuMaiKaDe/jddockerbot/tree/master)\n{botlog}\n运行日志为log/bot/run.log\n\n\t{info}', link_preview=False)
    else:
        with open(BOT_UP_LOG, 'w+', encoding='utf-8') as f:
            f.writelines([version, botlog])
        await jdbot.send_message(chat_id, f'[机器人上新了](https://github.com/SuMaiKaDe/jddockerbot/tree/master)\n{botlog}\n运行日志为log/bot/run.log\n\n\t{info}', link_preview=False)


async def bot_set_init():
    try:
        with open(BOT_SET_JSON_FILE, 'r', encoding='utf-8') as f:
            bot_set = json.load(f)
        if os.path.exists(BOT_SET_JSON_FILE_USER):
            with open(BOT_SET_JSON_FILE_USER, 'r', encoding='utf-8') as f:
                user_set = json.load(f)
            if user_set['版本'] != bot_set['版本']:
                for i in user_set:
                    if '版本' not in i and not isinstance(user_set[i], dict):
                        bot_set[i] = user_set[i]
                    elif isinstance(user_set[i], dict):
                        for j in user_set[i]:
                            bot_set[i][j] = user_set[i][j]
                    else:
                        continue
                with open(BOT_SET_JSON_FILE_USER, 'w+', encoding='utf-8') as f:
                    json.dump(bot_set, f)
        else:
            with open(BOT_SET_JSON_FILE_USER, 'w+', encoding='utf-8') as f:
                json.dump(bot_set, f)
    except Exception as e:
        logger.info(str(e))


async def hello():
    if BOT_SET.get('启动问候') and BOT_SET['启动问候'].lower() == 'true':
        info = '[项目地址](https://github.com/SuMaiKaDe/) \t| \t[交流频道](https://t.me/tiangongtong) '
        hello_words = BOT_SET["启动问候语"].split("|")
        hello_word = hello_words[random.randint(0, len(hello_words) - 1)]
        await jdbot.send_message(chat_id, f'{str(hello_word)}\n\n\t{info}', link_preview=False)


if __name__ == "__main__":
    with jdbot:
        jdbot.loop.create_task(new_ver())
        jdbot.loop.create_task(bot_set_init())
        jdbot.loop.create_task(hello())
        jdbot.loop.run_forever()
