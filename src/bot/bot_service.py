from aiogram import F, Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .bot_server import bot, ADMIN_ID
from src.utils.logger_client import error_log


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
            f'─💲─ <b>Платёж подтверждён</b> ────\n\n<b>{title}</b>\n<b>ID:</b> #{payment_id}',
            parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления пользователю: {exc}')
        error_log.error(f'Ошибка отправки уведомления админу: {exc}')
        raise
    

@service_router.callback_query(F.data.regexp(r'^process:(.+)$'))
async def callback_process(callback: types.CallbackQuery):
    payment_id = callback.data.split(':')[1]
    if not payment_id: await callback.answer(f'❌ payment_id не передан')
    try:
        from src.database.database_service import process_payment
        await process_payment(payment_id=payment_id)
        await callback.answer(f'✅ Платёж {payment_id} успешно обработан')
        t = callback.message.html_text
        await callback.message.edit_text(text=f'{t[:1] + "☑️" + t[1:]}', reply_markup=None, parse_mode=ParseMode.HTML)

    except Exception as exc:
        await callback.answer(f'❌ {exc}')
