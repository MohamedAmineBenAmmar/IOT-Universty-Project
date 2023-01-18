from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime


class Configuration(Base):
    __tablename__ = "Configurations"

    id = Column(Integer, primary_key=True, index=True)    
    temperature = Column(Float)
    humidity = Column(Float)
    purpose = Column(String)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    