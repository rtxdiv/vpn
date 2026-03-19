from pydantic import BaseModel, Field
from typing import Optional

class BuyDto(BaseModel):
    uname: str = Field(..., description='uname обязательное поле')
    months: Optional[int] = None 