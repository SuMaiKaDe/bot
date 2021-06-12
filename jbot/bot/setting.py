import json
from telethon import events, Button
from asyncio import exceptions
from .. import jdbot, chat_id, _botset
from .utils import split_list, logger,press_event


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='^/set$'))
async def myset(event):
    SENDER = event.sender_id
    try:
        msg = await jdbot.send_message(chat_id,'请稍后，正在查询')
        with open(_botset,'r',encoding='utf-8') as f:
            myset = json.load(f)
        info = '您目前设置如下：\n'
        for i in myset:
            info = info + f'\t\t- {i}-->{myset[i]} \n'
        info = info + '请点击您要设置的项目，选择后，输入要设置的值，重启生效,垃圾话以 | 进行区隔,黑名单以空格或逗号或顿号区隔'
        btn = [Button.inline(i,i) for i in myset]
        btn.append(Button.inline('取消', data='cancel'))
        btn = split_list(btn,3)
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await jdbot.edit_message(msg,info,buttons=btn)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
            else:
                await jdbot.delete_messages(chat_id,msg)
                msg = await conv.send_message(f'请输入您要修改的{res}\n如果为True或False首字符大写\n```{myset[res]}```')
                data = await conv.get_response()
                myset[res] = data.raw_text
                with open(_botset,'w+',encoding='utf-8') as f:
                    json.dump(myset,f)
                await jdbot.delete_messages(chat_id,msg)
                await jdbot.send_message(chat_id,'已完成修改，重启后生效')
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '选择已超时，对话已停止')
    except Exception as e:
        msg = await jdbot.edit_message(msg, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')
