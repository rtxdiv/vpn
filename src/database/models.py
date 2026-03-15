from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f'{__class__.__name__}: {__class__.__dict__}'


class Tariffs(Base):
    __tablename__ = 'tariffs'

    tariff_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String, nullable=False)
    devices: Mapped[int] = mapped_column(Integer, nullable=False)
    traffic: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    

class AllowedPeriods(Base):
    __tablename__ = 'allowed_periods'

    days: Mapped[int] = mapped_column(Integer, nullable=False)
    months: Mapped[int] = mapped_column(Integer, nullable=False)
    discount: Mapped[float] = mapped_column(Float, nullable=False)


class Settings(Base):
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    value: Mapped[str] = mapped_column(String)


class UserPeriods(Base):
    __tablename__ = 'user_periods'

    user_id: Mapped[str] = mapped_column(String, nullable=False)
    tariff_id: Mapped[str] = mapped_column(String, ForeignKey('tariffs.tariff_id', name='fk_tariff'), nullable=False)
    days: Mapped[int] = mapped_column(Integer, nullable=False)
    used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    tariff: Mapped["Tariffs"] = relationship(viewonly=True)


class Payments(Base):
    __tablename__ = 'payments'

    payment_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default='waiting')
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    tariff_id: Mapped[str] = mapped_column(String, ForeignKey('tariffs.tariff_id', name='tariff_fk'), nullable=False)
    period_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user_periods.id', name='period_fk'), nullable=True)

    tariff: Mapped["Tariffs"] = relationship(viewonly=True)
    period: Mapped["UserPeriods"] = relationship(viewonly=True)