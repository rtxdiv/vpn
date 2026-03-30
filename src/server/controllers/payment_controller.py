from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import FileResponse
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
    type = 'Buy'
    id = request.state.telegram_user['id']
    
    try:
        starts = await get_user_periods_end(id=id)
        info: PaymentInfo = await get_payment_info(uname=dto.to_tariff_uname, months=dto.months)
        return {
            'title': info.title,
            'periods': info.periods,
            'starts': starts,
            'total': info.total
        }
    except Exception:
        return ForeseenException('Ошибка загрузки данных')