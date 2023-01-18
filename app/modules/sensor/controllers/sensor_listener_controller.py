from ..schemas.sensor_schema import CreateSensorInSchema, UpdateSensorInSchema, ListenerConfigInSchema
import json

class SensorListenerController():

    def manage_listener(self, listener_config: ListenerConfigInSchema):
        if listener_config.collect:
            self.__start_listener()
        else:
            self.__shutdown_listener()

    def __start_listener(self):
        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)
       
        data["collect"] = True

        with open('modules/sensor/config/listener_config.json', "w") as f:
            f.write(data)

    
    def __shutdown_listener(self):
        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)
       
        data["collect"] = False

        with open('modules/sensor/config/listener_config.json', "w") as f:
            f.write(data)




sensor_listener_controller = SensorListenerController()