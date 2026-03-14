from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f'{__class__.__name__}: {__class__.__dict__}'


class Tariffs(Base):
    __tablename__ = 'tariffs'

    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String, nullable=False)
    devices: Mapped[int] = mapped_column(Integer, nullable=False)
    traffic: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    

class Periods(Base):
    __tablename__ = 'periods'

    days: Mapped[int] = mapped_column(Integer, nullable=False)
    months: Mapped[int] = mapped_column(Integer, nullable=False)
    discount: Mapped[float] = mapped_column(Float, nullable=False)


class Settings(Base):
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)