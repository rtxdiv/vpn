from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message as Ctx, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from xui import XUIClient
from datetime import datetime
from exceptions import ForeseenException
import time
import os


class MainBot:
    def __init__(self, token: str):
        self._bot = Bot(token)
        self._xui = XUIClient()
        self._sub_host = os.environ['PANEL_SUB_HOST']

        self._dp = Dispatcher()
        # self._dp.message.register(self.cmd_start, Command('start'))
        # self._dp.message.register(self.cmd_add, Command('add'))
        self._dp.message.register(self.cmd_bonus, Command('bonus'))
        # self._dp.message.register(self.cmd_reset, Command('update'))
        # self._dp.callback_query.register(self.cb_tariff, F.data == 'cb_tariff')
        # self._dp.callback_query.register(self.cb_help, F.data == 'cb_help')
        # self._dp.callback_query.register(self.cb_already_bought, F.data == 'cb_already_bought')
        
    async def run(self):
        await self._xui.login()
        await self._dp.start_polling(self._bot)


    async def cmd_start(self, ctx: Ctx):
        client = await self._xui.get_by_tgid(ctx.from_user.id)
        keyboard = None
        message = f'<b>Здравствуйте, {ctx.from_user.first_name}!</b> Здесь вы можете получить информацию о тарифе и управлять подпиской'

        if client:
            message += f'\n\n🟢 <b>Подписка активна</b>\nдействует до: {self.format_date(client.expiry_time)}'
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Мой тариф', callback_data='cb_tariff')],
                [InlineKeyboardButton(text='Помощь', callback_data='cb_help')]
            ])
        else:
            message += f'\n\n🔴 <b>Нет подписки</b>'
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Купить подписку', url='https://t.me/rtxdiv_production')],
                [InlineKeyboardButton(text='Я уже купил', callback_data='cb_already_bought')]
            ])

        await ctx.answer(message, reply_markup=keyboard, parse_mode=ParseMode.HTML)


    async def cb_tariff(self, call: CallbackQuery):
        client = await self._xui.get_by_tgid(call.from_user.id)
        message = 'Не найдено тарифов, связанных с вашим аккаунтом. Купите подписку или обратитесь в поддержку'
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить подписку', url='https://t.me/rtxdiv_production')]])

        if client:
            message = f"⭐️ <b>Ваш тариф</b>"
            message += f"\n\nКоличество устройств: <b>{client.limit_ip if client.limit_ip != '0' else 'Бесконечно'}</b>"
            message += f"\n\n<b>Трафик:</b>"
            message += f"\n├ up: {self.to_gb(client.up)} Gb"
            message += f"\n├ down: {self.to_gb(client.down)} Gb"
            message += f"\n└ <b>общий: {self.to_gb(client.up + client.down)} Gb / Безлимит</b>"
            message += f"\n\nПодписка действует до: <b>{self.format_date(client.expiry_time)}</b>"

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Конфигурация VPN', url=f'{self._sub_host}/{client.sub_id}')]])
        
        await call.answer()
        await call.message.answer(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    async def cb_already_bought(self, call: CallbackQuery):
        await call.answer()
        await call.message.answer(f'<b>ID:</b> {call.from_user.id}', parse_mode=ParseMode.HTML)
    
    async def cb_help(self, call: CallbackQuery):
        await call.answer()
        await call.message.answer('Тут будет помощь')


    async def cmd_add(self, ctx: Ctx):
        try:
            await self._xui.create_client(ctx.from_user.id, 5, 0)
            await ctx.answer('Подписка зарегистрирована')

        except ForeseenException as e:
            await ctx.answer(str(e))
        except Exception as e:
            await ctx.answer('Произошла непредвиденная ошибка')
            print(e)

    async def cmd_reset(self, ctx: Ctx, command: CommandObject):
        try:
            await self._xui.reset_sub_id(command.args)
            await ctx.answer('Подписка обновлена')

        except ForeseenException as e:
            await ctx.answer(str(e))
        except Exception as e:
            await ctx.answer('Произошла непредвиденная ошибка')
            print(e)

    # IN DEVELOPMENT
    async def cmd_bonus(self, ctx: Ctx, command: CommandObject):
        if (command.args != 'PROMO-30'): return

        days = 30
        message = f'*Вы получили бесплатную подписку на {days} дней!*\n\n'
        message += f'*Как активировать?*\n'
        message += f'1. Откройте подписку и нажмите на QR-код, чтобы скопировать ссылку на конфигурацию\n'
        message += f'2. Скачайте любой VPN клиент (v2RayRun на Android)\n'
        message += f'3. В приложении найдите кнопку добавления конфигурации\n'
        message += f'4. Добавьте скопированную ссылку или отсканируйте QR-код (пункт 1)'
        sub_url = None

        try:
            client = await self._xui.get_by_tgid(ctx.from_user.id)
            if (not client): 
                expiry = int(time.time() * 1000) + (days * 24 * 60 * 60 * 1000)
                new_client = await self._xui.create_client(ctx.from_user.id, 1, expiry, 'PROMO-30')
                sub_url = f'{self._sub_host}/{new_client.sub_id}'
            else:
                message = f'*У вас уже есть подписка!*'
                sub_url = f'{self._sub_host}/{client.sub_id}'

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подписка', url=sub_url)]])
            message += f'\n\n💚 *По всем вопросам: @rtxdiv*'
            
            await ctx.answer(message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

        except ForeseenException as e:
            await ctx.answer(str(e))
        except Exception as e:
            await ctx.answer('Произошла непредвиденная ошибка')
            print(e)


    def format_date(self, timestamp):
        if timestamp <= 0: return 'Бессрочно'
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime('%d.%m.%Y')
    
    def to_gb(self, bytes):
        return round(bytes / (1024 * 1024 * 1024), 1)