from ..schemas.sensor_schema import CreateSensorInSchema, UpdateSensorInSchema, ListenerConfigInSchema
import json


class SensorListenerController():

    def manage_listener(self, listener_config: ListenerConfigInSchema) -> int:
        # The return type of this function follows the same principe as C
        # 0: Success
        # 1: Error in starting the listener
        # 2: Error in shutingdown the listener
        status = 0
        if listener_config.collect:
            try:
                self.__start_listener()
            except:
                status = 1
        else:
            try:
                self.__shutdown_listener()
            except:
                status = 2

        return status

    def __start_listener(self):
        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)

        data["collect"] = True

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json.dump(data, f)

    def __shutdown_listener(self):
        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)

        data["collect"] = False

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json.dump(data, f)

    def get_listener_state(self) -> bool:
        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)
        return data['collect']


sensor_listener_controller = SensorListenerController()
