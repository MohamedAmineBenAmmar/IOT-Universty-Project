from fastapi import APIRouter
from ..schemas.temperature_schema import TemperatureOutSchema
from typing import List
from ..controllers.temperature_controller import temperature_controller

router = APIRouter(
    prefix='/temperature',
    tags=['Temperature']
)

@router.get('/all', status_code=200, response_model=List[TemperatureOutSchema])
async def get_temperatures():
    return temperature_controller.get_temperatures()
