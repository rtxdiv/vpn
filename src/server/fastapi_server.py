from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
from root import ROOT_DIR
from src.database.database_service import *


app = FastAPI()

PUBLIC_DIR = ROOT_DIR / 'public'
app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')

@app.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@app.get('/sub')
@authorization
async def get_sub(request: Request):
    return await xui.get_by_tgid(request.state.telegram_user['id'])

@app.get('/tariffs')
async def get_tariffs():
    # return await get_all_tafiffs()
    return None