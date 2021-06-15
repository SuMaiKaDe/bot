from telethon import events
from .. import jdbot, chat_id, _LogDir, _JdDir, mybot, chname
from .utils import logbtn
import os


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/log'))
async def my_log(event):
    '''定义日志文件操作'''
    SENDER = event.sender_id
    path = _LogDir
    page = 0
    filelist = None
    async with jdbot.conversation(SENDER, timeout=60) as conv:
        msg = await conv.send_message('正在查询，请稍后')
        while path:
            path, msg, page, filelist = await logbtn(conv, SENDER, path, msg, page, filelist)


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/getfile'))
async def my_getfile(event):
    '''定义获取文件命令'''
    SENDER = event.sender_id
    path = _JdDir
    page = 0
    msg_text = event.raw_text.split(' ')
    if len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None
    if text and os.path.isfile(text):
        await jdbot.send_message(chat_id, '请查收文件', file=text)
        return
    elif text and os.path.isdir(text):
        path = text
        filelist = None
    elif text:
        await jdbot.send_message(chat_id, 'please marksure it\'s a dir or a file')
        filelist = None
    else:
        filelist = None
    async with jdbot.conversation(SENDER, timeout=60) as conv:
        msg = await conv.send_message('正在查询，请稍后')
        while path:
            path, msg, page, filelist = await logbtn(conv, SENDER, path, msg, page, filelist)

if chname:
    jdbot.add_event_handler(my_getfile, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['getfile']))
    jdbot.add_event_handler(my_log, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['log']))
