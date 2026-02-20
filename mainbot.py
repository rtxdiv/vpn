from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message as Ctx, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from xui import XUIClient
from datetime import datetime


class MainBot:
    def __init__(self, token, host, login, password, sub_host):
        self._bot = Bot(token=token)
        self._dp = Dispatcher()
        self._dp.message.register(self.cmd_start, Command('start'))
        self._dp.message.register(self.cmd_add, Command('add'))
        self._dp.callback_query.register(self.cb_tariff, F.data == 'cb_tariff')
        self._dp.callback_query.register(self.cb_help, F.data == 'cb_help')
        self._dp.callback_query.register(self.cb_already_bought, F.data == 'cb_already_bought')
        self._xui = XUIClient(host, login, password)
        self._sub_host = sub_host
        

    async def run(self):
        await self._xui.login()
        await self._dp.start_polling(self._bot)


    async def cmd_start(self, ctx: Ctx):
        user = await self._xui.get_by_tgid(ctx.from_user.id)
        keyboard = None
        message = f'<b>Здравствуйте, {ctx.from_user.first_name}!</b> Здесь вы можете получить информацию о тарифе и управлять подпиской'

        if user:
            message += f'\n\n🟢 <b>Подписка активна</b>\nдействует до: {self.format_date(user.expiry_time)}'
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
        user = await self._xui.get_by_tgid(call.from_user.id)
        message = 'Не найдено тарифов, связанных с вашим аккаунтом. Купите подписку или обратитесь в поддержку'
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить подписку', url='https://t.me/rtxdiv_production')]])

        if user:
            message = f'⭐️ <b>Ваш тариф</b>'
            message += f'\n\nКоличество устройств: <b>{user.limit_ip or '♾️'}</b>'
            message += f'\n\n<b>Трафик:</b>'
            message += f'\n├ up: {self.to_gb(user.up)} Gb'
            message += f'\n├ down: {self.to_gb(user.down)} Gb'
            message += f'\n└ <b>общий: {self.to_gb(user.up + user.down)} Gb / ♾️</b>'
            message += f'\n\nПодписка действует до: <b>{self.format_date(user.expiry_time)}</b>'

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Конфигурация VPN', url=f'{self._sub_host}/{user.uuid}')]])
        
        await call.answer()
        await call.message.answer(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    async def cb_already_bought(self, call: CallbackQuery):
        await call.answer()
        await call.message.answer(f'<b>ID:</b> {call.from_user.id}', parse_mode=ParseMode.HTML)
    
    async def cb_help(self, call: CallbackQuery):
        await call.answer()
        await call.message.answer('Тут будет помощь')


    async def cmd_add(self, ctx: Ctx):
        await self._xui.create_client(ctx.from_user.id, 0, 0)
        await ctx.answer('Created')


    def format_date(self, timestamp):
        if timestamp <= 0: return '♾️'
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime('%d.%m.%Y')
    
    def to_gb(self, bytes):
        return round(bytes / (1024 * 1024 * 1024), 1)