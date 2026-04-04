from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
from root import PUBLIC_DIR
from src.utils.auth_guard import authorization
from src.database.database_service import *
from src.utils.exceptions import *
from ..dto.payment_buy_dto import BuyDto


payment_router = APIRouter(prefix='/payments')

@payment_router.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'payments.html')

# page gets
@payment_router.get('/getAll')
@authorization
async def get_payments(request: Request):
    user_id = request.state.telegram_id
    return await get_all_payments(user_id)

@payment_router.get('/get')
@authorization
async def get_payment(request: Request, id: str):
    user_id = request.state.telegram_id
    payment: Payments = await get_user_payment(user_id=user_id, payment_id=id)
    payment_settings = await get_payment_settings()
    return {
        'paymentId': payment.payment_id,
        'title': payment.title,
        'amount': payment.amount,
        'currency': payment.currency,
        'settings': payment_settings
    }


# payment api
@payment_router.post('/buy')
@authorization
async def get_buy(request: Request, dto: BuyDto):
    user_id = request.state.telegram_id
    info: PaymentInfo = await prepare_buy(user_id=user_id, uname=dto.to_tariff, months=dto.months)
    return {
        'title': info.title,
        'starts': info.starts,
        'total': info.total
    }

@payment_router.post('/buy/pay')
@authorization
async def pay_buy(request: Request, dto: BuyDto):
    user_id = request.state.telegram_id
    payment_id: str = await prepare_buy(user_id=user_id, uname=dto.to_tariff, months=dto.months, pay=True)
    return {
        'payment_id': payment_id
    }