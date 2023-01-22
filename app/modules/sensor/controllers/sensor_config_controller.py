from ..schemas.sensor_schema import *
from ..models.sensor_config_model import Configuration
from sqlalchemy.orm import Session
from database.config import db
from fastapi import status, HTTPException
import subprocess
import os
import json
from ..config.sensor_config import listen
from multiprocessing import Process

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

        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)  

        data["temp"] = new_sensor_config.temperature
        data["hum"] = new_sensor_config.humidity

        print("data ")
        print(data)
        with open('modules/sensor/config/listener_config.json', "w") as f:
            json_string = json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            f.write(json_string)

        subprocess.Popen(f"python3 modules/sensor/config/sensor_config.py &", shell=True)

        return sensor_config



    def update_sensor_config(self, id: int, updated_sensor_config: UpdateSensorInSchema) -> Configuration:
        sensor_config = db.query(Configuration).filter(Configuration.id == id)
        if not sensor_config.first():
            raise HTTPException(status_code=404, detail=f"Sensor configuration with the id = {id} is not found")

        #print(updated_sensor_config.dict())
        sensor_config: Configuration = sensor_config.first()
        sensor_config.temperature = updated_sensor_config.temperature
        sensor_config.humidity = updated_sensor_config.humidity
        sensor_config.purpose = updated_sensor_config.purpose
        
        db.commit()

        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)  

        data["temp"] = updated_sensor_config.temperature
        data["hum"] = updated_sensor_config.humidity

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json_string = json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            f.write(json_string)
        
        return sensor_config

        
    def delete_sensor_config(self, id: int) -> None:
        sensor_config = db.query(Configuration).filter(Configuration.id == id)

        if not sensor_config.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor configuration with id = {id} is not found")
        
        sensor_config.delete(synchronize_session=False)
        db.commit()

        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)  

    
        result = os.system(f'kill -9 {data["pid"]}')
        if result != 0:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'No process with PID = {data["pid"]}')

        data["temp"] = 9999
        data["hum"] = 9999
        data["collect"] = False
        data["temp_email_sent"] = False
        data["hum_email_sent"] = False
        data["pid"] = -1
        data["receiver"] = None

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json.dump(data, f)


    def get_sensor_config(self, id: int) -> Configuration:
        sensor_config = db.query(Configuration).filter(Configuration.id == id).first()
        if not sensor_config:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor configuration with id = {id} is not found")

        return sensor_config

    def set_receiver_email(self, receiver: ReceiverInSchema) -> int:        
        status = 0
        try:
            with open('modules/sensor/config/listener_config.json', "r") as f:
                data = json.load(f)  

            data["receiver"] = receiver.email

            with open('modules/sensor/config/listener_config.json', "w") as f:
                json.dump(data, f)
        except Exception as e:
            status = 1

        return status

    def get_receiver_email(self) -> str:               
        try:
            with open('modules/sensor/config/listener_config.json', "r") as f:
                data = json.load(f)  

            return data["receiver"]

        except Exception as e:
            print(e)

    def reset_email_notifications_flags(self, email_notifications_flags: EmailNotificationsFlagsInSchema) -> int:
        try:
            with open('modules/sensor/config/listener_config.json', "r") as f:
                data = json.load(f)  

            if email_notifications_flags.temp_email_sent:
                data["temp_email_sent"] = False

            if email_notifications_flags.hum_email_sent:
                data["hum_email_sent"] = False

            with open('modules/sensor/config/listener_config.json', "w") as f:
                json.dump(data, f)

            return 0
        except Exception as exception:
            return 1
        



        





sensor_config_controller = SensorConfigController()