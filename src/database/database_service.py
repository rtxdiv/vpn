from src.database.database_client import database_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.database.models import *
from datetime import timedelta
from src.utils.exceptions import *
from src.utils.hashids_client import hashids
from src.utils.payment_info import PaymentInfo


@database_session
async def get_all_tafiffs(session: AsyncSession) -> list[Tariffs]:
    return (await session.scalars(select(Tariffs))).all()

@database_session
async def get_all_settings(session: AsyncSession) -> list[Settings]:
    settings = (await session.scalars(select(Settings))).all()
    return { setting.key: setting.value for setting in settings }

@database_session
async def get_all_allowed_periods(session: AsyncSession) -> list[PaymentPeriods]:
    return (await session.scalars(select(PaymentPeriods))).all()

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
    return end_date

@database_session
async def get_payment_info(session: AsyncSession, uname: str, months: int) -> PaymentInfo:
    tariff = await session.scalar(select(Tariffs).where(Tariffs.uname == uname))
    if not tariff: raise ForeseenException('Тариф не найден')
    periods = (await session.scalars(
        select(PaymentPeriods)
        .order_by(PaymentPeriods.months)
    )).all()
    if (len(period)) == 0: raise ForeseenException('Нет периодов для покупки')
    
    if not months:
        period = periods[0]
    else:
        period = [item for item in periods if item.months == months][0]
    total = round(tariff.price * period.months * (1 - period.discount))

    return PaymentInfo(
        title=tariff.name,
        periods=periods,
        total=total
    )

@database_session
async def create_payment(session: AsyncSession, user_id: int, type: str, amount: float, currency: str, data: dict):
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
    payment.updated = None
    await session.commit()


# @database_session
# async def get_sub_url(session: AsyncSession) -> str:
#     setting = await session.scalar(select(Settings).where(Settings.key == 'sub_url'))
#     if not setting: raise Exception
#     return setting.value