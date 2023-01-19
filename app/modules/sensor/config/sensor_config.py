import sys
sys.path.insert(0, '.')

import random
from modules.humidity.models.humidity_model import Humidity
from modules.temperature.models.temperature_model import Temperature
from database.config import db
import paho.mqtt.client as mqtt
import json
import os
from settings.settings import NOTIFICATION_EMAIL_TEMPLATE
import subprocess
from time import sleep



# MQTT callback function for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected to Hive MQTT broker with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("topic_sensor_humidity")
    client.subscribe("topic_sensor_temperature")




# MQTT callback function for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    f = open('modules/sensor/config/listener_config.json')
    data = json.load(f)
    f.close()

    payload = str(msg.payload.decode()).split('_')
    value = float(payload[0])
    nature = payload[1]

    # Simulation of getting diff values
    variation = random.randint(0, 20)
    value += variation

    print(nature)
    print(value)

    if nature == 'temp' and value >= data["temp"] and not data["temp_email_sent"]:
        subprocess.Popen(f'python3 utilities/notification_sender.py temperature {data["receiver"]} &', shell=True)

        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)  

        data["temp_email_sent"] = True

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json.dump(data, f)

    if nature == 'hum' and value >= data["hum"] and not data["hum_email_sent"]:
        subprocess.Popen(f'python3 utilities/notification_sender.py humidity {data["receiver"]} &', shell=True)

        with open('modules/sensor/config/listener_config.json', "r") as f:
            data = json.load(f)  

        data["hum_email_sent"] = True

        with open('modules/sensor/config/listener_config.json', "w") as f:
            json.dump(data, f)

    if data["collect"]:
        try:
            if nature == 'temp':
                new_temperature = Temperature(value=value)
                db.add(new_temperature)
            else:
                new_humidity = Humidity(value=value)
                db.add(new_humidity)
            db.commit()
        except Exception as e:
            print(e)


def set_my_pid():
    # write the pid to the cofnfig file
    with open('modules/sensor/config/listener_config.json', "r") as f:
        data = json.load(f)  

    data["pid"] = os.getpid()
    print("pid")
    print(os.getpid())

    with open('modules/sensor/config/listener_config.json', "w") as f:
        json.dump(data, f)


def listen():  
    # Create an MQTT client and connect to Hive
    client = mqtt.Client(client_id="clientId-BbEa9FpHyh")
    client.on_connect = on_connect
    client.on_message = on_message

    # Set the username and password for the MQTT broker if required
    # client.username_pw_set("username", "password")

    # Connect to the Hive MQTT broker
    client.connect("broker.mqttdashboard.com", 1883, 60)

    # Loop to process incoming messages
    client.loop_forever()


if __name__ == '__main__':
    set_my_pid()
    listen()
