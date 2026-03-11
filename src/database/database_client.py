from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from functools import wraps
from typing import Callable
from root import ROOT_DIR


DB_PATH = ROOT_DIR / 'main.db'
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(url=DB_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

def with_session(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            return await func(session, *args, **kwargs)
    return wrapper