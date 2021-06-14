
#  [交流频道](https://t.me/tiangongtong)
-------
#  安装教程
##  一、青龙
1. 最新版本青龙直接执行`ql bot`命令即可完成下载安装
2. 设置随容器启动。在config.sh内的`AutostartBot=""`改成`AutostartBot="true"`
##  二、V4
1. 下载项目config内的bot.sh，放在容器config文件夹内，执行`bash /jd/config/bot.sh`
2. 注释掉定时任务内的jup或更改为jup scripts，否则会被自动更新覆盖
3. 执行`cd /jd/jbot && pm2 start ecosystem.config.js
`或`nohup python3 -m jbot >/dev/null 2>&1 &`来启动机器人
## 三、其他
1. 安装python3
2. 如需扫码获取cookie，需增加C环境及图片支持，如`zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev`
3. 执行`pip3 install telethon python-socks[asyncio] pillow qrcode requests prettytable`
4. 或者下载requirements.txt `pip3 install -r requirements.txt`
5. 下载jbot文件夹/jd目录下，下载config/bot.json放在config下
6. ` nohup python3 -m jbot >/dev/null 2>&1 &`
-------
#  配置教程
- 安装好后需要对config目录下的**bot.json**文件进行配置
- bot.json内容严格按照注释要求进行填写，大部分不能启动的原因都是json文件没写对，或格式有错误，或内容未按要求填写。建议填写完后找一个JSON检验网站，验证一下格式
-------
#  排错教程
配置完成，启动完毕，机器人会向你发送最新的更新日志，如果未收到机器人消息，则可能出现了错误，可按如下方式处理
1. 查看log/bot目录下的run.log，看是否有错误，如果该文件内有错误，一般是网络代理问题
2. 如果上述文件不存在，容器内执行`python3 -m jbot`查看是否报错，如错误最后出现json.xxxxx.error则为bot.json未配置好。
3. 如出现其他错误请百度或谷歌或加入
[频道](https://t.me/tiangongtong)交流
-------
#  使用教程
- `/start` 命令可查看当前机器人所支持的所有命令
- `/help` 命令可直接发送给[botfather](https://t.me/BotFather)，用来设置快捷命令
    - `/help` 加其他命令可查看具体使用方法
- `/set` 用来设置一些机器人设置
- `/setshort` 用来设置快捷键，也可通过修改config/shortcut.list进行修改
    - 快捷设置好后，可通过`/a`命令进行触发
    - `/b`命令可以触达shortcut.list内的
-  `/getfile`命令用来获取容器内文件。可通过`/getfile`后边加参数直接获取文件，或选择该目录文件，例如:
    - `/getfile /jd/config`则进入config目录选择文件
    - `/getfile /jd/config/bot.json`则直接获取config目录下的bot.json文件
- `/edit`选择文件进行编辑，命令用法同`/getfile`，也支持`/edit /jd/config/config.sh`这样直接编辑文件
- `/getcookie`用于扫码获取ck 
- `/snode`命令选择脚本进行执行
- `/cmd`相当于在容器内执行终端命令
## 本项目仅作为学习交流使用，严禁任何人与任何组织用于收费项目中
