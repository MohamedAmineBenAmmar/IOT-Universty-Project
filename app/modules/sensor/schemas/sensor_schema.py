from pydantic import BaseModel, EmailStr
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

class ListenerStateOutSchema(BaseModel):
    state: bool


class ListenerConfigInSchema(BaseModel):
    collect: bool


class ReceiverInSchema(BaseModel):
    email: EmailStr

class EmailNotificationsFlagsInSchema(BaseModel):
    hum_email_sent: bool
    temp_email_sent: bool
