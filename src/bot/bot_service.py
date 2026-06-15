from aiogram import F, Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .bot_server import bot, ADMIN_ID, GROUP_ID
from src.utils.logger_client import error_log
from src.utils.funcs import format_date


service_router = Router()

async def send_new_payment(payment_id: str, amount: int, currency: str):
    try:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить', callback_data=f'process:{payment_id}')]
        ])
        await bot.send_message(
            ADMIN_ID,
            f'── <b>Новый платёж</b> ──────\n\n#<code>{payment_id}</code>\n└─ <b>{amount}{currency}</b>',
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления админу: {exc}')
        error_log.error(f'Ошибка отправки уведомления админу: {exc}')
        raise

async def send_processed_payment(user_id: str, payment_id: str, title: str):
    try:
        await bot.send_message(
            user_id,
            f'── <b>Платёж подтверждён</b> ────\n\n<b>{title}</b>\n<b>ID:</b> #{payment_id}',
            parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления пользователю: {exc}')
        error_log.error(f'Ошибка отправки уведомления пользователю: {exc}')
        raise

async def send_processed_compensation(user_id: str, days: int, starts: str, message: str):
    try:
        await bot.send_message(
            user_id,
            f'── <b>Компенсация</b> ────\n\n<b>Дни:</b> {days}\n<b>Начнётся</b>: {format_date(starts)}\n\n<i>{message}</i>',
            parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления пользователю: {exc}')
        error_log.error(f'Ошибка отправки уведомления пользователю: {exc}')
        raise

async def send_start():
    try:
        await bot.send_message(
            GROUP_ID,
            '▶️ App started'
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления о старте: {exc}')
        error_log.error(f'Ошибка отправки уведомления о старте: {exc}')
        raise

async def send_not_renewed(user_id: str, date: str):
    try:
        await bot.send_message(
            user_id,
            f'🔔 <b>Оплаченный VPN закончится {date} по МСК</b>\n\n<a href="t.me/rtxdiv_vpn_bot/app">Купить заранее</a>',
            parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления пользователю: {exc}')
        error_log.error(f'Ошибка отправки уведомления пользователю: {exc}')


@service_router.callback_query(F.data.regexp(r'^process:(.+)$'))
async def callback_process(callback: types.CallbackQuery):
    payment_id = callback.data.split(':')[1]
    if not payment_id: await callback.answer(f'❌ payment_id не передан')
    try:
        from src.database.database_service import process_payment
        await process_payment(payment_id=payment_id)
        await callback.answer(f'✅ Платёж {payment_id} успешно обработан')
        await callback.message.edit_text(text=f'✅ {callback.message.html_text}', reply_markup=None, parse_mode=ParseMode.HTML)

    except Exception as exc:
        await callback.answer(f'❌ {exc}')
