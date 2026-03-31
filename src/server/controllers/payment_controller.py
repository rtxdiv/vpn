from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from root import PUBLIC_DIR
from src.utils.auth_guard import authorization
from src.database.database_service import *
from src.utils.exceptions import *
from ..dto.payment_buy_dto import BuyDto


payment_router = APIRouter(prefix='/payments')

@payment_router.get('/')
async def get_payments():
    return FileResponse(PUBLIC_DIR / 'payments.html')

@payment_router.post('/buy')
@authorization
async def get_buy(request: Request, dto: BuyDto):
    id = request.state.telegram_user['id']
    starts = await get_user_periods_end(id=id)
    info: PaymentInfo = await prepare_buy(user_id=id, uname=dto.to_tariff, months=dto.months)
    return {
        'title': info.title,
        'periods': info.periods,
        'starts': starts,
        'total': info.total
    }

@payment_router.post('/buy/pay')
@authorization
async def pay_buy(request: Request, dto: BuyDto):
    id = request.state.telegram_user['id']
    payment_id: str = await prepare_buy(user_id=id, uname=dto.to_tariff, months=dto.months, pay=True)
    return RedirectResponse(url=f'https://vapp.rtxdiv.ru/payments?id={payment_id}')