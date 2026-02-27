from init_data_py import InitData
from exceptions import TelegramAuthError
from fastapi import Request, HTTPException
from functools import wraps
from contextvars import ContextVar

# Создаем ContextVar для хранения данных пользователя (аналог flask.g)
telegram_user_var = ContextVar("telegram_user", default=None)
user_id_var = ContextVar("user_id", default=None)

class Validation:
    def __init__(self, token: str):
        self._token = token

    def validate(self, init_data: str) -> dict:
        data = InitData.parse(init_data)
        
        if not data.validate(self._token, lifetime=86400):
            raise TelegramAuthError('Invalid init data')
        
        if not data.user:
            raise TelegramAuthError('No user data')
        
        return data.user.to_dict()


def auth_guard(auth: Validation):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, request: Request, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                raise HTTPException(status_code=401, detail='Missing Authorization header')
            
            if not auth_header.startswith('Telegram '):
                raise HTTPException(status_code=401, detail='Invalid Authorization format. Use: Telegram <init_data>')
            
            init_data = auth_header[9:]
            
            try:
                user = auth.validate(init_data)
                telegram_user_var.set(user)
                user_id_var.set(user['id'])
                
                request.state.telegram_user = user
                request.state.user_id = user['id']
                
                return await f(*args, **kwargs)
                
            except TelegramAuthError as e:
                raise HTTPException(status_code=403, detail=str(e))
        
        return decorated_function
    return decorator