from telethon import events
from .. import jdbot, chat_id
from .utils import V4, cmd


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/reboot$'))
async def bot_reboot(event):
    await jdbot.send_message(chat_id, '即将重启，请稍后')
    if V4:
        await cmd('pm2 restart jbot')
    else:
        await cmd('ql bot')
