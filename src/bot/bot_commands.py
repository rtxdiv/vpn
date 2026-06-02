from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from src.utils.exceptions import *
from src.utils.logger_client import error_log
from .bot_server import ADMIN_ID
from src.database.database_service import *


commands_router = Router()

@commands_router.message(Command('process'))
async def cmd_process(ctx: Message, command: CommandObject):
    if str(ctx.from_user.id) != ADMIN_ID: return
    try:
        await process_payment(payment_id=command.args)
        await ctx.answer('Платёж обработан')
        
    except ForeseenException as e:
        await ctx.answer(str(e))
    except Exception as e:
        await ctx.answer('Ошибка сервера')
        error_log.error(str(e))

@commands_router.message(Command('notify'))
async def cmd_notify(ctx: Message):
    if str(ctx.from_user.id) != ADMIN_ID: return
    try:
        periods = await get_not_renewed()
        print(str(periods), flush=True)
        await ctx.answer(str(periods))
        
    except ForeseenException as e:
        await ctx.answer(str(e))

@commands_router.message(Command('newperiods'))
async def cmd_notify(ctx: Message):
    if str(ctx.from_user.id) != ADMIN_ID: return
    try:
        periods = await get_new_periods()
        print(str(periods), flush=True)
        await ctx.answer(str(periods))
        
    except ForeseenException as e:
        periods = await ctx.answer(str(e))
