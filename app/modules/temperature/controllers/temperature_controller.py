from database.config import db
from ..models.temperature_model import Temperature
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func, desc

class TemperatureController():

    def get_temperatures(self) -> List[Temperature]:
        temperatures = db.query(Temperature).all()
        return temperatures

    def get_daily_min_max_temperatures(self) -> List[Temperature]:
        # TODO: change th is to today
        now = datetime.now() - timedelta(days=2)
        today_start = datetime.combine(now, datetime.min.time())
        today_end = datetime.combine(now, datetime.max.time())
        subquery = (db.query(func.strftime("%H:00", Temperature.created_at).label("hour"), 
                            func.min(Temperature.value).label("min_temp"), 
                            func.max(Temperature.value).label("max_temp"))
                    .filter(Temperature.created_at.between(today_start, today_end))
                    .group_by(func.strftime("%H", Temperature.created_at))
                    .subquery())
        result = (db.query(subquery.c.hour, subquery.c.min_temp, subquery.c.max_temp)
                .order_by(desc(subquery.c.hour))
                .all())
        return result        


temperature_controller = TemperatureController()