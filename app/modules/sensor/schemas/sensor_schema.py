from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime


class BaseSensorSchema(BaseModel):
    temperature: float
    humidity: float
    purpose: str


class CreateSensorInSchema(BaseSensorSchema):
    pass


class UpdateSensorInSchema(CreateSensorInSchema):
    created_at: datetime
    updated_at: datetime


class SensorConfigOutSchema(BaseSensorSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config():
        orm_mode = True


class OutSchema(BaseModel):
    state: Literal['Success', 'Error']
    msgs: List[str] = None


class SensorOutSchema(OutSchema):
    pass


class ListenerConfigOutSchema(OutSchema):
    pass


class ListenerConfigInSchema(BaseModel):
    collect: bool
