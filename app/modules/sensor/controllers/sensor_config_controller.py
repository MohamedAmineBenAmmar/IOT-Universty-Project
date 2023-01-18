from ..schemas.sensor_schema import *
from ..models.sensor_config_model import Configuration
from sqlalchemy.orm import Session
from database.config import db
from fastapi import status, HTTPException


class SensorConfigController():

    def get_sensor_config_by_id(self, id: int) -> Configuration | None:
        sensor_config = db.query(Configuration).filter(Configuration.id == id).first()

        if not sensor_config:
            return None

        return sensor_config

        
    def create_new_sensor_config(self, new_sensor_config: CreateSensorInSchema) -> Configuration:
        configs = db.query(Configuration).all()
        if len(configs) > 0:
            raise HTTPException(status_code=400, detail=f"Sensor already configured")
        
        dict_new_sensor_config = new_sensor_config.dict()
        sensor_config = Configuration(**dict_new_sensor_config)
        db.add(sensor_config)
        db.commit()
        db.refresh(sensor_config)

        # Start the process that will listen for the simulation + write the values to the listener file json file
        #...

        return sensor_config



    def update_sensor_config(self, id: int, updated_sensor_config: UpdateSensorInSchema) -> Configuration:
        sensor_config = db.query(Configuration).filter(Configuration.id == id)
        if not sensor_config.first():
            raise HTTPException(status_code=404, detail=f"Sensor configuration with the id = {id} is not found")

        sensor_config.update(**updated_sensor_config.dict())
        db.commit()

        # Update the listener file with the new values to listen for
        # ...
        
        return sensor_config.first()

        
    def delete_sensor_config(self, id: int) -> None:
        sensor_config = db.query(Configuration).filter(Configuration.id == id)

        if not sensor_config.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor configuration with id = {id} is not found")
        
        sensor_config.delete(synchronize_session=False)
        db.commit()

        # Kill the process that listening to the simulation + reset the file ot the init values


  
    def get_sensor_config(self, id: int) -> Configuration:
        sensor_config = db.query(Configuration).filter(Configuration.id == id).first()
        if not sensor_config:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor configuration with id = {id} is not found")

        return sensor_config





sensor_config_controller = SensorConfigController()