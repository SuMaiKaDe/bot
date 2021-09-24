from telethon import events
from .. import jdbot, chat_id,JD_DIR

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/aff$'))
async def bot_aff(event):
    await jdbot.send_message(chat_id,'感谢您',file=f'{JD_DIR}/jbot/font/aff.jpg')
