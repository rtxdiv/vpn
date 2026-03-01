from init_data_py import InitData
from exceptions import TelegramAuthError
from fastapi import Request, HTTPException, Header
from typing import Optional

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


def create_auth_guard(validation: Validation):
    async def auth_guard_dependency(
        request: Request,
        authorization: Optional[str] = Header(None)
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail='Missing Authorization header')
        if not authorization.startswith('Telegram '):
            raise HTTPException(status_code=401, detail='Invalid Authorization format. Use: Telegram <init_data>')
        
        init_data = authorization[9:]
        try:
            user = validation.validate(init_data)
            request.state.telegram_user = user
        except TelegramAuthError as e:
            raise HTTPException(status_code=403, detail=str(e))
    
    return auth_guard_dependency