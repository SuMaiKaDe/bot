from telethon import events
from .. import jdbot, chat_id, mybot, chname
from .utils import cmd, jdcmd


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='/node'))
async def my_node(event):
    '''接收/node命令后执行程序'''
    msg_text = event.raw_text.split(' ')
    if isinstance(msg_text,list) and len(msg_text) == 2:
        text = ''.join(msg_text[1:])
    else:
        text = None
    if not text:
        res = '''请正确使用/node命令，如
        /node /abc/123.js 运行abc/123.js脚本
        /node /own/abc.js 运行own/abc.js脚本
        '''
        await jdbot.send_message(chat_id, res)
    else:
        await cmd('{} {}'.format(jdcmd, text))

if chname:
    jdbot.add_event_handler(my_node, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['node']))
