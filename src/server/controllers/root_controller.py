from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
from src.database.database_service import *
from root import PUBLIC_DIR
from src.utils.periods_info import PeriodsInfo


root_router = APIRouter(prefix='')

@root_router.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@root_router.get('/client')
@authorization
async def get_sub(request: Request):
    user_id = request.state.telegram_id
    active_periods: PeriodsInfo = await get_active_periods(user_id=user_id)
    if not active_periods.current: return None
    client = await xui.get_by_tgid(user_id=user_id)
    if not client: raise ForeseenException('Клиент подключения отсутствует. Обратитесь в поддержку')
    return {
        'enable': client.enable,
        'tariff': active_periods.current.tariffs.name,
        'limitIp': active_periods.current.tariffs.devices,
        'expiry': active_periods.current.ends.isoformat(),
        'featureCount': active_periods.feature_count,
        'subId': client.sub_id
    }

@root_router.get('/tariffs')
async def get_tariffs():
    return await get_all_tafiffs()

@root_router.get('/settings')
async def get_settings():
    return await get_all_settings()

@root_router.get('/paymentPeriods')
async def get_periods():
    return await get_all_allowed_periods()

@root_router.post('/resetSub')
@authorization
async def reset_sub(request: Request):
    user_id = request.state.telegram_id
    return await xui.reset_sub_id(user_id=user_id)