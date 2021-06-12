from telethon import events, Button
from .utils import split_list, press_event, cmd
from asyncio import exceptions
from .. import jdbot, chat_id, _shortcut, logger


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/a$'))
async def shortcut(event):
    markup = []
    SENDER = event.sender_id
    msg = await jdbot.send_message(chat_id, '正在查询您的常用命令，请稍后')
    with open(_shortcut, 'r', encoding='utf-8') as f:
        shortcuts = f.readlines()
    try:
        cmdtext = None
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            markup = [Button.inline(shortcut.split(
                '-->')[0], data=str(shortcut.split('-->')[-1])) for shortcut in shortcuts if '-->' in shortcut]
            markup = split_list(markup, 3)
            markup.append([Button.inline('取消', data='cancel')])
            msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=markup)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
            else:
                await jdbot.delete_messages(chat_id, msg)
                cmdtext = res
                conv.cancel()
        if cmdtext:
            await cmd(cmdtext.replace('nohup ',''))
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/b$'))
async def shortcut(event):
    markup = []
    msg = await jdbot.send_message(chat_id, '正在查询您的常用命令，请稍后')
    with open(_shortcut, 'r', encoding='utf-8') as f:
        shortcuts = f.readlines()
    try:
        await jdbot.delete_messages(chat_id,msg)
        markup = [Button.text(shortcut,single_use=True) for shortcut in shortcuts if '-->' not in shortcut]
        markup = split_list(markup, 3)
        await jdbot.send_message(chat_id, '请做出您的选择：', buttons=markup)
    except Exception as e:
        await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
