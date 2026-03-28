from dotenv import load_dotenv
load_dotenv()
import asyncio
import uvicorn
from src.server.fastapi_server import app
from src.xui.xui_client import xui
from src.bot.bot_server import bot, dp, register_routers
from src.http.http_client import init_http_session, close_http_session


async def main():
    config = uvicorn.Config(app, host='localhost', port=8000)
    server = uvicorn.Server(config)
    await xui.login()
    await bot.delete_webhook(drop_pending_updates=True)
    register_routers()

    await init_http_session()
    try:
        await asyncio.gather(
            server.serve(),
            asyncio.create_task(dp.start_polling(bot)),
            return_exceptions=True
        )
    finally:
        await close_http_session()

if __name__ == '__main__':
    asyncio.run(main())