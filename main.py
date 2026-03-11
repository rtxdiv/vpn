from dotenv import load_dotenv
load_dotenv()
import asyncio
import uvicorn
from src.server.fastapi_server import app
from src.xui.xui_client import xui
from src.bot.bot_server import bot, dp
from src.database.models import Tariffs


async def main():
    config = uvicorn.Config(app, host='localhost', port=8000)
    server = uvicorn.Server(config)
    await xui.login()
    await bot.delete_webhook(drop_pending_updates=True)
    
    await asyncio.gather(
        server.serve(),
        asyncio.create_task(dp.start_polling(bot)),
        return_exceptions=True
    )

if __name__ == '__main__':
    asyncio.run(main())