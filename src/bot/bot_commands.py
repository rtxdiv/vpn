import time
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from src.utils.exceptions import *
from src.xui.xui_client import xui
from src.utils.logger_client import info_log, error_log
from src.database.database_service import get_sub_url
from src.bot.bot_server import bot


commands_router = Router()

@commands_router.message(Command('status'))
async def cmd_pay(ctx: Message):
    if ctx.from_user.username != 'rtxdiv': return
    print('--/status')
    await get_shop_info()
    await ctx.answer('Лог создан')

@commands_router.message(Command('update'))
async def cmd_reset(ctx: Message, command: CommandObject):
    try:
        await xui.reset_sub_id(command.args)
        await ctx.answer('ID подписки обновлён')
        
    except ForeseenException as e:
        await ctx.answer(str(e))
    except Exception as e:
        await ctx.answer('Ошибка сервера')
        error_log.error(str(e))

# @commands_router.message(Command('enable'))
async def cmd_enable(ctx: Message, command: CommandObject):
    try:
        ### await xui.enable_client(command.args, )
        #
        # ЛОГИКА:
        # если expiry < NOW, то прибавить к текущему expiry
        # иначе прибавить expiry к NOW
        #
        await ctx.answer('Срок подписки обновлён')
        
    except ForeseenException as e:
        await ctx.answer(str(e))
    except Exception as e:
        await ctx.answer('Ошибка сервера')
        error_log.error(str(e))

@commands_router.message(Command('disable_message'))
async def cmd_enable(ctx: Message, command: CommandObject):
    try:
        message = '❗ *Доступ к PROMO-подписке приосановлен администратором*\n'
        message += '\nПо всем вопросам: @rtxdiv'
        await bot.send_message(chat_id=command.args, text=message, parse_mode=ParseMode.MARKDOWN)
        await ctx.answer('Отправлено!')
        
    except Exception as e:
        await ctx.answer(f'Произошла ошибка: {e}')
        print(e)