from fastapi import APIRouter
from ..schemas.humidity_schema import HumidityOutSchema
from typing import List
from ..controllers.humidity_controller import humidity_controller

router = APIRouter(
    prefix='/humidity',
    tags=['Humidity']
)

@router.get('/all', status_code=200, response_model=List[HumidityOutSchema])
async def get_humidities():
    return humidity_controller.get_humidities()
