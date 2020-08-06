import asyncio
from tortoise import Tortoise
from pyrogram import Client

import config
import models


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()
    
    ## add account to DB
    api_id = config.API_ID
    api_hash = config.API_HASH
    
    login = input('Please enter session file name(login): ')
    
    client = Client(f'sessions/{login}', api_id, api_hash)
    await client.start()
    exists = await models.Account.get_or_none(login=login)
    if not exists:
        await models.Account.create(login=login)
    await client.stop()
    await Tortoise.close_connections()
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())