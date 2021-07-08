import requests
import os
from telethon import events, Button
import re
import time
import json
from .. import jdbot, chat_id, _LogDir, logger, _JdDir, _OwnDir, _ConfigDir, mybot
import asyncio
import datetime
row = int(mybot['每页列数'])
_CronFile = f'{_ConfigDir}/crontab.list'
bean_log = f'{_LogDir}/jd_bean_change/'
_ConfigFile = f'{_ConfigDir}/config.sh'
V4, QL = False, False
if 'JD_DIR' in os.environ.keys():
    V4 = True
    _Auth = None
    if os.path.exists(f'{_ConfigDir}/cookie.sh'):
        _ConfigFile = f'{_ConfigDir}/cookie.sh'
    _DiyDir = _OwnDir
    jdcmd = 'jtask'
elif 'QL_DIR' in os.environ.keys():
    QL = True
    _Auth = f'{_ConfigDir}/auth.json'
    _ConfigFile = _Auth
    _DiyDir = None
    jdcmd = 'task'
    dirs = os.listdir(_LogDir)
    for mydir in dirs:
        if 'jd_bean_change' in mydir:
            bean_log = f'{_LogDir}/{mydir}'
            break
else:
    _DiyDir = None
    jdcmd = 'node'


def myck(ckfile):
    ckreg = re.compile(r'pt_key=\S*?;pt_pin=\S*?;')
    cookiefile = r'/ql/db/cookie.db'
    if QL and not os.path.exists(cookiefile):
        with open(ckfile, 'r', encoding='utf-8') as f:
            auth = json.load(f)
        lines = str(qlenv('search', 'JD_COOKIE', auth['token']))
    elif QL:
        with open(f'{_ConfigDir}/cookie.sh', 'r', encoding='utf-8') as f:
            lines = f.read()
    else:
        with open(ckfile, 'r', encoding='utf-8') as f:
            lines = f.read()
    cookies = ckreg.findall(lines)
    for ck in cookies:
        if ck == 'pt_key=xxxxxxxxxx;pt_pin=xxxx;':
            cookies.remove(ck)
            break
    return cookies


def split_list(datas, n, row: bool = True):
    """一维列表转二维列表，根据N不同，生成不同级别的列表"""
    length = len(datas)
    size = length / n + 1 if length % n else length/n
    _datas = []
    if not row:
        size, n = n, size
    for i in range(int(size)):
        start = int(i * n)
        end = int((i + 1) * n)
        _datas.append(datas[start:end])
    return _datas


def backfile(file):
    '''如果文件存在，则备份，并更新'''
    if os.path.exists(file):
        try:
            os.rename(file, f'{file}.bak')
        except WindowsError:
            os.remove(f'{file}.bak')
            os.rename(file, f'{file}.bak')


def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)


async def cmd(cmdtext):
    '''定义执行cmd命令'''
    try:
        msg = await jdbot.send_message(chat_id, '开始执行命令')
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8')
        if len(res) == 0:
            await jdbot.edit_message(msg, '已执行，但返回值为空')
        elif len(res) <= 4000:
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, res)
        elif len(res) > 4000:
            _log = f'{_LogDir}/bot/{cmdtext.split("/")[-1].split(".js")[0]}-{datetime.datetime.now().strftime("%H-%M-%S")}.log'
            with open(_log, 'w+', encoding='utf-8') as f:
                f.write(res)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '执行结果较长，请查看日志', file=_log)
            os.remove(_log)
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')


def getname(path, dir):
    '''获取文件中文名称，如无则返回文件名'''
    names = []
    reg = r'new Env\(\'[\S]+?\'\)'
    cname = False
    for file in dir:
        try:
            if os.path.isdir(f'{path}/{file}'):
                names.append(file)
            elif file.endswith('.js') and file != 'jdCookie.js' and file != 'getJDCookie.js' and file != 'JD_extra_cookie.js' and 'ShareCode' not in file:
                with open(f'{path}/{file}', 'r', encoding='utf-8') as f:
                    resdatas = f.readlines()
                for data in resdatas:
                    if 'new Env' in data:
                        data = data.replace('\"', '\'')
                        res = re.findall(reg, data)
                        if len(res) != 0:
                            res = res[0].split('\'')[-2]
                            names.append(f'{res}--->{file}')
                            cname = True
                        break
                if not cname:
                    names.append(f'{file}--->{file}')
                    cname = False
            else:
                continue
        except:
            continue
    return names


