from database.config import db
from ..models.humidity_model import Humidity
from typing import List
from datetime import datetime
from sqlalchemy import func


class HumidityController():

    def get_humidities(self) -> List[Humidity]:
        subquery = (db.query(func.strftime("%Y-%m-%d %H:%M", Humidity.created_at).label("created_at"),
                        func.round(func.avg(Humidity.value)).label("value"))
                    .group_by(func.strftime("%Y-%m-%d %H:%M", Humidity.created_at))
                    .subquery())
        humidities = (db.query(subquery.c.created_at, subquery.c.value)
              .all())
        return humidities

    def get_daily_min_max_temperatures(self) -> List[Humidity]:
        now = datetime.now()
        today_start = datetime.combine(now, datetime.min.time())
        today_end = datetime.combine(now, datetime.max.time())
        subquery = (db.query(func.strftime("%H:00", Humidity.created_at).label("hour"), 
                            func.min(Humidity.value).label("min_temp"), 
                            func.max(Humidity.value).label("max_temp"))
                    .filter(Humidity.created_at.between(today_start, today_end))
                    .group_by(func.strftime("%H", Humidity.created_at))
                    .subquery())
        result = (db.query(subquery.c.hour, subquery.c.min_temp, subquery.c.max_temp)
                .order_by(subquery.c.hour)
                .all())
        return result        

    
humidity_controller = HumidityController()