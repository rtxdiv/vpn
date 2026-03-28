import aiohttp
import os


session: aiohttp.ClientSession | None = None

async def init_http_session():
    if session is None:
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60),
            headers={
                'Content-Type': 'application/json',
                'x-shop': os.environ['SHOP_ID'],
                'x-secret': os.environ['SHOP_SECRET']
            }
        )

async def close_http_session():
    if session is not None:
        await session.close()
        session = None

def get_session() -> aiohttp.ClientSession:
    if not session: raise Exception('HTTP session isnt initialized')
    return session