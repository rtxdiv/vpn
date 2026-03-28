import os
from aiogram import Bot, Dispatcher


TOKEN = os.environ['MAIN_BOT_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher()

def register_routers():
    from src.bot.bot_commands import commands_router
    dp.include_router(commands_router)