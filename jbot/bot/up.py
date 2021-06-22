from telethon import events
from .. import jdbot, chat_id, _ConfigDir, logger, mybot
from .utils import cmd
from .update import version, botlog
import requests

@jdbot.on(events.NewMessage(from_users=chat_id, pattern='^/up$'))
async def my_up(event):
    try:
        msg = await jdbot.send_message(chat_id, '开始更新程序，请稍候，\n提示开始运行后，机器人会被杀死，并重新启动\n因此后边更新信息不会再推送，不代表机器人不理你了')
        res = requests.get('https://ghproxy.com/https://raw.githubusercontent.com/SuMaiKaDe/bot/main/config/bot.sh').text
        with open(f'{_ConfigDir}/bot.sh','w+',encoding='utf-8') as f:
            f.write(res)
        await cmd(f'bash {_ConfigDir}/bot.sh')
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        await jdbot.send_message(chat_id, str(e))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ver$', incoming=True))
async def my_ver(event):
    await jdbot.send_message(chat_id, f'当前版本\n{version}\n{botlog}')