async def logbtn(conv, SENDER, path, msg, page, filelist):
    '''定义log日志按钮'''
    mybtn = [Button.inline('上一页', data='up'), Button.inline(
        '下一页', data='next'), Button.inline('上级', data='updir'), Button.inline('取消', data='cancel')]
    try:
        if filelist:
            markup = filelist
            newmarkup = markup[page]
            if mybtn not in newmarkup:
                newmarkup.append(mybtn)
        else:
            dir = os.listdir(path)
            dir.sort()
            if path == _LogDir:
                markup = [Button.inline("_".join(file.split("_")[-2:]), data=str(file))
                          for file in dir]
            elif os.path.dirname(os.path.realpath(path)) == _LogDir:
                markup = [Button.inline("-".join(file.split("-")[-5:]), data=str(file))
                          for file in dir]
            else:
                markup = [Button.inline(file, data=str(file))
                          for file in dir]
            markup = split_list(markup, row)
            if len(markup) > 30:
                markup = split_list(markup, 30)
                newmarkup = markup[page]
                newmarkup.append(mybtn)
            else:
                newmarkup = markup
                if path == _JdDir:
                    newmarkup.append([Button.inline('取消', data='cancel')])
                else:
                    newmarkup.append(
                        [Button.inline('上级', data='updir'), Button.inline('取消', data='cancel')])
        msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=newmarkup)
        convdata = await conv.wait_event(press_event(SENDER))
        res = bytes.decode(convdata.data)
        if res == 'cancel':
            msg = await jdbot.edit_message(msg, '对话已取消')
            conv.cancel()
            return None, None, None, None
        elif res == 'next':
            page = page + 1
            if page > len(markup) - 1:
                page = 0
            return path, msg, page, markup
        elif res == 'up':
            page = page - 1
            if page < 0:
                page = len(markup) - 1
            return path, msg, page, markup
        elif res == 'updir':
            path = '/'.join(path.split('/')[:-1])
            if path == '':
                path = _JdDir
            return path, msg, page, None
        elif os.path.isfile(f'{path}/{res}'):
            msg = await jdbot.edit_message(msg, '文件发送中，请注意查收')
            await conv.send_file(f'{path}/{res}')
            msg = await jdbot.edit_message(msg, f'{res}发送成功，请查收')
            conv.cancel()
            return None, None, None, None
        else:
            return f'{path}/{res}', msg, page, None
    except asyncio.exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，本次对话已停止')
        return None, None, None, None
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
        return None, None, None, None


async def nodebtn(conv, SENDER, path, msg, page, filelist):
    '''定义scripts脚本按钮'''
    mybtn = [Button.inline('上一页', data='up'), Button.inline(
        '下一页', data='next'), Button.inline('上级', data='updir'), Button.inline('取消', data='cancel')]
    try:
        if filelist:
            markup = filelist
            newmarkup = markup[page]
            if mybtn not in newmarkup:
                newmarkup.append(mybtn)
        else:
            if path == _JdDir and V4:
                dir = ['scripts', _OwnDir.split('/')[-1]]
            elif path == _JdDir and QL:
                dir = ['scripts']
            else:
                dir = os.listdir(path)
                if mybot['中文'].lower() == "true":
                    dir = getname(path, dir)
            dir.sort()
            markup = [Button.inline(file.split('--->')[0], data=str(file.split('--->')[-1]))
                      for file in dir if os.path.isdir(f'{path}/{file}') or file.endswith('.js')]
            markup = split_list(markup, row)
            if len(markup) > 30:
                markup = split_list(markup, 30)
                newmarkup = markup[page]
                newmarkup.append(mybtn)
            else:
                newmarkup = markup
                if path == _JdDir:
                    newmarkup.append([Button.inline('取消', data='cancel')])
                else:
                    newmarkup.append(
                        [Button.inline('上级', data='updir'), Button.inline('取消', data='cancel')])
        msg = await jdbot.edit_message(msg, '请做出您的选择：', buttons=newmarkup)
        convdata = await conv.wait_event(press_event(SENDER))
        res = bytes.decode(convdata.data)
        if res == 'cancel':
            msg = await jdbot.edit_message(msg, '对话已取消')
            conv.cancel()
            return None, None, None, None
        elif res == 'next':
            page = page + 1
            if page > len(markup) - 1:
                page = 0
            return path, msg, page, markup
        elif res == 'up':
            page = page - 1
            if page < 0:
                page = len(markup) - 1
            return path, msg, page, markup
        elif res == 'updir':
            path = '/'.join(path.split('/')[:-1])
            if path == '':
                path = _JdDir
            return path, msg, page, None
        elif os.path.isfile(f'{path}/{res}'):
            conv.cancel()
            logger.info(f'{path}/{res} 脚本即将在后台运行')
            msg = await jdbot.edit_message(msg, f'{res} 在后台运行成功')
            cmdtext = f'{jdcmd} {path}/{res} now'
            return None, None, None, f'CMD-->{cmdtext}'
        else:
            return f'{path}/{res}', msg, page, None
    except asyncio.exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
        return None, None, None, None
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
        return None, None, None, None


