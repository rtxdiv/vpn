from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

class Tariffs(Base):
    __tablename__ = 'tariffs'

    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String, nullable=False)
    devices: Mapped[int] = mapped_column(Integer, nullable=False)
    traffic: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Tariffs(id={self.id!r}, uid={self.uid!r}, name={self.name!r})'