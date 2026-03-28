from .http_client import get_session
from aiohttp import ClientSession


def create_payment(session: ClientSession):
    session = get_session()
    print('okak')