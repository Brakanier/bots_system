import asyncio

from tortoise import Tortoise

import config
from Manager import Manager


api_id = config.API_ID
api_hash = config.API_HASH
manager = Manager(api_id, api_hash)

async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']},
    )
    
    await manager.init()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(init())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        if not manager.checking_task.cancelled:
            manager.checking_task.cancel()
        loop.run_until_complete(Tortoise.close_connections())
        loop.stop()
    finally:
        loop.close()
    

