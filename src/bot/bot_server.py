import os
from aiogram import Bot, Dispatcher
from .bot_commands import commands_router


TOKEN = os.environ['MAIN_BOT_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(commands_router)