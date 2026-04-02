from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from functools import wraps
import os

HOST = os.environ['MYSQL_HOST']
USER = os.environ['MYSQL_USER']
PASSWORD = os.environ['MYSQL_PASSWORD']
DATABASE = os.environ['MYSQL_DATABASE']
DB_URL = f'mysql+aiomysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

engine = create_async_engine(
    url=DB_URL,
    pool_pre_ping=True,
    pool_recycle=28000,
    pool_size=5,
    max_overflow=5
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    connect_args={
        'init_command': "SET time_zone = '+00:00'"
    }
)

def database_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with AsyncSessionLocal() as session:
            return await func(session, *args, **kwargs)
    return wrapper