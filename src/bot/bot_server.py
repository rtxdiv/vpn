import os
from aiogram import Bot, Dispatcher


TOKEN = os.environ['MAIN_BOT_TOKEN']
ADMIN_ID = os.environ['ADMIN_ID']

bot = Bot(token=TOKEN)
dp = Dispatcher()

def register_routers():
    from src.bot.bot_commands import commands_router
    from src.bot.bot_service import service_router
    dp.include_router(commands_router)
    dp.include_router(service_router)