from telethon import events
from .. import jdbot, chat_id,chname


version = 'version :0.9.9.5'
botlog = '''
**2021年6月15日下午**
本次更新内容如下:
    - 新增 支持`MTProxy`类型代理，使用方法见bot.json注释
    - 修复 下载链接不能保存定时任务的BUG
    - 首先需通过 /set 开启别名 改为True
    - 新增 /setname 设置命令别名
    - 可通过中文进行触发命令，可能有bug，自定义名称不能重复！！

**本次更新内容涉及了所有模块，如果产生了新BUG请及时反馈**
'''
@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'版本|^/ver'))
async def my_ver():
    await jdbot.send_message(chat_id,f'当前版本\n：{version}\n{botlog}')