from telethon import events
from .. import jdbot, chat_id, _ConfigDir
from .utils import cmd

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/up$'))
async def mycodes():
    await cmd(f'bash {_ConfigDir}/bot.sh')
