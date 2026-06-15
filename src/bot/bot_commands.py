from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from src.utils.exceptions import *
from src.utils.logger_client import error_log
from .bot_server import ADMIN_ID
from src.database.database_service import *
import shlex


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

@commands_router.message(Command('compensation'))
async def cmd_compensation(ctx: Message, command: CommandObject):
    if str(ctx.from_user.id) != ADMIN_ID: return
    args = shlex.split(command.args)
    user = args[0]
    days = args[1]
    devices = args[2]
    message = args[3]

    try:
        if user == 'all':
            periods = await get_last_periods()
            print(str(periods), flush=True)
            await ctx.answer(str(len(periods)))
        else:
            period = await get_last_period(user_id=user)
            print(str(period), flush=True)
            await ctx.answer(str(period))

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
