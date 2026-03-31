from pydantic import BaseModel, Field

class UpgradeDto(BaseModel):
    user_period_id: int = Field(...)
    from_tariff: str = Field(..., min_length=1)
    to_tariff: str = Field(..., min_length=1)

    class Config:
        extra = 'ignore'