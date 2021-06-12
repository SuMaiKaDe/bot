#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 0.3 版本开始不再区分ql、V3、V4。运行日志：log/bot/run.log
# author：   https://github.com/SuMaiKaDe

import json
from . import jdbot, chat_id, logger, _JdbotDir, _LogDir, _botset, _set
from .utils import load_diy
import os
from .bot.update import version, botlog
_botuplog = f'{_LogDir}/bot/up.log'
botpath = f'{_JdbotDir}/bot/'
diypath = f'{_JdbotDir}/diy/'
logger.info('loading bot module...')
load_diy('bot', botpath)
logger.info('loading diy module...')
load_diy('diy', diypath)


async def hello():
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
                    if '版本' not in i:
                        botset[i] = myset[i]
                    else:
                        continue
                with open(_botset, 'w+', encoding='utf-8') as f:
                    json.dump(botset, f)
        else:
            with open(_botset, 'w+', encoding='utf-8') as f:
                json.dump(botset, f)
    except Exception as e:
        logger.info(str(e))

if __name__ == "__main__":
    with jdbot:
        jdbot.loop.create_task(hello())
        jdbot.loop.create_task(mysetting())
        jdbot.loop.run_forever()
