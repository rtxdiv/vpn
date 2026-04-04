from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from .database_server import database_session
from .models import *
from src.utils.exceptions import *
from src.utils.hashids_client import hashids
from src.utils.payment_info import PaymentInfo
from src.server.dto.payment_buy_dto import BuyDto
from datetime import timedelta, datetime


@database_session
async def get_all_tafiffs(session: AsyncSession) -> list[Tariffs]:
    return (await session.scalars(select(Tariffs).where(Tariffs.enabled == True))).all()

@database_session
async def get_all_settings(session: AsyncSession) -> list[Settings]:
    settings = (await session.scalars(select(Settings))).all()
    return { setting.key: setting.value for setting in settings }

@database_session
async def get_all_allowed_periods(session: AsyncSession) -> list[PaymentPeriods]:
    return (await session.scalars(select(PaymentPeriods))).all()

@database_session
async def get_user_periods_end(session: AsyncSession, user_id: str) -> str:
    last_period = await session.scalar(
        select(UserPeriods)
        .where(UserPeriods.user_id == user_id)
    )
    if not last_period: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_date = last_period.starts + timedelta(days=last_period.days)
    return end_date


@database_session
async def get_all_payments(session: AsyncSession, user_id: str) -> list[Payments]:
    return (await session.scalars(
        select(Payments)
        .where(Payments.user_id == user_id)
        .order_by(desc(Payments.created))
    )).all()

@database_session
async def get_user_payment(session: AsyncSession, user_id: str, payment_id: str) -> Payments:
    payment = (await session.scalar(
        select(Payments)
        .where(Payments.user_id == user_id, Payments.payment_id == payment_id)
    ))
    if not payment: raise ForeseenException('Платёж не найден')
    return payment

@database_session
async def get_payment_settings(session: AsyncSession) -> dict:
    settings = (await session.scalars(select(Settings).where(
        Settings.key.in_([
            'payment_details', 
            'payment_comment', 
            'payment_id_prefix', 
            'payment_message'
        ])
    ))).all()
    return {setting.key: setting.value for setting in settings}

@database_session
async def create_payment(session: AsyncSession, user_id: str, type: str, title: str, amount: float, data: dict, currency: str | None = None) -> str:
    payment = Payments(
        user_id=user_id,
        type=type,
        title=title,
        amount=amount,
        currency=currency,
        data=data
    )
    session.add(payment)
    await session.flush()
    payment.payment_id = hashids.encode(payment.id)
    payment.updated = None
    await session.commit()
    return payment.payment_id


# payment types
@database_session
async def prepare_buy(session: AsyncSession, user_id: str, uname: str, months: int, pay: bool = False) -> PaymentInfo | str:
    tariff = await session.scalar(select(Tariffs).where(Tariffs.uname == uname, Tariffs.enabled == True))
    if not tariff: raise ForeseenException('Тариф не найден')
    if not months:
        period = await session.scalar(
            select(PaymentPeriods)
            .order_by(PaymentPeriods.months)
            .limit(1)
        )
    else:
        period = await session.scalar(
            select(PaymentPeriods)
            .where(PaymentPeriods.months == months)
        )
    if not period:
        raise ForeseenException('Нет периодов для покупки' if not months else 'Такой период для оплаты недоступен')

    total = round(tariff.price * period.months * (1 - period.discount))

    if pay:
        title = f'{tariff.name}, {period.months} мес.'

        payment_data = BuyDto(
            to_tariff=tariff.uname,
            months=period.months
        )
        payment_id = await create_payment(
            user_id=user_id,
            type='Buy',
            title=title,
            amount=total,
            data=payment_data.model_dump()
        )
        return payment_id

    return PaymentInfo(
        title=tariff.name,
        total=total
    )
    

# @database_session
# async def get_sub_url(session: AsyncSession) -> str:
#     setting = await session.scalar(select(Settings).where(Settings.key == 'sub_url'))
#     if not setting: raise Exception
#     return setting.value
