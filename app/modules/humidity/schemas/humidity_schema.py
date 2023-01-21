from pydantic import BaseModel
from datetime import datetime

class HumidityOutSchema(BaseModel):
    value: float
    created_at: datetime

    class Config():
        orm_mode = True

class DailyHumidityOutSchema(BaseModel):
    hour: str
    min_temp: float
    max_temp: float

    class Config():
        orm_mode = True