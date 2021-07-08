from telethon import events, Button
import json
import os
from asyncio import exceptions
from .. import jdbot, chat_id, logger, _LogDir, chname, mybot
from ..bot.utils import QL, press_event, split_list, cronmanger, _Auth


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/cron'))
async def my_cron(event):
    '''接收/cron后执行程序'''
    logger.info(f'即将执行{event.raw_text}命令')
    msg_text = event.raw_text.split(' ')
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, '正在查询请稍后')
        if QL:
            with open(_Auth, 'r', encoding='utf-8') as f:
                auth = json.load(f)
            buttons = [{'name': '运行', 'data': 'run'}, {'name': '日志', 'data': 'log'}, {'name': '编辑', 'data': 'edit'}, {
                'name': '启用', 'data': 'enable'}, {'name': '禁用', 'data': 'disable'}, {'name': '删除', 'data': 'del'}, {'name': '取消', 'data': 'cancel'}, {'name': '上级', 'data': 'up'}]
        else:
            auth = {'token': ''}
            buttons = [{'name': '运行', 'data': 'run'}, {'name': '编辑', 'data': 'edit'}, {
                'name': '启用', 'data': 'enable'}, {'name': '禁用', 'data': 'disable'}, {'name': '删除', 'data': 'del'}, {'name': '取消', 'data': 'cancel'}, {'name': '上级', 'data': 'up'}]
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
        logger.info(f'命令参数值为：{text}')
        if not text:
            await jdbot.edit_message(msg, '请正确使用cron命令,后边需跟关键字。/cron abcd')
            return
        go_up = True
        async with jdbot.conversation(SENDER, timeout=30) as conv:
            while go_up:
                res = cronmanger('search', text, auth['token'])
                logger.info(f'任务查询结果：{res}')
                if res['code'] == 200:
                    await jdbot.delete_messages(chat_id, msg)
                    if QL:
                        markup = [Button.inline(
                            i['name'], data=str(res['data'].index(i))) for i in res['data']]
                    else:
                        markup = [Button.inline(i, data=res['data'][i])
                                    for i in res['data']]
                    markup = split_list(markup, int(mybot['每页列数']))
                    markup.append([Button.inline('取消', data='cancel')])
                    msg = await jdbot.send_message(
                        chat_id, '查询结果如下，点击按钮查看详细信息', buttons=markup)
                    convdata = await conv.wait_event(press_event(SENDER))
                    resp = bytes.decode(convdata.data)
                    if resp == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        conv.cancel()
                        go_up = False
                        return
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
                        go_up = False
                        return
                    elif btnres == 'up':
                        continue
                    elif btnres == 'edit':
                        go_up = False
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
                        go_up = False
                        if QL:
                            crondata = res['data'][int(resp)]
                        else:
                            crondata = resp
                        cronres = cronmanger(
                            btnres, crondata, auth['token'])
                    if cronres['code'] == 200:
                        if 'data' not in cronres.keys():
                            cronres['data'] = 'success'
                        await jdbot.delete_messages(chat_id, msg)
                        if len(cronres['data']) <= 4000:
                            msg = await jdbot.send_message(chat_id, f"指令发送成功，结果如下：\n{cronres['data']}")
                        elif len(cronres['data']) > 4000:
                            _log = f'{_LogDir}/bot/qlcron.log'
                            with open(_log, 'w+', encoding='utf-8') as f:
                                f.write(cronres['data'])
                            msg = await jdbot.send_message(chat_id, '日志结果较长，请查看文件', file=_log)
                            os.remove(_log)
                    else:
                        await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{cronres["data"]}')
                else:
                    go_up = False
                    await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(res["data"])}')
        logger.info(f'执行{event.raw_text}命令完毕')
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
        logger.error(f'选择已超时，对话已停止')
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')

if chname:
    jdbot.add_event_handler(my_cron, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['cron']))


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/addcron'))
async def my_addcron(event):
    try:
        SENDER = event.sender_id
        msg = await jdbot.send_message(chat_id, f'请稍后，正在查询')
        if QL:
            with open(_Auth, 'r', encoding='utf-8') as f:
                auth = json.load(f)
            info = '任务名称-->任务命令-->定时\n```测试2-->ql repo xxxxxx.git "jd"-->0 6 * * *```'
        else:
            info = '```0 0 * * * jtask /jd/own/abcd.js```'
            auth = {'token': ''}
        markup = [Button.inline('是', data='yes'),
                  Button.inline('否', data='cancel')]
        async with jdbot.conversation(SENDER, timeout=30) as conv:
            await jdbot.delete_messages(chat_id, msg)
            msg = await conv.send_message('是否确认添加cron', buttons=markup)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
            else:
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message(f'点击复制下方信息进行修改,并发送给我\n{info}')
                resp = await conv.get_response()
                if QL:
                    crondata = {}
                    crondata['name'], crondata['command'], crondata['schedule'] = resp.raw_text.split(
                        '-->')
                    res = cronmanger('add', crondata, auth['token'])
                else:
                    crondata = resp.raw_text
                    res = cronmanger('add', crondata, auth['token'])
                if res['code'] == 200:
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await jdbot.send_message(chat_id, '已成功添加定时任务')
                else:
                    await jdbot.delete_messages(chat_id, msg)
                    msg = await jdbot.send_message(chat_id, f'添加定时任务时发生了一些错误\n{res["data"]}')
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
if chname:
    jdbot.add_event_handler(my_addcron, events.NewMessage(
        from_users=chat_id, pattern=mybot['命令别名']['addcron']))
