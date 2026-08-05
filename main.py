from dotenv import load_dotenv
load_dotenv()
import asyncio
import uvicorn
from src.server.fastapi_server import app
from src.xui.xui_client import xui
from src.bot.bot_server import bot, dp, register_routers
from src.bot.bot_service import send_system_message
import os


async def main():
    config = uvicorn.Config(app, host=os.environ['APP_HOST'], port=int(os.environ['APP_PORT']))
    server = uvicorn.Server(config)
    await xui.login()
    await bot.delete_webhook(drop_pending_updates=True)
    register_routers()

    from src.cron import notify, limit
    await send_system_message('▶️ App started')

    await asyncio.gather(
        server.serve(),
        asyncio.create_task(dp.start_polling(bot, timeout=60, relax=5, fast=True)),
        return_exceptions=True
    )


if __name__ == '__main__':
    asyncio.run(main())