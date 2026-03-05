from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from auth import Validation, create_auth_guard
from xui_client import xui
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR.parent / 'public'

app = FastAPI()

app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')

validation = Validation(os.environ['MAIN_BOT_TOKEN'])
auth_guard = create_auth_guard(validation)

@app.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@app.get('/sub')
async def get_user(request: Request, _=Depends(auth_guard)):
    user = await xui.get_by_tgid(request.state.telegram_user['id'])
    return { 'user': user, 'subHost': os.environ['SUB_HOST'] }