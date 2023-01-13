from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime


class Humidity(Base):
    __tablename__ = "Humidities"

    id = Column(Integer, primary_key=True, index=True)    
    value = Column(Float)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    