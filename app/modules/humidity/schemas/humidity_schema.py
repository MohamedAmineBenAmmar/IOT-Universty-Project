from pydantic import BaseModel
from datetime import datetime

class HumidityOutSchema(BaseModel):
    id: int
    value: float
    created_at: datetime
    updated_at: datetime

    class Config():
        orm_mode = True

class DailyHumidityOutSchema(BaseModel):
    hour: str
    min_temp: float
    max_temp: float

    class Config():
        orm_mode = True