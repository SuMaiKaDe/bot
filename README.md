
#  [交流频道](https://t.me/tiangongtong)
-------
#  安装教程
##  一、青龙
1. 最新版本青龙直接执行`ql bot`命令即可完成下载安装
2. 设置随容器启动。在config.sh内的`AutostartBot=""`改成`AutostartBot="true"`
##  二、V4
1. 下载本项目config目录内的bot.sh，并上传至容器内`/jd/config`文件夹并执行
> docker exec -it **替换成你的容器名** bash /jd/config/bot.sh
2. 修改/jd/config/crontab.list，修改jup定时设定【2选1】，防止自动更新覆盖BOT设置
- #6 3,8,12,18,22 * * * sleep 37 && jup >> /jd/log/jup.log 2>&1        【关闭JUP】
- 6 3,8,12,18,22 * * * sleep 37 && jup scripts >> /jd/log/jup.log 2>&1 【只更新scripts】
3. 执行命令启动机器人【2选1】
- `cd /jd/jbot && pm2 start ecosystem.config.js`
- `nohup python3 -m jbot >/dev/null 2>&1 &`
##### 更多详细图文教程，请参考：https://blog.zjxnas.top/archives/31/

## 三、其他
1. 安装python3
- apk update 
- apk add python3
- apk add py2-pip
2. 添加环境支持，如`zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev`
- 执行`pip3 install telethon python-socks[asyncio] pillow qrcode requests prettytable`
- 或下载requirements.txt后，执行 `pip3 install -r requirements.txt`
3. 下载jbot文件夹并上传至容器内的/jd目录
4. 下载config/bot.json，并上传至容器内的/jd/config目录
5. 后台挂机，进入容器的ssh，并执行命令
- `nohup python3 -m jbot >/dev/null 2>&1 &`
-------
#  配置教程
1. 首次安装，需要配置/jd/config目录下的**bot.json**文件
2. 配置示例，如图

![OxKRUjYdXzmnk6V](https://i.loli.net/2021/06/14/OxKRUjYdXzmnk6V.png)

### 注意：
- bot.json有严格的格式要求，需按照注释要求进行填写。
- 大部分不能启动的原因都是json文件格式错误，或未按要求填写。
-------
-------
#  排错教程
配置完成，启动完毕，机器人会向你发送最新的更新日志，如果未收到机器人消息，则可能出现了错误，可按如下方式处理
1. 检查是否关注了自己的BOT
2. 检查网络
- 查看log/bot目录下的run.log，看是否有错误，如果该文件内有错误，一般是网络代理问题
3. 如果上述文件不存在，容器内执行`python3 -m jbot`查看是否报错，如错误最后出现json.xxxxx.error则为bot.json未配置好。
4. 如出现其他错误请谷歌或加入
[频道](https://t.me/tiangongtong)交流
-------
#  使用教程
- `/start` 可查看当前机器人所支持的所有命令
- `/help` 可直接发送给[botfather](https://t.me/BotFather)，用来设置快捷命令，其他命令可查看具体使用方法
- `/set` 用来设置一些机器人设置
- `/setshort` 用来设置快捷键，也可通过修改config/shortcut.list进行修改
- `/a`或`/b` 可以触发shortcut.list内的自定义命令
- `/getfile` 获取容器内文件。可通过`/getfile`直接获取文件或选择文件，例: `/getfile /jd/config`进入config目录选择文件；`/getfile /jd/config/bot.json`直接获取bot.json文件
- `/edit` 选择文件进行编辑，命令用法同`/getfile`，也支持`/edit /jd/config/config.sh`来直接编辑文件
- `/getcookie`  扫码获取ck 
- `/snode` 选择脚本进行执行
- `/cmd` 在容器内执行终端命令
- `/chart n`用于查看第n个账户的近7日收支曲线柱状图。 n为数字，代表你得第几个账户
- `/bean n`用法同`/chart`以表格形式展示
- `/node` 使用node执行js脚本，例如：`/node /jd/scripts/jd_fruit.js`
## 本项目仅作为学习交流使用，严禁任何人与任何组织用于收费项目中
