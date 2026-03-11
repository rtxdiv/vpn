from dotenv import load_dotenv
load_dotenv()
import asyncio
import uvicorn
from src.server.fastapi_server import app
from src.xui.xui_client import xui
from src.bot.bot_server import bot, dp
from src.database.models import Tariffs
from src.database.database_client import with_session, AsyncSession
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