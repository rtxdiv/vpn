from src.database.database_client import database_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import Tariffs, Settings


@database_session
async def get_all_tafiffs(session: AsyncSession):
    tariffs = await session.execute(select(Tariffs))
    return tariffs.scalars().all()

@database_session
async def get_all_settings(session: AsyncSession):
    settings = await session.execute(select(Settings))
    settings_list = settings.scalars().all()
    return { setting.key: setting.value for setting in settings_list }