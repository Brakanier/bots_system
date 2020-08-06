import asyncio
from datetime import date
import time
import datetime

from pyrogram import Client, MessageHandler, Message
from pyrogram.client.methods.decorators import on_message

import models

class Bot:
    def __init__(self, login, api_id, api_hash, run_all):
        self.login = login
        self.run_all = run_all
        self.client = Client(f'sessions/{self.login}', api_id, api_hash)
        self.client.add_handler(MessageHandler(self.on_message))
        self.check_new = False
        self.inwork = False
        self.click_time = time.time()
        self.start_time = None
    
    async def start(self):
        await self.client.start()
        await self.client.join_chat('@teleprofiitbot_teleprofitbot')

    async def run(self, check_new=False):
        if check_new:
            self.check_new = True
        
        self.inwork = True
        self.start_time = time.time()
        await self.client.send_message(461620250, '💸️ Заработать')
        

    async def on_message(self, client: Client, message: Message):
        if message.from_user and message.from_user.id == 461620250:
            print('Step', time.time() - self.start_time)
            if message.text == "Подпишись на этот канал и получи вознаграждение!":
                if self.check_new:
                    self.check_new = False
                    await self.run_all()
                    print('Let`s work!')
                    return
                chat_id = '@' + message.reply_markup.inline_keyboard[0][0].url.split('/')[-1]
                await client.join_chat(chat_id)
                #await self.sub(chat_id)
                try:
                    await self.click(message, 1)
                    self.inwork = False
                    print('Sum time:', time.time() - self.start_time)
                except:
                    pass
            elif 'Оповещения о новых заданиях' in message.text:
                try:
                    await self.click(message, 0)
                except:
                    pass
            elif "Спасибо за подписку" in message.text:
                pass
            elif 'Пока нет каналов для подписки, попробуй позднее' in message.text:
                self.inwork = False
    

    async def click(self, message, index):
        delta = time.time() - self.click_time
        if delta < 1:
            print('click delta', delta)
            await asyncio.sleep(1)
        try:
            await message.click(index)
        except:
            pass
        self.click_time = time.time()
    
    async def sub(self, channel_name):
        account = await models.Account.get(login=self.login)
        unsub = datetime.datetime.now() + datetime.timedelta(days=8)
        await models.Sub.create(account=account, channel_name=channel_name, unsub_datetime=unsub)