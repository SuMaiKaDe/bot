from telethon import events, Button
import requests
from asyncio import exceptions
from .. import jdbot, chat_id, logger, _ScriptsDir, _ConfigDir, logger, mybot, chname
from .utils import press_event, backfile, _DiyDir, jdcmd, V4, cmd, cronup


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/dl'))
async def my_urlfile(event):
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
        if '下载代理' in mybot.keys() and str(mybot['下载代理']).lower() != 'false' and 'github' in url:
            url = f'{str(mybot["下载代理"])}/{url}'
        filename = url.split('/')[-1]
        resp = requests.get(url).text
        v4btn = [[Button.inline('放入config', data=_ConfigDir), Button.inline('放入scripts', data=_ScriptsDir), Button.inline('放入OWN文件夹', data=_DiyDir)], [
            Button.inline('放入scripts并运行', data='node1'), Button.inline('放入OWN并运行', data='node'), Button.inline('取消', data='cancel')]]
        btn = [[Button.inline('放入config', data=_ConfigDir), Button.inline('放入scripts', data=_ScriptsDir)], [
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
                        backfile(f'{_DiyDir}/{filename}')
                        with open(f'{_DiyDir}/{filename}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        cmdtext = f'{jdcmd} {_DiyDir}/{filename} now'
                        if res2 == 'yes':
                            await cronup(jdbot, conv, resp, filename,
                                         msg, SENDER, markup, _DiyDir)
                        else:
                            await jdbot.edit_message(msg, '脚本已保存到DIY文件夹，并成功运行')
                        conv.cancel()
                    elif res == 'node1':
                        backfile(f'{_ScriptsDir}/{filename}')
                        with open(f'{_ScriptsDir}/{filename}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        cmdtext = f'{jdcmd} {_ScriptsDir}/{filename} now'
                        if res2 == 'yes':
                            await cronup(jdbot, conv, resp, filename,
                                         msg, SENDER, markup, _ScriptsDir)
                        else:
                            await jdbot.edit_message(msg, '脚本已保存到SCRIPTS文件夹，并成功运行')
                        conv.cancel()
                    else:
                        backfile(f'{res}/{filename}')
                        with open(f'{res}/{filename}', 'w+', encoding='utf-8') as f:
                            f.write(resp)
                        if res2 == 'yes':
                            await cronup(jdbot, conv, resp, filename,
                                         msg, SENDER, markup, res)
                        else:
                            await jdbot.edit_message(msg, f'{filename}已保存到{res}文件夹')
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')

if chname:
    jdbot.add_event_handler(my_urlfile, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['dl']))
