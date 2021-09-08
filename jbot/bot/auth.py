from telethon import events
from .. import jdbot, chat_id, logger, mybot, chname, _ConfigDir
import requests
import os
import json
import time

_Auth = None
if 'QL_DIR' in os.environ.keys():
    _Auth = f'{_ConfigDir}/auth.json'
    if not os.path.exists(_Auth):
        _Auth = None


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/auth'))
async def my_chart(event):
    if _Auth is None:
        await jdbot.send_message(chat_id, '此命令仅支持青龙面板')
        return None
    msg_text = event.raw_text.split(' ')
    try:
        res = None
        msg = await jdbot.send_message(chat_id, '正在登录，请稍后')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            code_login = msg_text[-1]
            if len(code_login) == 6:
                res = qlLogin(code_login)
            else:
                res = '两步验证的验证码有误'
        else:
            res = qlLogin()
        await jdbot.edit_message(msg, res)
    except Exception as e:
        await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')


def qlLogin(code: str = None):

    try:
        with open(_Auth, 'r', encoding='utf-8') as f:
            auth = json.load(f)
        token = auth['token']
        if token and len(token) > 10:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            res = requests.get('http://127.0.0.1:5600/api/crons', params={
                               'searchValue': '', 't': int(round(time.time() * 1000))}, headers=headers).text
            if res.find('code":200') > -1:
                return '当前登录状态未失效\n无需重新登录'
        if code:
            url = 'http://127.0.0.1:5600/api/user/two-factor/login'
            data = {'username': auth['username'],
                    'password': auth['password'], 'code': code}
            res = requests.put(url, json=data).json()
        else:
            url = 'http://127.0.0.1:5600/api/login'
            data = {'username': auth['username'], 'password': auth['password']}
            res = requests.post(url, json=data).json()
        if res['code'] == 200:
            return '自动登录成功，请重新执行命令'
        if res['message'].find('两步验证') > -1:
            return ' 当前登录已过期，且已开启两步登录验证，请使用命令/auth 六位验证码 完成登录'
        return res['message']
    except Exception as e:
        return '自动登录出错：' + str(e)


if chname:
    jdbot.add_event_handler(my_chart, events.NewMessage(
        chats=chat_id, pattern=mybot['命令别名']['auth']))
