from telethon import events
from .. import jdbot, chat_id, _LogDir, logger, mybot, chname
from ..bot.quickchart import QuickChart
from .beandata import get_bean_data
_botimg = f'{_LogDir}/bot/bean.jpeg'


@jdbot.on(events.NewMessage(chats=chat_id, pattern=r'^/chart'))
async def my_chart(event):
    logger.info(f'即将执行{event.raw_text}命令')
    msg_text = event.raw_text.split(' ')
    try:
        msg = await jdbot.send_message(chat_id, '正在查询，请稍后')
        if isinstance(msg_text,list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
        logger.info(f'命令参数值为：{text}')
        if text and int(text):
            beanin, beanout, beanstotal, date = get_bean_data(int(text))
            if not beanout:
                msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(beanin)}')
            else:
                creat_chart(date, f'账号{str(text)}',
                            beanin, beanout, beanstotal[1:])
                await jdbot.delete_messages(chat_id,msg)
                msg = await jdbot.send_message(chat_id, f'您的账号{text}收支情况', file=_botimg)
        else:
            msg = await jdbot.edit_message(msg, '请正确使用命令\n/chart n n为第n个账号')
    except Exception as e:
        await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
    finally:
        logger.info(f'执行{event.raw_text}命令完毕')


if chname:
    jdbot.add_event_handler(my_chart, events.NewMessage(
        chats=chat_id, pattern=mybot['命令别名']['chart']))


def creat_chart(xdata, title, bardata, bardata2, linedate):
    logger.info(f'即将生成chart图表{title}')
    qc = QuickChart()
    qc.background_color = '#fff'
    qc.width = "1000"
    qc.height = "600"
    qc.config = {
        "type": "bar",
        "data": {
            "labels": xdata,
            "datasets": [
                {
                    "label": "IN",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata
                },
                {
                    "label": "OUT",
                    "backgroundColor": [
                        "rgb(255, 99, 132)",
                        "rgb(255, 159, 64)",
                        "rgb(255, 205, 86)",
                        "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)",
                        "rgb(153, 102, 255)",
                        "rgb(255, 99, 132)"
                    ],
                    "yAxisID": "y1",
                    "data": bardata2
                },
                {
                    "label": "TOTAL",
                    "type": "line",
                    "fill": False,
                    "backgroundColor": "rgb(201, 203, 207)",
                    "yAxisID": "y2",
                    "data": linedate
                }
            ]
        },
        "options": {
            "plugins": {
                "datalabels": {
                    "anchor": 'end',
                    "align": -100,
                    "color": '#666',
                    "font": {
                        "size": 20,
                    }
                },
            },
            "legend": {
                "labels": {
                    "fontSize": 20,
                    "fontStyle": 'bold',
                }
            },
            "title": {
                "display": True,
                "text": f'{title}   收支情况',
                "fontSize": 24,
            },
            "scales": {
                "xAxes": [{
                    "ticks": {
                        "fontSize": 24,
                    }
                }],
                "yAxes": [
                    {
                        "id": "y1",
                        "type": "linear",
                        "display": False,
                        "position": "left",
                        "ticks": {
                            "max": int(int(max([max(bardata), max(bardata2)])+100)*2)
                        },
                        "scaleLabel": {
                            "fontSize": 20,
                            "fontStyle": 'bold',
                        }
                    },
                    {
                        "id": "y2",
                        "type": "linear",
                        "display": False,
                        "ticks": {
                            "min": int(min(linedate)*2-(max(linedate))-100),
                            "max": int(int(max(linedate)))
                        },
                        "position": "right"
                    }
                ]
            }
        }
    }
    qc.to_file(_botimg)
    logger.info(f'生成chart图表{title}完成')
