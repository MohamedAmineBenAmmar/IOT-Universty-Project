from database.config import db
from ..models.temperature_model import Temperature
from typing import List

class TemperatureController():

    def get_temperatures(self) -> List[Temperature]:
        temperatures = db.query(Temperature).all()
        return temperatures

    
temperature_controller = TemperatureController()