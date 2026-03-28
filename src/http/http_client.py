import aiohttp


session: aiohttp.ClientSession | None = None

async def init_http_session():
    global session
    if session is None:
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60),
        )

async def close_http_session():
    global session
    if session is not None:
        await session.close()
        session = None

def get_session() -> aiohttp.ClientSession:
    if not session: raise Exception('HTTP session isnt initialized')
    return session