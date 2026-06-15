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
    try:
        user_id = args[0] # user_id | all
        days = int(args[1])
        tariff_uname = args[2] # uname | aslast
        message = args[3]
    except: return ctx.answer('Неправильный формат команды')

    try:
        if user_id == 'all':
            periods: list[UserPeriods] = await get_last_active_periods()
            errors = []
            for period in periods:
                try:
                    await process_compensation(
                        user_id=period.user_id,
                        days=days,
                        tariff_uname=period.tariff_uname if tariff_uname == 'aslast' else tariff_uname,
                        starts=period.ends,
                        message=message
                    )
                except Exception as e:
                    errors.append(period)
                    error_log.error(str(e))
            if errors:
                print(f'Ошибки начисления компенсаций: {errors}', flush=True)
                error_log.error(f'Ошибки начисления компенсаций: {errors}')
            await ctx.answer(f'Компенсация начислена\nОшибок: {len(errors)} из {len(periods)}')

        else:
            period: UserPeriods = await get_last_active_period(user_id=user_id)
            await process_compensation(
                user_id=user_id,
                days=days,
                tariff_uname=period.tariff_uname if tariff_uname == 'aslast' else tariff_uname,
                starts=period.ends,
                message=message
            )
            await ctx.answer('Компенсация начислена')

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
