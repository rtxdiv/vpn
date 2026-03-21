from pydantic import BaseModel, Field
from typing import Optional

class BuyDto(BaseModel):
    uname: str = Field(..., description='uname обязательное поле')
    months: Optional[int] = Field(None)
    for_pay: bool = Field(default=False)