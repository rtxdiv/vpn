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
            f'Получен новый платёж\n\n#*{payment_id}*\n└─ *{amount}{currency}*',
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as exc:
        print(f'Ошибка отправки уведомления админу: {exc}')
        error_log.error(f'Ошибка отправки уведомления админу: {exc}')
        raise

    
@service_router.callback_query(F.data.regexp(r'^process:(.+)$'))
async def callback_process(callback: types.CallbackQuery):
    payment_id = callback.data.split(':')[1]
    if not payment_id: callback.answer(text=f'Платёж {payment_id} успешно обработан')
    try:
        from src.database.database_service import process_payment
        await process_payment(payment_id=payment_id)
    except Exception as exc:
        callback.answer(text=f'Ошибка: {exc}')
