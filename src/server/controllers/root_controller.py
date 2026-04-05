from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
from src.database.database_service import *
from root import PUBLIC_DIR


root_router = APIRouter(prefix='')

@root_router.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@root_router.get('/client')
@authorization
async def get_sub(request: Request):
    user_id = request.state.telegram_id
    last_period: UserPeriods = await get_active_period(user_id=user_id)
    if not last_period: return None
    client = await xui.get_by_tgid(user_id=user_id)
    if not client: raise ForeseenException('Клиент подключения отсутствует. Обратитесь в поддержку')
    return {
        'enable': client.enable,
        'tariff': last_period.tariffs.name,
        'limitIp': last_period.tariffs.devices,
        'expiry': (last_period.starts + timedelta(days=last_period.days)).isoformat(),
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