from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from src.utils.auth_guard import authorization
from src.xui.xui_client import xui
from root import ROOT_DIR
from src.database.database_service import *
from src.utils.exceptions import *
from src.utils.logger_client import error_log


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
    return await get_all_tafiffs()

@app.exception_handler(ForeseenException)
def forseen_exception_handler(exc: ForeseenException):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)}
    )

@app.exception_handler(Exception)
def forseen_exception_handler(exc: ForeseenException):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={'detail': 'Ошибка сервера'}
    )
