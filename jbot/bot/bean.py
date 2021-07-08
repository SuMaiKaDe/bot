from logging import log
from PIL import Image, ImageFont, ImageDraw
from telethon import events
from .. import jdbot, chat_id, _LogDir, _JdbotDir, logger, mybot, chname
from prettytable import PrettyTable
import subprocess
from .beandata import get_bean_data
from .utils import V4

IN = _LogDir + '/bean_income.csv'
OUT = _LogDir + '/bean_outlay.csv'
TOTAL = _LogDir + '/bean_total.csv'
_botimg = _LogDir + '/bean.jpg'
_font = _JdbotDir + '/font/jet.ttf'


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/bean'))
async def my_bean(event):
    logger.info(f'即将执行{event.raw_text}命令')
    msg_text = event.raw_text.split(' ')
    try:
        msg = await jdbot.send_message(chat_id, '正在查询，请稍后')
        if isinstance(msg_text,list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
        logger.info(f'命令参数值为：{text}')
        if V4 and text == 'in':
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(IN)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的近日收入情况', file=_botimg)
        elif V4 and text == 'out':
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(OUT)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的近日支出情况', file=_botimg)
        elif not V4 and (text == 'in' or text == 'out' or text == None):
            await jdbot.edit_message(msg, 'QL暂不支持使用bean in、out \n请使用/bean n n为数字')
        elif text and int(text):
            beanin, beanout, beanstotal, date = get_bean_data(int(text))
            logger.info(f'获取到的数据为：{beanin}-{beanout}-{beanstotal}-{date}')
            if not beanout:
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(beanin)}')
            else:
                creat_bean_count(date, beanin, beanout, beanstotal[1:])
                await jdbot.delete_messages(chat_id, msg)
                await jdbot.send_message(chat_id, f'您的账号{text}收支情况', file=_botimg)
        elif not text:
            subprocess.check_output(
                'jcsv', shell=True, stderr=subprocess.STDOUT)
            creat_bean_counts(TOTAL)
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '您的总京豆情况', file=_botimg)
        else:
            logger.info(f'青龙暂仅支持/bean n n为账号数字')
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '青龙暂仅支持/bean n n为账号数字')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry{str(e)}')

if chname:
    jdbot.add_event_handler(my_bean, events.NewMessage(
        chats=chat_id, pattern=mybot['命令别名']['bean']))


def creat_bean_count(date, beansin, beansout, beanstotal):
    logger.info(f'正在单账户生成图片')
    tb = PrettyTable()
    tb.add_column('DATE', date)
    tb.add_column('BEANIN', beansin)
    tb.add_column('BEANOUT', beansout)
    tb.add_column('TOTAL', beanstotal)
    font = ImageFont.truetype(_font, 18)
    im = Image.new("RGB", (500, 260), (244, 244, 244))
    dr = ImageDraw.Draw(im)
    dr.text((10, 5), str(tb), font=font, fill="#000000")
    im.save(_botimg)
    logger.info(f'图片生成完成')


def creat_bean_counts(csv_file):
    logger.info(f'正在多账户生成图片')
    with open(csv_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    tb = PrettyTable()
    num = len(data[-1].split(',')) - 1
    title = ['DATE']
    for i in range(0, num):
        title.append('COUNT'+str(i+1))
    tb.field_names = title
    data = data[-7:]
    for line in data:
        row = line.split(',')
        if len(row) > len(title):
            row = row[:len(title)]
        elif len(row) < len(title):
            i = len(title) - len(row)
            for _ in range(0, i):
                row.append(0)
        tb.add_row(row)
    length = 172 + 100 * num
    im = Image.new("RGB", (length, 400), (244, 244, 244))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(_font, 18)
    dr.text((10, 5), str(tb), font=font, fill="#000000")
    im.save(_botimg)
    logger.info(f'图片生成完成')
