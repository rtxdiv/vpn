from typing import Optional
import datetime

from sqlalchemy import Date, DateTime, Float, ForeignKeyConstraint, Index, Integer, JSON, String, Text, text
from sqlalchemy.dialects.mysql import FLOAT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class PaymentPeriods(Base):
    __tablename__ = 'payment_periods'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    days: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    months: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    discount: Mapped[float] = mapped_column(FLOAT(unsigned=True), nullable=False, server_default=text("'0'"))


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        Index('payment_id', 'payment_id', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    type: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    title: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(VARCHAR(64, charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False, server_default=text("'₽'"))
    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('(now())'))
    success: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    payment_id: Mapped[Optional[str]] = mapped_column(VARCHAR(16, charset='utf8mb4', collation='utf8mb4_unicode_ci'))
    updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    purchases: Mapped[list['Purchases']] = relationship('Purchases', back_populates='payment')


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))


class Tariffs(Base):
    __tablename__ = 'tariffs'
    __table_args__ = (
        Index('uname', 'uname', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uname: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    name: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    country: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    devices: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    traffic: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    price: Mapped[float] = mapped_column(FLOAT(unsigned=True), nullable=False)
    enabled: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"))

    user_periods: Mapped[list['UserPeriods']] = relationship('UserPeriods', back_populates='tariffs')
    purchases_from_tariff: Mapped[list['Purchases']] = relationship('Purchases', foreign_keys='[Purchases.from_tariff]', back_populates='tariffs')
    purchases_to_tariff: Mapped[list['Purchases']] = relationship('Purchases', foreign_keys='[Purchases.to_tariff]', back_populates='tariffs_')


class UserPeriods(Base):
    __tablename__ = 'user_periods'
    __table_args__ = (
        ForeignKeyConstraint(['tariff_uname'], ['tariffs.uname'], onupdate='CASCADE', name='tariff_uname_fk'),
        Index('tariff_uname_fk', 'tariff_uname')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    tariff_uname: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    days: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    used: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"))
    starts: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(now())'))

    tariffs: Mapped['Tariffs'] = relationship('Tariffs', back_populates='user_periods')
    purchases: Mapped[list['Purchases']] = relationship('Purchases', back_populates='user_period')


class Purchases(Base):
    __tablename__ = 'purchases'
    __table_args__ = (
        ForeignKeyConstraint(['from_tariff'], ['tariffs.uname'], onupdate='CASCADE', name='from_tariff_fk'),
        ForeignKeyConstraint(['payment_id'], ['payments.payment_id'], onupdate='CASCADE', name='payment_id_fk'),
        ForeignKeyConstraint(['to_tariff'], ['tariffs.uname'], onupdate='CASCADE', name='to_tariff_fk'),
        ForeignKeyConstraint(['user_period_id'], ['user_periods.id'], onupdate='CASCADE', name='user_period_fk'),
        Index('from_tariff_uname_fk', 'from_tariff'),
        Index('payment_id_fk', 'payment_id'),
        Index('to_tariff_uname_fk', 'to_tariff'),
        Index('user_period_fk', 'user_period_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    payment_id: Mapped[str] = mapped_column(VARCHAR(16, charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    to_tariff: Mapped[str] = mapped_column(VARCHAR(64, charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    user_period_id: Mapped[Optional[int]] = mapped_column(Integer)
    from_tariff: Mapped[Optional[str]] = mapped_column(VARCHAR(64, charset='utf8mb4', collation='utf8mb4_unicode_ci'))

    tariffs: Mapped[Optional['Tariffs']] = relationship('Tariffs', foreign_keys=[from_tariff], back_populates='purchases_from_tariff')
    payment: Mapped['Payments'] = relationship('Payments', back_populates='purchases')
    tariffs_: Mapped['Tariffs'] = relationship('Tariffs', foreign_keys=[to_tariff], back_populates='purchases_to_tariff')
    user_period: Mapped[Optional['UserPeriods']] = relationship('UserPeriods', back_populates='purchases')
