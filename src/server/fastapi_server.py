from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette import status
from root import ROOT_DIR
from src.database.database_service import *
from src.utils.exceptions import *
from src.utils.logger_client import error_log
from .controllers.root_controller import root_router
from .controllers.payment_controller import payment_router
from .controllers.docs_controller import docs_router


PUBLIC_DIR = ROOT_DIR / 'public'

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')
app.include_router(root_router)
app.include_router(payment_router)
app.include_router(docs_router)

@app.exception_handler(ForeseenException)
def forseen_exception_handler(request: Request, exc: ForeseenException):
    raise HTTPException(status_code=400, detail=str(exc))

@app.exception_handler(Exception)
def forseen_exception_handler(request: Request, exc: Exception):
    error_log.error(exc)
    raise HTTPException(status_code=500, detail='Ошибка сервера')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # exc.errors() содержит список всех ошибок
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Ошибка валидации данных",
            "details": exc.errors()  # Здесь будут детали: какое поле и почему не подошло
        },
    )
