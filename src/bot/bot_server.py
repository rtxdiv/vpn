import os
from aiogram import Bot, Dispatcher


TOKEN = os.environ['MAIN_BOT_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher()

import bot_commands