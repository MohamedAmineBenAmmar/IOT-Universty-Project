from config import Base
from sqlalchemy import MetaData, Table, Column, Float, Integer, DateTime, create_engine, String
from datetime import datetime

# import Temperature, Humidity
class Temperature(Base):
    __tablename__ = "Temperatures"

    id = Column(Integer, primary_key=True, index=True)    
    value = Column(Float)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
class Humidity(Base):
    __tablename__ = "Humidities"

    id = Column(Integer, primary_key=True, index=True)    
    value = Column(Float)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

def main():
    metadata = MetaData()
    
    # Function to init the db tables
    temperatures_table = Table('Temperatures', metadata,
        Column('id', Integer(), primary_key=True),
        Column('value', Float()),    
        Column('created_at', DateTime(), default=datetime.now),
        Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now)
    )

    humidities_table = Table('Humidities', metadata,
        Column('id', Integer(), primary_key=True),
        Column('value', Float()),    
        Column('created_at', DateTime(), default=datetime.now),
        Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now)
    )

    sensor_config_table = Table('Configurations', metadata,
        Column('id', Integer(), primary_key=True),
        Column('temperature', Float()), 
        Column('humidity', Float()),
        Column('purpose', String()),   
        Column('created_at', DateTime(), default=datetime.now),
        Column('updated_at', DateTime(), default=datetime.now, onupdate=datetime.now)
    )

    # Connect to the database
    engine = create_engine('sqlite:///app.db', echo=True)
   
    metadata.create_all(engine)

    def add_fake_data():
        from sqlalchemy.orm import sessionmaker
        from random import randint, uniform
        from datetime import datetime, timedelta

        # Add fake data to the tables
        Session = sessionmaker(bind=engine)
        session = Session()
        for i in range(30):
            temp = Temperature(value=randint(40, 48), created_at=datetime.now() - timedelta(hours=randint(0,10), minutes=randint(30, 60)), updated_at=datetime.now())
            humi = Humidity(value=randint(25, 32), created_at=datetime.now() - timedelta(hours=randint(0,10), minutes=randint(30, 60)), updated_at=datetime.now())
            session.add(temp)
            session.add(humi)
        session.commit()
        session.close()

    add_fake_data()


if __name__ == '__main__':
    main()

