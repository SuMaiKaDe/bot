from telethon import events, Button
import requests
from asyncio import exceptions
from .. import jdbot, chat_id, logger, SCRIPTS_DIR, CONFIG_DIR, logger, BOT_SET, ch_name
from .utils import press_event, backup_file, DIY_DIR, TASK_CMD, V4, cmd, add_cron


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/dl'))
async def bot_url_file(event):
    '''接收github链接后执行程序'''
    msg_text = event.raw_text.split(' ')
    try:
        if isinstance(msg_text,list) and len(msg_text) == 2:
            url = msg_text[-1]
        else:
            url = None
        SENDER = event.sender_id
        if not url:
            await jdbot.send_message(chat_id, '请正确使用dl命令，需加入下载链接')
            return
        else:
            msg = await jdbot.send_message(chat_id, '请稍后正在下载文件')
        if '下载代理' in BOT_SET.keys() and str(BOT_SET['下载代理']).lower() != 'false' and 'github' in url:
            url = f'{str(BOT_SET["下载代理"])}/{url}'
        file_name = url.split('/')[-1]
        resp = requests.get(url).text
        v4btn = [[Button.inline('放入config', data=CONFIG_DIR), Button.inline('放入scripts', data=SCRIPTS_DIR), Button.inline('放入OWN文件夹', data=DIY_DIR)], [
            Button.inline('放入scripts并运行', data='node1'), Button.inline('放入OWN并运行', data='node'), Button.inline('取消', data='cancel')]]
        btn = [[Button.inline('放入config', data=CONFIG_DIR), Button.inline('放入scripts', data=SCRIPTS_DIR)], [
            Button.inline('放入scripts并运行', data='node1'), Button.inline('取消', data='cancel')]]
        if resp:
            cmdtext = None
            markup = []
            async with jdbot.conversation(SENDER, timeout=30) as conv:
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message('请选择您要放入的文件夹或操作：\n')
                if V4:
                    markup = v4btn
                else:
                    markup = btn
                msg = await jdbot.edit_message(msg, '请选择您要放入的文件夹或操作：', buttons=markup)
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                markup = [Button.inline('是', data='yes'),
                          Button.inline('否', data='no')]
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                else:
                    msg = await jdbot.edit_message(msg, '是否尝试自动加入定时', buttons=markup)
                    convdata2 = await conv.wait_event(press_event(SENDER))
                    res2 = bytes.decode(convdata2.data)
                    if res == 'node':
                        backup_file(f'{DIY_DIR}/{file_name}')
                        with open(f'{DIY_DIR}/{file_name}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        cmdtext = f'{TASK_CMD} {DIY_DIR}/{file_name} now'
                        if res2 == 'yes':
                            await add_cron(jdbot, conv, resp, file_name,
                                         msg, SENDER, markup, DIY_DIR)
                        else:
                            await jdbot.edit_message(msg, '脚本已保存到DIY文件夹，并成功运行')
                        conv.cancel()
                    elif res == 'node1':
                        backup_file(f'{SCRIPTS_DIR}/{file_name}')
                        with open(f'{SCRIPTS_DIR}/{file_name}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        cmdtext = f'{TASK_CMD} {SCRIPTS_DIR}/{file_name} now'
                        if res2 == 'yes':
                            await add_cron(jdbot, conv, resp, file_name,
                                         msg, SENDER, markup, SCRIPTS_DIR)
                        else:
                            await jdbot.edit_message(msg, '脚本已保存到SCRIPTS文件夹，并成功运行')
                        conv.cancel()
                    else:
                        backup_file(f'{res}/{file_name}')
                        with open(f'{res}/{file_name}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        if res2 == 'yes':
                            await add_cron(jdbot, conv, resp, file_name,
                                         msg, SENDER, markup, res)
                        else:
                            await jdbot.edit_message(msg, f'{file_name}已保存到{res}文件夹')
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')

if ch_name:
    jdbot.add_event_handler(bot_url_file, events.NewMessage(
        from_users=chat_id, pattern=BOT_SET['命令别名']['dl']))
