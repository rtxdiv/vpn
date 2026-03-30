import json

from src.database.database_client import database_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.database.models import *
from datetime import datetime, timedelta
from src.utils.exceptions import *
from src.utils.hashids_client import hashids
from src.server.dto.payment_buy_dto import BuyDto


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
    end_date = last_period.starts + timedelta(days=last_period.days)
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
    return (tariff, periods, total, period.months)

@database_session
async def create_payment(session: AsyncSession, user_id: int, type: str, amount: float, currency: str, data: BuyDto):
    payment = Payments(
        user_id=user_id,
        type=type,
        amount=amount,
        currency=currency,
        data=data
    )
    session.add(payment)
    await session.flush()
    payment.payment_id = hashids.encode(payment.id)
    await session.commit()


# @database_session
# async def get_sub_url(session: AsyncSession) -> str:
#     setting = await session.scalar(select(Settings).where(Settings.key == 'sub_url'))
#     if not setting: raise Exception
#     return setting.value