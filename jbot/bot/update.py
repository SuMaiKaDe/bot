from telethon import events
from .. import jdbot, chat_id


version = 'version :0.9.9.6'
botlog = '''
**2021年6月21日**
本次更新内容如下:
    - 新增 /ver 用来查看当前版本号
    - 青龙新增 /env 命令，用来管理环境变量
        - 使用方法 /env keywords 将列出所有包含keywords的环境变量
    - 青龙新增 /addenv 命令，用来新增环境变量
        - 使用方法 /addenv 触发，按照格式复制修改发送。
        - 以“-->”进行名称、值、备注区隔

'''


# @jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^版本'))
@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ver'))
async def my_ver(event):
    await jdbot.send_message(chat_id, f'当前版本\n{version}\n{botlog}')
