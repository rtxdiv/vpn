from init_data_py import InitData
from src.utils.exceptions import TelegramAuthError
from fastapi import Request, HTTPException
from functools import wraps
import os


def validate(init_data: str) -> dict:
    data = InitData.parse(init_data)
    if not data.validate(os.environ['MAIN_BOT_TOKEN'], lifetime=86400):
        raise TelegramAuthError('Invalid init data')
    if not data.user:
        raise TelegramAuthError('No user data')
    return data.user.to_dict()


def authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs['request'] or None
        auth: str = request.headers.get('Authorization')
        if not auth:
            raise HTTPException(status_code=401, detail='Missing Authorization header')
        if not auth.startswith('Telegram '):
            raise HTTPException(status_code=401, detail='Invalid Authorization format. Use: Telegram <init_data>')

        init_data = auth[9:]
        try:
            user = validate(init_data)
            print(f'Auth passed: { user["id"] }', flush=True)
            request.state.telegram_user = user
        except TelegramAuthError as e:
            raise HTTPException(status_code=403, detail=str(e))

        return await func(*args, **kwargs)
    return wrapper