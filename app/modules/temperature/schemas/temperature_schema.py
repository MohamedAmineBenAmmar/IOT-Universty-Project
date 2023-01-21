from pydantic import BaseModel
from datetime import datetime

class TemperatureOutSchema(BaseModel):
    value: float
    created_at: datetime

    class Config():
        orm_mode = True
        
class DailyTemperatureOutSchema(BaseModel):
    hour: str
    min_temp: float
    max_temp: float
    class Config():
        orm_mode = True