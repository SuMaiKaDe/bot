from telethon import events
from .. import jdbot, chat_id,chname


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='/start'))
async def my_start(event):
    '''接收/start命令后执行程序'''
    msg = '''使用方法如下：
    /help 获取命令，可直接发送至botfather。
    /start 开始使用本程序。
    /a 使用你的自定义快捷按钮。
    /addcron 增加cron，例：0 0 * * * jtask xxxxx。
    /bean 获取变化，默认为总京豆收支。/bean in 进账，/bean out 支出。
    /chart 获取变化数据柱状图和曲线图。例：/chart 1，获取账号1变化。
    /clearboard 删除快捷输入按钮。
    /cmd 执行命令，例：/cmd python3 /python/bot.py，则执行python目录下的bot.py。不建议使用BOT使用并发，可能产生不明原因的崩溃。 
    /cron 进行cron管理。
    /dl 下载文件，例：/dl https://raw.githubusercontent.com/SuMaiKaDe/bot/main/requirements.txt
    /edit 从目录选择文件并编辑，需要将编辑好信息全部发给BOT，BOT会根据你发的信息进行替换。建议仅编辑config或crontab.list，其他文件慎用！！！
    /env 环境变量管理，仅支持青龙面板。
    /getfile 获取/jd目录下文件。
    /log 查看脚本执行日志。
    /node 执行js脚本，输入/node xxxxx.js。如执行非scripts目录js，需输入绝对路径执行。node命令会等待脚本执行完，期间不能使用BOT，建议使用snode命令。
    /set 设置。
    /setname 设置命令别名。
    /setshort 设置自定义按钮，每次设置会覆盖原设置。
    /snode 选择脚本执行，只能选择/scripts和/own目录下的脚本，选择完后直接后台运行，不影响BOT响应其他命令。 
    
    此外，直接发送文件至BOT，会让您选择保存到目标文件夹，支持保存并运行。'''
    await jdbot.send_message(chat_id, msg)

if chname:
    jdbot.add_event_handler(my_start,events.NewMessage(from_users=chat_id, pattern='开始'))
