from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
from src.database.database_service import *
from root import ROOT_DIR


PUBLIC_DIR = ROOT_DIR / 'public'

root_router = APIRouter(prefix='')

@root_router.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@root_router.get('/client')
@authorization
async def get_sub(request: Request):
    return await xui.get_by_tgid(request.state.telegram_user['id'])

@root_router.get('/tariffs')
async def get_tariffs():
    return await get_all_tafiffs()

@root_router.get('/settings')
async def get_settings():
    return await get_all_settings()