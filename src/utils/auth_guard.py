from init_data_py import InitData
from src.utils.exceptions import ForeseenException, TelegramAuthError
from fastapi import Request
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
        if not auth or not auth.startswith('Telegram '):
            raise ForeseenException('Необходима авторизация через <a href="https://t.me/rtdVpn/app">Telegram</a>')

        init_data = auth[9:]
        try:
            user = validate(init_data)
            print(f'Auth passed: { user["id"] }', flush=True)
            request.state.telegram_user = user
        except TelegramAuthError as e:
            raise ForeseenException('Ошибка авторизации')

        return await func(*args, **kwargs)
    return wrapper