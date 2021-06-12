from telethon import events, Button
import json
import os
from asyncio import exceptions
from .. import jdbot, chat_id, logger, _LogDir
from ..bot.utils import QL, press_event, split_list, cronmanger, mybot, _Auth


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/cron'))
async def mycrons(event):
    '''接收/cron后执行程序'''
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, '正在查询请稍后')
        if QL:
            with open(_Auth, 'r', encoding='utf-8') as f:
                auth = json.load(f)
            buttons = [{'name': '运行', 'data': 'run'}, {'name': '日志', 'data': 'log'}, {'name': '编辑', 'data': 'edit'}, {
                'name': '启用', 'data': 'enable'}, {'name': '禁用', 'data': 'disable'}, {'name': '删除', 'data': 'del'}, {'name': '取消', 'data': 'cancel'}]
        else:
            auth = {'token': ''}
            buttons = [{'name': '运行', 'data': 'run'}, {'name': '编辑', 'data': 'edit'}, {
                'name': '启用', 'data': 'enable'}, {'name': '禁用', 'data': 'disable'}, {'name': '删除', 'data': 'del'}, {'name': '取消', 'data': 'cancel'}]
        if len(event.raw_text.split(' ')) > 1:
            text = event.raw_text.replace('/cron ', '')
        else:
            text = ''
        res = cronmanger('search', text, auth['token'])
        if res['code'] == 200:
            async with jdbot.conversation(SENDER, timeout=30) as conv:
                await jdbot.delete_messages(chat_id, msg)
                if QL:
                    markup = [Button.inline(
                        i['name'], data=str(res['data'].index(i))) for i in res['data']]
                else:
                    markup = [Button.inline(i, data=res['data'][i])
                              for i in res['data']]
                markup = split_list(markup, int(mybot['每页列数']))
                msg = await jdbot.send_message(
                    chat_id, '查询结果如下，点击按钮查看详细信息', buttons=markup)
                convdata = await conv.wait_event(press_event(SENDER))
                resp = bytes.decode(convdata.data)
                logger.info(res['data'])
                logger.info(resp)
                if QL:
                    croninfo = '名称：\n\t{name}\n任务：\n\t{command}\n定时：\n\t{schedule}\n是否已禁用：\n\t{isDisabled}\n\t0--表示启用，1--表示禁用'.format(
                        **res['data'][int(resp)])
                    markup = [Button.inline(i['name'], data=i['data'])
                              for i in buttons]
                else:
                    croninfo = f'{resp}'
                    markup = [Button.inline(i['name'], data=i['data'])
                              for i in buttons]
                markup = split_list(markup, int(mybot['每页列数']))
                msg = await jdbot.edit_message(msg, croninfo, buttons=markup)
                convdata = await conv.wait_event(press_event(SENDER))
                btnres = bytes.decode(convdata.data)
                if btnres == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                    return
                elif btnres == 'edit':
                    if QL:
                        info = '```{name}-->{command}-->{schedule}```'.format(
                            **res["data"][int(resp)])
                    else:
                        info = f'```{resp}```'
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await conv.send_message(f'{info}\n请复制信息并进行修改')
                    respones = await conv.get_response()
                    respones = respones.raw_text
                    if QL:
                        res['data'][int(resp)]['name'], res['data'][int(
                            resp)]['command'], res['data'][int(resp)]['schedule'] = respones.split('-->')
                        cronres = cronmanger(
                            'edit', res['data'][int(resp)], auth['token'])
                    else:
                        cronres = cronmanger(
                            'edit', f'{resp}-->{respones}\n', auth['token'])
                else:
                    if QL:
                        crondata = res['data'][int(resp)]
                    else:
                        crondata = resp
                    cronres = cronmanger(
                        btnres, crondata, auth['token'])
                if cronres['code'] == 200:
                    if 'data' not in cronres.keys():
                        cronres['data'] = 'sucess'
                    await jdbot.delete_messages(chat_id, msg)
                    if len(cronres['data']) <= 4000:
                        msg = await jdbot.send_message(chat_id, f"指令发送成功，结果如下：\n{cronres['data']}")
                    elif len(res) > 4000:
                        _log = f'{_LogDir}/bot/qlcron.log'
                        with open(_log, 'w+', encoding='utf-8') as f:
                            f.write(cronres['data'])
                        msg = await jdbot.send_message(chat_id, '日志结果较长，请查看文件', file=_log)
                        os.remove(_log)
                else:
                    await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{cronres["data"]}')
        else:
            await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(res["data"])}')
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
