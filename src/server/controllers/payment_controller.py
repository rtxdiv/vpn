from fastapi import Request, APIRouter
from src.utils.auth_guard import authorization
from src.database.database_service import *
from root import ROOT_DIR

payment_router = APIRouter(prefix='/payment')

@authorization
@payment_router.post('/buy')
def prepare_buy(request: Request):
    request.state.telegram_user['id']
