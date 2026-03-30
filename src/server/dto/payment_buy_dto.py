from pydantic import BaseModel, Field
from typing import Optional

class BuyDto(BaseModel):
    to_tariff_uname: str = Field(..., min_length=1)
    months: int = Field(...)


# ПУТЬ ЗАПРОСА НА ПОКУПКУ И АПГРЕЙД:
# FastAPI сервер (DTO) -> 
# -> DB service:
#      1. Готовит данные для платежа (order, user, сумма)
#      2. Просит создать платёж
#      3. Создаёт запись в payments (вместе с нужными данными)
#      4. Возвращает данные для оплаты