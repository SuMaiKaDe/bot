#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import json
from . import jdbot, chat_id, logger, _JdbotDir, _LogDir, _botset, _set, mybot
from .utils import load_diy
import os
import random
from .bot.update import version, botlog
_botuplog = f'{_LogDir}/bot/up.log'
botpath = f'{_JdbotDir}/bot/'
diypath = f'{_JdbotDir}/diy/'
logger.info('loading bot module...')
load_diy('bot', botpath)
logger.info('loading diy module...')
load_diy('diy', diypath)


async def new():
    info = '[项目地址](https://github.com/SuMaiKaDe/) \t| \t[交流频道](https://t.me/tiangongtong) '
    if os.path.exists(_botuplog):
        isnew = False
        with open(_botuplog, 'r', encoding='utf-8') as f:
            logs = f.readlines()
        for log in logs:
            if version in log:
                isnew = True
                return
        if not isnew:
            with open(_botuplog, 'a', encoding='utf-8') as f:
                f.writelines([version, botlog])
            await jdbot.send_message(chat_id, f'[机器人上新了](https://github.com/SuMaiKaDe/jddockerbot/tree/master)\n{botlog}\n运行日志为log/bot/run.log\n\n\t{info}', link_preview=False)
    else:
        with open(_botuplog, 'w+', encoding='utf-8') as f:
            f.writelines([version, botlog])
        await jdbot.send_message(chat_id, f'[机器人上新了](https://github.com/SuMaiKaDe/jddockerbot/tree/master)\n{botlog}\n运行日志为log/bot/run.log\n\n\t{info}', link_preview=False)


async def mysetting():
    try:
        with open(_set, 'r', encoding='utf-8') as f:
            botset = json.load(f)
        if os.path.exists(_botset):
            with open(_botset, 'r', encoding='utf-8') as f:
                myset = json.load(f)
            if myset['版本'] != botset['版本']:
                for i in myset:
                    if '版本' not in i and not isinstance(myset[i],dict):
                        botset[i] = myset[i]
                    elif isinstance(myset[i],dict):
                        for j in myset[i]:
                            botset[i][j] = myset[i][j]
                    else:
                        continue
                with open(_botset, 'w+', encoding='utf-8') as f:
                    json.dump(botset, f)
        else:
            with open(_botset, 'w+', encoding='utf-8') as f:
                json.dump(botset, f)
    except Exception as e:
        logger.info(str(e))


async def hello():
    if '启动问候' in mybot.keys() and mybot['启动问候'].lower() == 'true':
        info = '[项目地址](https://github.com/SuMaiKaDe/) \t| \t[交流频道](https://t.me/tiangongtong) '
        words = mybot["启动问候语"].split("|")
        word = words[random.randint(0, len(words) - 1)]
        await jdbot.send_message(chat_id, f'{str(word)}\n\n\t{info}', link_preview=False)


if __name__ == "__main__":
    with jdbot:
        jdbot.loop.create_task(new())
        jdbot.loop.create_task(mysetting())
        jdbot.loop.create_task(hello())
        jdbot.loop.run_forever()
