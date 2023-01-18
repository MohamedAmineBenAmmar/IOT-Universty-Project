import sys
sys.path.insert(0, '.')

import json
import paho.mqtt.client as mqtt
from database.config import db
from modules.temperature.models.temperature_model import Temperature
from modules.humidity.models.humidity_model import Humidity
import random


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

    variation = random.randint(0, 20)
    value += variation

    print(nature)
    print(value)
    
    if nature == 'temp' and value >= data["temp"]:
        print("send email to the user informing that the temp is too high")
    
    if nature == 'hum' and value >= data["hum"]:
        print("send email to the user informing that the hum is too high")

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
