from .login import user
from telethon import events
import time


@user.on(events.NewMessage(pattern=r'^re[ 0-9]*$', outgoing=True))
async def mycp(event):
    num = event.raw_text.split(' ')
    if isinstance(num, list) and len(num) == 2:
        num = int(num[-1])
    else:
        num = 1
    reply = await event.get_reply_message()
    await event.delete()
    for _ in range(0, num):
        await reply.forward_to(int(event.chat_id))


@user.on(events.NewMessage(pattern=r'^id$', outgoing=True))
async def myid(event):
    reply = await event.get_reply_message()
    if reply:
        userid = reply.sender.id
        chat_id = event.chat_id
        await event.edit(f'当前聊天:`{chat_id}`\n你的user_id:`{userid}`')
    else:
        await event.delete()


@user.on(events.NewMessage(pattern=r'^del[ 0-9]*$', outgoing=True))
async def selfprune(event):
    try:
        num = event.raw_text.split(' ')
        if isinstance(num, list) and len(num) == 2:
            count = int(num[-1])
        else:
            count = 1
        await event.delete()
        count_buffer = 0
        async for message in user.iter_messages(event.chat_id, from_user="me"):
            if count_buffer == count:
                break
            await message.delete()
            count_buffer += 1
        notification = await user.send_message(event.chat_id, f'已删除{count_buffer}/{count}')
        time.sleep(.5)
        await notification.delete()
    except Exception as e:
        await user.send_message(event.chat_id, str(e))
