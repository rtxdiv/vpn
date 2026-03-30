from pydantic import BaseModel, Field
from typing import Optional

class UpgradeDto(BaseModel):
    user_period_id: Optional[int] = Field(None)
    from_tariff_uname: str = Field(..., min_length=1)
    to_tariff_uname: str = Field(..., min_length=1)
    for_pay: bool = Field(default=False)