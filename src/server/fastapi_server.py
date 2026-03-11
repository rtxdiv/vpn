from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
import os
from root import ROOT_DIR


app = FastAPI()

PUBLIC_DIR = ROOT_DIR / 'public'
app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')

@app.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@app.get('/sub')
@authorization
async def get_user(request: Request):
    user = await xui.get_by_tgid(request.state.telegram_user['id'])
    return { 'user': user, 'subHost': os.environ['SUB_HOST'] }