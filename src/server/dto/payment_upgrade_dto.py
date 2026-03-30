from pydantic import BaseModel, Field
from typing import Optional

class UpgradeDto(BaseModel):
    user_period_id: int = Field(...)
    from_tariff_uname: str = Field(..., min_length=1)
    to_tariff_uname: str = Field(..., min_length=1)