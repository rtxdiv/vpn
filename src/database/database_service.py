from src.database.database_client import database_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.database.models import *
from datetime import datetime, timedelta
from src.utils.exceptions import *


months = ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]


@database_session
async def get_all_tafiffs(session: AsyncSession) -> list[Tariffs]:
    return (await session.scalars(select(Tariffs))).all()

@database_session
async def get_all_settings(session: AsyncSession) -> list[Settings]:
    settings = (await session.scalars(select(Settings))).all()
    return { setting.key: setting.value for setting in settings }

@database_session
async def get_user_periods_end(session: AsyncSession, id: any) -> str:
    last_period = await session.scalar(
        select(UserPeriods)
        .where(UserPeriods.user_id == str(id))
        .order_by(desc(UserPeriods.starts))
        .limit(1)
    )
    if not last_period: return 'сегодня'
    date = datetime.strptime(last_period.starts, '%Y-%m-%d')
    end_date = date + timedelta(days=last_period.days)
    return f'{end_date.day} {months[end_date.month]} {end_date.year}'

@database_session
async def get_tariff_and_price(session: AsyncSession, uname: str, months: Optional[int] = None) -> Optional[float]:
    tariff = await session.scalar(select(Tariffs).where(Tariffs.uname == uname))
    if not tariff: raise ForeseenException
    periods = (await session.scalars(
        select(AllowedPeriods)
        .order_by(AllowedPeriods.months)
    )).all()
    
    period = None
    if not months:
        period = periods[0]
    else:
        period = [item for item in periods if item.months == months][0]
    if not period: raise ForeseenException
    total = round(tariff.price * period.months * (1 - period.discount))
    return { tariff: tariff, periods: periods, total: total, months: period.months }
    