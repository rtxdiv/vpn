from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message as Ctx, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from xui import XUIClient
from datetime import datetime


class KButtons:
    TARIFF = "Мой тариф"
    HELP = "Помощь"

BotKB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=KButtons.TARIFF)],
        [KeyboardButton(text=KButtons.HELP)]
    ],
    resize_keyboard=True
)


class MainBot:
    def __init__(self, token, host, login, password):
        self._bot = Bot(token=token)
        self._dp = Dispatcher()
        self._dp.message.register(self.cmd_start, Command('start'))
        self._dp.message.register(self.kbd_tariff, F.text == KButtons.TARIFF)
        self._dp.message.register(self.cmd_add, Command('add'))
        self._xui = XUIClient(host, login, password)
        

    async def run(self):
        await self._xui.login()
        await self._dp.start_polling(self._bot)


    async def cmd_start(self, ctx: Ctx):
        await ctx.answer(f'Привет, {ctx.from_user.first_name}! Используй клавиатуру снизу для управления:', reply_markup=BotKB)

    async def kbd_tariff(self, ctx: Ctx):
        user = await self._xui.get_by_tgid(ctx.from_user.id)
        message = 'Не найдено тарифов, связанных с вашим аккаунтом'

        if user:
            ip_limit = user.limit_ip
            traffic = round((user.up + user.down) / (1024 * 1024 * 1024), 1)
            expiry = self.format_date(user.expiry_time)

            message = f'⭐️ <b>Ваш тариф</b>\n\nКоличество устройств: <b>{ip_limit or '♾️'}</b>\nИзрасходованный трафик: <b>{traffic}Gb / ♾️</b>\nДействует до: <b>{expiry}</b>'
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Конфигурация VPN', url='https://google.com')]])

        await ctx.answer(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    async def cmd_add(self, ctx: Ctx):
        await self._xui.create_client(ctx.from_user.id, 0, 0)
        await ctx.answer('OK')
    

    def format_date(self, timestamp):
        if timestamp <= 0: return '♾️'
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime('%d.%m.%Y')