def mycron(lines):
    cronreg = re.compile(r'([0-9\-\*/,]{1,} ){4,5}([0-9\-\*/,]){1,}')
    return cronreg.search(lines).group()


def upcron(cron):
    owninfo = '# mtask任务区域'
    with open(_CronFile, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if owninfo in line:
            i = lines.index(line)
            lines.insert(i+1, cron+'\n')
            break
    with open(_CronFile, 'w', encoding='utf-8') as f:
        f.write(''.join(lines))


async def cronup(jdbot, conv, resp, filename, msg, SENDER, markup, path):
    try:
        if QL:
            #{name: "测试2", command: "ql bot", schedule: "0 0 * * *"}
            crondata = {
                "name": f'{filename.split(".")[0]}', "command": f'task {path}/{filename}', "schedule": f'{mycron(resp)}'}
        else:
            crondata = f'{mycron(resp)} mtask {path}/{filename}'
        msg = await jdbot.edit_message(msg, f'已识别定时\n```{crondata}```\n是否需要修改', buttons=markup)
    except:
        if QL:
            crondata = {
                "name": f'{filename.split(".")[0]}', "command": f'task {path}/{filename}', "schedule": f'0 0 * * *'}
        else:
            crondata = f'0 0 * * * mtask {path}/{filename}'
        msg = await jdbot.edit_message(msg, f'未识别到定时，默认定时\n```{crondata}```\n是否需要修改', buttons=markup)
    convdata3 = await conv.wait_event(press_event(SENDER))
    res3 = bytes.decode(convdata3.data)
    if res3 == 'yes':
        convmsg = await conv.send_message(f'```{crondata}```\n请输入您要修改内容，可以直接点击上方定时进行复制修改\n如果需要取消，请输入`cancel`或`取消`')
        crondata = await conv.get_response()
        crondata = crondata.raw_text
        if crondata == 'cancel' or crondata == '取消':
            conv.cancel()
            await jdbot.send_message(chat_id, '对话已取消')
            return
        await jdbot.delete_messages(chat_id, convmsg)
    await jdbot.delete_messages(chat_id, msg)
    if QL:
        with open(_Auth, 'r', encoding='utf-8') as f:
            auth = json.load(f)
        res = qlcron('add', json.loads(
            str(crondata).replace('\'', '\"')), auth['token'])
        if res['code'] == 200:
            await jdbot.send_message(chat_id, f'{filename}已保存到{path}，并已尝试添加定时任务')
        else:
            await jdbot.send_message(chat_id, f'{filename}已保存到{path},定时任务添加失败，{res["data"]}')
    else:
        upcron(crondata)
        await jdbot.send_message(chat_id, f'{filename}已保存到{path}，并已尝试添加定时任务')


def qlcron(fun, crondata, token):
    url = 'http://127.0.0.1:5600/api/crons'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        if fun == 'search':
            # crondata 格式：str
            params = {
                't': int(round(time.time() * 1000)),
                'searchValue': crondata
            }
            res = requests.get(url, params=params, headers=headers).json()
        elif fun == 'add':
            # crondata 格式：{name: "测试2", command: "ql bot", schedule: "0 0 * * *"}
            data = {
                'name': crondata['name'],
                'command': crondata['command'],
                'schedule': crondata['schedule']
            }
            res = requests.post(url, data=data, headers=headers).json()
        elif fun == 'run':
            data = [crondata['_id']]
            # crondata 格式：命令id
            res = requests.put(f'{url}/run', json=data, headers=headers).json()
        elif fun == 'log':
            # crondata 格式：命令id
            data = crondata['_id']
            res = requests.get(f'{url}/{data}/log', headers=headers).json()
        elif fun == 'edit':
            data = {
                'name': crondata['name'],
                'command': crondata['command'],
                'schedule': crondata['schedule'],
                '_id': crondata['_id']
            }
            # crondata 格式：{name: "测试2", command: "ql bot", schedule: "0 0 * * *", _id: "8HHqjXZM0Va92G63"}
            res = requests.put(url, json=data, headers=headers).json()
        elif fun == 'disable':
            # crondata 格式：命令id
            data = [crondata['_id']]
            res = requests.put(url+'/disable', json=data,
                               headers=headers).json()
        elif fun == 'enable':
            # crondata 格式：命令id
            data = [crondata['_id']]
            res = requests.put(url+'/enable', json=data,
                               headers=headers).json()
        elif fun == 'del':
            # crondata 格式：命令id
            data = [crondata['_id']]
            res = requests.delete(url, json=data, headers=headers).json()
        else:
            res = {'code': 400, 'data': '未知功能'}
    except Exception as e:
        res = {'code': 400, 'data': str(e)}
    finally:
        return res


def V4cron(fun, crondata):
    file = f'{_ConfigDir}/crontab.list'
    with open(file, 'r', encoding='utf-8') as f:
        v4crons = f.readlines()
    try:
        if fun == 'search':
            res = {'code': 200, 'data': {}}
            for cron in v4crons:
                if str(crondata) in cron:
                    res['data'][cron.split(
                        'task ')[-1].split(' ')[0].split('/')[-1].replace('\n', '')] = cron
        elif fun == 'add':
            v4crons.append(crondata)
            res = {'code': 200, 'data': 'success'}
        elif fun == 'run':
            cmd(f'jtask {crondata.split("task")[-1]}')
            res = {'code': 200, 'data': 'success'}
        elif fun == 'edit':
            ocron, ncron = crondata.split('-->')
            i = v4crons.index(ocron)
            v4crons.pop(i)
            v4crons.insert(i, ncron)
            res = {'code': 200, 'data': 'success'}
        elif fun == 'disable':
            i = v4crons.index(crondata)
            crondatal = list(crondata)
            crondatal.insert(0, '#')
            ncron = ''.join(crondatal)
            v4crons.pop(i)
            v4crons.insert(i, ncron)
            res = {'code': 200, 'data': 'success'}
        elif fun == 'enable':
            i = v4crons.index(crondata)
            ncron = crondata.replace('#', '')
            v4crons.pop(i)
            v4crons.insert(i, ncron)
            res = {'code': 200, 'data': 'success'}
        elif fun == 'del':
            i = v4crons.index(crondata)
            v4crons.pop(i)
            res = {'code': 200, 'data': 'success'}
        else:
            res = {'code': 400, 'data': '未知功能'}
        with open(file, 'w', encoding='utf-8') as f:
            f.write(''.join(v4crons))
    except Exception as e:
        res = {'code': 400, 'data': str(e)}
    finally:
        return res


def cronmanger(fun, crondata, token):
    if QL:
        res = qlcron(fun, crondata, token)
    else:
        res = V4cron(fun, crondata)
    return res


def qlenv(fun, envdata, token):
    url = 'http://127.0.0.1:5600/api/envs'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        if fun == 'search':
            params = {
                't': int(round(time.time() * 1000)),
                'searchValue': envdata
            }
            res = requests.get(url, params=params, headers=headers).json()
        elif fun == 'add':
            data = {
                'name': envdata['name'],
                'value': envdata['value'],
                'remarks': envdata['remarks'] if 'remarks' in envdata.keys() else ''
            }
            res = requests.post(url, data=data, headers=headers).json()
        elif fun == 'edit':
            data = {
                'name': envdata['name'],
                'value': envdata['value'],
                '_id': envdata['_id'],
                'remarks': envdata['remarks'] if 'remarks' in envdata.keys() else ''
            }
            res = requests.put(url, json=data, headers=headers).json()
        elif fun == 'disable':
            data = [envdata['_id']]
            res = requests.put(url+'/disable', json=data,
                               headers=headers).json()
        elif fun == 'enable':
            data = [envdata['_id']]
            res = requests.put(url+'/enable', json=data,
                               headers=headers).json()
        elif fun == 'del':
            data = [envdata['_id']]
            res = requests.delete(url, json=data, headers=headers).json()
        else:
            res = {'code': 400, 'data': '未知功能'}
    except Exception as e:
        res = {'code': 400, 'data': str(e)}
    finally:
        return res
