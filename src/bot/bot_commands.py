import time
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from src.utils.exceptions import *
from src.xui.xui_client import xui
from src.utils.logger_client import info_log, error_log
from src.database.database_service import get_sub_url
from .bot_server import bot

commands_router = Router()

@commands_router.message(Command('activate'))
async def cmd_activate(ctx: Message, command: CommandObject):
    if command.args != 'PROMO-30': return

    days = 30
    message = f'*Вы получили бесплатную подписку на {days} дней!*\n'
    message += '\n*Как активировать?*\n'
    message += '1. Откройте подписку и нажмите на QR-код, чтобы скопировать ссылку на конфигурацию\n'
    message += '2. Скачайте любой VPN клиент (v2RayRun на Android)\n'
    message += '3. В приложении найдите кнопку добавления конфигурации\n'
    message += '4. Добавьте скопированную ссылку или отсканируйте QR-код (пункт 1)\n'
    subscription = None

    try:
        sub_url = await get_sub_url()
        client = await xui.get_by_tgid(ctx.from_user.id)
        if not client:
            expiry = int(time.time() * 1000) + (days * 24 * 60 * 60 * 1000)
            new_client = await xui.create_client(ctx.from_user.id, 1, expiry, 'PROMO-30')
            info_log.info(f'[NEW PROMO-30 USER] id: {ctx.from_user.id} | username: {ctx.from_user.username} | first_name: {ctx.from_user.first_name} | last_name: {ctx.from_user.last_name}')
            subscription = f'{sub_url}{new_client.sub_id}'
        else:
            message = '*У вас уже есть подписка!*\n'
            subscription = f'{sub_url}{client.sub_id}'

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Подписка', url=subscription)]
            ]
        )
        message += '\n🗳️ Поучаствуйте в голосовании: @rtdVpn\n💚 По всем вопросам: @rtxdiv'

        await ctx.answer(message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

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