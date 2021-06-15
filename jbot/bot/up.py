from telethon import events
from .. import jdbot, chat_id, _ConfigDir
from .utils import cmd

@jdbot.on(events.NewMessage(from_users=chat_id, pattern='^/up$'))
async def myup(event):
    try:
        msg = await jdbot.send_message(chat_id,'开始更新程序，请稍候，\n提示开始运行后，机器人会被杀死，并重新启动\n因此后边更新信息不会再推送，不代表机器人不理你了')
        await cmd(f'bash {_ConfigDir}/bot.sh')
        await jdbot.delete_messages(chat_id,msg)
    except Exception as e:
        await jdbot.send_message(chat_id,str(e))
