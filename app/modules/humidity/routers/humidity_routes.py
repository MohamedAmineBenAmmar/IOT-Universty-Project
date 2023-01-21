from fastapi import APIRouter
from ..schemas.humidity_schema import HumidityOutSchema, DailyHumidityOutSchema
from typing import List
from ..controllers.humidity_controller import humidity_controller

router = APIRouter(
    prefix='/humidity',
    tags=['Humidity']
)

@router.get('/all', status_code=200, response_model=List[HumidityOutSchema])
async def get_humidities():
    return humidity_controller.get_humidities()

@router.get('/get-daily-min-max-humidities', status_code=200, response_model=List[DailyHumidityOutSchema])
async def get_daily_min_max_temperatures():
    return humidity_controller.get_daily_min_max_temperatures()
