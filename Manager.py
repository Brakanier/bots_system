import asyncio
import random
import datetime

from Bot import Bot
import models

class Manager:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.loop = None
        self.bots = []
        self.checking_task = None
    
    async def init(self):
        self.loop = asyncio.get_running_loop()
        accounts = await models.Account.all()
        for a in accounts:
            bot = Bot(a.login, self.api_id, self.api_hash, self.run_all)
            await bot.start()
            self.bots.append(bot)
        await self.checking_on()
    
    async def run_all(self):
        await self.checking_off()
        # await asyncio.sleep(5) # simulate work
        # await self.checking_on()
        
        tasks = []
        for bot in self.bots:
            task = self.loop.create_task(bot.run())
            tasks.append(task)
        print('Tasks created', len(tasks))
        await asyncio.gather(*tasks)
        print('Tasks ready')
        print('Inwork', next(filter(lambda b: b.inwork, self.bots)))
        while next(filter(lambda b: b.inwork, self.bots), False):
            await asyncio.sleep(0.1)
        await self.checking_on()

    async def check_new_task(self):
        while True:
            print(f'Check new task - {datetime.datetime.now()}')
            bot = random.choice(self.bots)
            await bot.run(check_new=True)
            await asyncio.sleep(5)
    
    async def checking_off(self):
        print('Checking off')
        if not self.checking_task.cancelled():
            self.checking_task.cancel()
            self.checking_task = None
    
    async def checking_on(self):
        print('Checking on')
        if not self.checking_task:
            self.checking_task = self.loop.create_task(self.check_new_task())
