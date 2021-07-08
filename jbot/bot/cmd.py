from telethon import events
from .. import jdbot, StartCMD, chat_id, logger, mybot, chname
from .utils import cmd


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='/cmd'))
async def my_cmd(event):
    '''接收/cmd命令后执行程序'''
    logger.info(f'即将执行{event.raw_text}命令')
    msg_text = event.raw_text.split(' ')
    try:
        if isinstance(msg_text,list):
            text = ' '.join(msg_text[1:])
        else:
            text = None
        if StartCMD and text:
            await cmd(text)
            logger.info(text)
        elif StartCMD:
            msg = '''请正确使用/cmd命令，如
            /cmd jlog    # 删除旧日志
            /cmd jup     # 更新所有脚本
            /cmd jcode   # 导出所有互助码
            /cmd jcsv    # 记录豆豆变化情况
            不建议直接使用cmd命令执行脚本，请使用/node或/snode
            '''
            await jdbot.send_message(chat_id, msg)
        else:
            await jdbot.send_message(chat_id, '未开启CMD命令，如需使用请修改配置文件')
        logger.info(f'执行{event.raw_text}命令完毕')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'发生了某些错误\n{str(e)}')


if chname:
    jdbot.add_event_handler(my_cmd, events.NewMessage(
        chats=chat_id, pattern=mybot['命令别名']['cmd']))
