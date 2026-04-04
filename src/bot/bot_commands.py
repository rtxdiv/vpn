from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from src.utils.exceptions import *
from src.xui.xui_client import xui
from src.utils.logger_client import error_log
from src.bot.bot_server import bot
from src.database.database_service import *


commands_router = Router()

@commands_router.message(Command('process'))
async def cmd_process(ctx: Message, command: CommandObject):
    try:
        await process_payment(payment_id=command.args)
        
    except ForeseenException as e:
        await ctx.answer(str(e))
    except Exception as e:
        await ctx.answer('Ошибка сервера')
        error_log.error(str(e))

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

@commands_router.message(Command('enable'))
async def cmd_enable(ctx: Message):
    try:
        await xui.enable_client(
            user_id=str(ctx.from_user.id),
            limit_ip=5,
            days=30,
            reset=30,
            comment='ADMIN'
        )
        await ctx.answer('Клиент активирован')
        
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
