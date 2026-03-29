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
async def prepare_buy(request: Request, dto: BuyDto):
    print(f"to_tariff_uname: {dto.to_tariff_uname}", flush=True)
    print(f"months: {dto.months}", flush=True)
    print(f"for_pay: {dto.for_pay}", flush=True)

    type = 'Buy'
    pay_link = None
    id = request.state.telegram_user['id']

    try:
        starts = await get_user_periods_end(id=id)
        (tariff, periods, total, months) = await get_tariff_and_price(uname=dto.uname, months=dto.months)
        return {
            'tariff': tariff,
            'periods': periods,
            'starts': starts,
            'months': months,
            'total': total,
            'pay_link': pay_link
        }
    
    except ForeseenException:
        raise HTTPException(status_code=400, detail='Выбранный тариф или период не предусмотрен')