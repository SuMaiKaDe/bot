
## 使用方法：
- 使用方法
    - ~~将bot.py、bot.json、rebot.sh放入/jd/config文件夹下(旧版本使用方法)~~
    - 在docker内执行`apk add python3`
    - 如需扫码获取cookie及获取图片 需执行`apk add zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev`
    - 由于需要安装多个依赖包，建议将清华源设置为默认源`pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
    - 如果清华源下载慢，可以改成 `pip3 config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/`
    - 执行`pip3 install telethon python-socks[asyncio] pillow qrcode requests prettytable`
    - 或者下载requirements.txt `pip3 install -r requirements.txt`
    - 下载jbot文件夹 放在、/jd或/ql目录下，下载config/bot.json放在config下，在jd或ql目录下运行 `nohup python3 -m jbot >/dev/null 2>&1 &`
    - 如果需要更换机器人token，需要将bot.session删除后，重新运行 
***
## 主要实现功能：
- 主要功能
    - help 获取命令，可直接发送至botfather。
    - start 开始使用本程序。
    - a 使用你的自定义快捷按钮。
    - bean 获取京豆变化，默认为总京豆收支。/bean in 京豆进账，/bean out 京豆支出。
    - chart 获取京豆变化数据柱状图和曲线图。例，/chart 1，获取账号1的京豆变化。
    - cmd 执行cmd命令,例如/cmd python3 /python/bot.py 则将执行python目录下的bot.py 不建议使用机器人使用并发，可能产生不明原因的崩溃。 
    - edit 从jd目录下选择文件编辑，需要将编辑好信息全部发给机器人，机器人会根据你发的信息进行替换。建议用来编辑config或crontab.list 其他文件慎用！！！
    - getcookie 扫码获取cookie 增加30s内取消按钮，30s后不能进行其他交互直到2分钟或获取到cookie。
    - getfile 获取jd目录下文件。
    - log 选择查看执行日志。
    - node 执行js脚本文件，直接输入/node jd_bean_change 如执行其他自己js，需输入绝对路径。即可进行执行。该命令会等待脚本执行完，期间不能使用机器人，建议使用snode命令。
    - setshort 设置自定义按钮，每次设置会覆盖原设置。
    - snode 命令可以选择脚本执行，只能选择/scripts 和/own目录下的脚本，选择完后直接后台运行，不影响机器人响应其他命令。 
    - set 设置
    - dl 下载
    此外直接发送文件，会让您选择保存到哪个文件夹，如果选择运行，将保存至own目录下，并立即运行脚本'''

## [交流频道](https://t.me/tiangongtong)

## 青龙与V4均可使用

# 严禁任何人以任何形式放置在收费项目中
