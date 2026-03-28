from pydantic import BaseModel, Field
from typing import Optional

class BuyDto(BaseModel):
    type: str = 'Buy'
    to_tariff_uname: str = Field(..., min_length=1)
    months: Optional[int] = Field(None)
    for_pay: bool = Field(default=False)

class UpgradeDto(BaseModel):
    type: str = 'Upgrade'
    user_period_id: Optional[int] = Field(None)
    from_tariff_uname: str = Field(..., min_length=1)
    to_tariff_uname: str = Field(..., min_length=1)
    for_pay: bool = Field(default=False)


# ПУТЬ ЗАПРОСА НА ПОКУПКУ И АПГРЕЙД:
# FastAPI сервер (DTO) -> 
# -> DB service:
#      1. Готовит данные для платежа (order, user, сумма)
#      2. Просит создать платёж
#      3. Создаёт запись в payments (вместе с нужными данными)
#      4. Возвращает данные для оплаты