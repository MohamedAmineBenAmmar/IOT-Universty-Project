from database.config import db
from ..models.humidity_model import Humidity
from typing import List
from datetime import datetime, timedelta
from sqlalchemy import func, desc


class HumidityController():

    def get_humidities(self) -> List[Humidity]:
        humidities = db.query(Humidity).all()
        return humidities

    def get_daily_min_max_temperatures(self) -> List[Humidity]:
        # TODO: change this to today
        now = datetime.now() - timedelta(days=2)
        today_start = datetime.combine(now, datetime.min.time())
        today_end = datetime.combine(now, datetime.max.time())
        subquery = (db.query(func.strftime("%H:00", Humidity.created_at).label("hour"), 
                            func.min(Humidity.value).label("min_temp"), 
                            func.max(Humidity.value).label("max_temp"))
                    .filter(Humidity.created_at.between(today_start, today_end))
                    .group_by(func.strftime("%H", Humidity.created_at))
                    .subquery())
        result = (db.query(subquery.c.hour, subquery.c.min_temp, subquery.c.max_temp)
                .order_by(desc(subquery.c.hour))
                .all())
        return result        

    
humidity_controller = HumidityController()