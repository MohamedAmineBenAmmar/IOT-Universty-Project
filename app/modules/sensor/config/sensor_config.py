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
from modules.email.controllers.email_controller import email_sender



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
        email_sender.send_email_async('Temperature Alert', data['receiver'],
        {'title': 'Temperature ', 'name': 'Alert we detected a raise in the temperature !!!'}, NOTIFICATION_EMAIL_TEMPLATE)

        # Update the email send flag
        # ...

    if nature == 'hum' and value >= data["hum"] and not data["hum_email_sent"]:
        email_sender.send_email_async('Hello World', data['receiver'],
        {'title': 'Humidity ', 'name': 'Alert we detected a raise in the humidity !!!'}, NOTIFICATION_EMAIL_TEMPLATE)

        # Update the email send flag
        # ...

    if data["collect"]:
        try:
            if nature == 'temp':
                new_temperature = Temperature(value=payload)
                db.add(new_temperature)
            else:
                new_humidity = Humidity(value=payload)
                db.add(new_humidity)
            db.commit()
        except Exception:
            print("error occured")


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
