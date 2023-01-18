from config import Base
from sqlalchemy import MetaData, Table, Column, Float, Integer, DateTime, create_engine, String
from datetime import datetime


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


if __name__ == '__main__':
    main()

