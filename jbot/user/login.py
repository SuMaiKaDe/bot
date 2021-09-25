from telethon import TelegramClient, events
import os
import asyncio,qrcode
from .. import API_HASH,API_ID,proxy,BOT,PROXY_START,PROXY_TYPE,connectionType,QR_IMG_FILE,jdbot,chat_id,CONFIG_DIR
if BOT.get('proxy_user') and BOT['proxy_user'] != "代理的username,有则填写，无则不用动":
    proxy = {
        'proxy_type': BOT['proxy_type'],
        'addr':  BOT['proxy_add'],
        'port': BOT['proxy_port'],
        'username': BOT['proxy_user'],
        'password': BOT['proxy_password']}
elif PROXY_TYPE == "MTProxy":
    proxy = (BOT['proxy_add'], BOT['proxy_port'], BOT['proxy_secret'])
else:
    proxy = (BOT['proxy_type'], BOT['proxy_add'], BOT['proxy_port'])
# 开启tg对话
if PROXY_START and BOT.get('noretry') and BOT['noretry']:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH, connection=connectionType,
                           proxy=proxy)
elif PROXY_START:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH, connection=connectionType,
                           proxy=proxy, connection_retries=None)
elif BOT.get('noretry') and BOT['noretry']:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH)
else:
    user = TelegramClient(f'{CONFIG_DIR}/user', API_ID, API_HASH,
                           connection_retries=None)

def creat_qr(text):
    '''实例化QRCode生成qr对象'''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.clear()
    # 传入数据
    qr.add_data(text)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    # 保存二维码
    img.save(QR_IMG_FILE)

@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'^/userlogin$'))
async def user_login(event):
    try:
        user.connect()
        qr_login = await user.qr_login()
        creat_qr(qr_login.url)
        await jdbot.send_message(chat_id,'请使用TG扫描二维码以开启USER',file=QR_IMG_FILE)
        await qr_login.wait(timeout=100)
        await jdbot.send_message(chat_id,'恭喜您已登录成功,请修改 /set 将开启user 改为True 并重启机器人 /reboot')
    except Exception as e:
        await jdbot.send_message(chat_id,'登录失败\n'+str(e))

@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'^/rmuser$'))
async def user_login(event):
    try:
        await jdbot.send_message(chat_id,'即将删除user.session')
        os.remove(f'{CONFIG_DIR}/user.session')
        await jdbot.send_message(chat_id,'已经删除user.session\n请重新登录')
    except Exception as e:
        await jdbot.send_message(chat_id,'删除失败\n'+str(e))


@jdbot.on(events.NewMessage(from_users=chat_id,pattern=r'^/codelogin$'))
async def user_login(event):
    try:
        await user.connect()
        async with jdbot.conversation(event.sender_id, timeout=100) as conv:
            msg = await conv.send_message('请输入手机号：\n例如：+8618888888888')
            phone = await conv.get_response()
            print(phone.raw_text)
            await user.send_code_request(phone.raw_text,force_sms=True)
            msg = await conv.send_message('请输入手机验证码:\n例如`code12345code`\n两侧code必须有')
            code = await conv.get_response()
            print(code.raw_text)
            await user.sign_in(phone.raw_text,code.raw_text.replace('code',''))
        await jdbot.send_message(chat_id,'恭喜您已登录成功,请修改 /set 将开启user 改为True 并重启机器人 /reboot')
    except asyncio.exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, '登录已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id,'登录失败\n 再重新登录\n'+str(e))
    finally:
        await user.disconnect()
