from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database.config import Base
from datetime import datetime


class Temperature(Base):
    __tablename__ = "Temperatures"

    id = Column(Integer, primary_key=True, index=True)    
    value = Column(Float)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    