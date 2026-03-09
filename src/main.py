from dotenv import load_dotenv
load_dotenv()
import asyncio
import uvicorn
from server import app
from xui_client import xui
from mainbot import bot, dp
from models import Tariffs
from database_client import with_session, AsyncSession
from sqlalchemy import select, update, delete

# @with_session + main(session: AsyncSession)
async def main():
    config = uvicorn.Config(app, host='localhost', port=8000)
    server = uvicorn.Server(config)
    await xui.login()
    await bot.delete_webhook(drop_pending_updates=True)

    # tariffs = await session.execute(select(Tariffs))
    # print(tariffs.scalars().all())
    
    await asyncio.gather(
        server.serve(),
        asyncio.create_task(dp.start_polling(bot)),
        return_exceptions=True
    )

if __name__ == '__main__':
    asyncio.run(main())