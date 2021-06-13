from telethon import events
from .. import jdbot, chat_id, _ConfigDir
from .utils import cmd

@jdbot.on(events.NewMessage(from_users=chat_id, pattern='^/up$'))
async def mycodes():
    try:
        msg = await jdbot.send_message(chat_id,'开始更新程序，请稍候')
        await cmd(f'bash {_ConfigDir}/bot.sh')
        await jdbot.delete_messages(chat_id,msg)
    except Exception as e:
        await jdbot.send_message(chat_id,str(e))
