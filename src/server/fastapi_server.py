from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from root import ROOT_DIR
from src.database.database_service import *
from src.utils.exceptions import *
from src.utils.logger_client import error_log
from .controllers.root_controller import root_router
from .controllers.payment_controller import payment_router


PUBLIC_DIR = ROOT_DIR / 'public'

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')
app.include_router(root_router)
app.include_router(payment_router)

@app.exception_handler(ForeseenException)
def forseen_exception_handler(request: Request, exc: ForeseenException):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc)}
    )

@app.exception_handler(Exception)
def forseen_exception_handler(request: Request, exc: Exception):
    error_log.error(exc)
    return JSONResponse(
        status_code=500,
        content={'detail': 'Ошибка сервера'}
    )
