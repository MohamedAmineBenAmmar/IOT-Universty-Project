from database.config import db
from ..models.humidity_model import Humidity
from typing import List

class HumidityController():

    def get_humidities(self) -> List[Humidity]:
        humidities = db.query(Humidity).all()
        return humidities

    
humidity_controller = HumidityController()