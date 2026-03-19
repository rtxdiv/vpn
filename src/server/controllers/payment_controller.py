from fastapi import Request, APIRouter, HTTPException
from src.utils.auth_guard import authorization
from src.database.database_service import *
from src.utils.exceptions import *


payment_router = APIRouter(prefix='/payment')

@payment_router.post('/buy')
@authorization
async def prepare_buy(request: Request):
    for_pay = False
    id = request.state.telegram_user['id']
    if not for_pay: pay_link = None
    try:
        starts = await get_user_periods_end(id=id)
        (total, tariff) = await get_tariff_and_price(uname='fn-solo', months=2)
        return { starts: starts, tariff: tariff, total: total, pay_link: pay_link }
    
    except ForeseenException:
        raise HTTPException(status_code=400, detail='Выбранный тариф или период не предусмотрен')