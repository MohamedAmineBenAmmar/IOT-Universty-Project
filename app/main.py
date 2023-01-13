from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import paho.mqtt.client as mqtt
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    message: str

# Configuring CORSMiddleware
# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))


@app.post("/send")
def send_message(item: Item):
    # mqttClient = mqtt.Client(client_id="clientId-TFjlYVNkwi")
    mqttClient = mqtt.Client(
        client_id="clientId-TFjlYVNkwi",
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport="tcp"

    )
    # mqttClient.username_pw_set("username", "password")
    mqttClient.connect("broker.mqttdashboard.com", 1883)
    mqttClient.publish("topic_sensor_temperature", item.message)

    mqttClient.on_message = on_message
    mqttClient.disconnect()

    print("nada is the best ")
    return {"message": "message sent lol"}


@app.get("/subscribe")
def subscribe():
    # mqttClient = mqtt.Client(client_id="clientId-TFjlYVNkwi")
    mqttClient = mqtt.Client(
        client_id="clientId-TFjlYVNkwi",
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport="tcp"
    )
    mqttClient.connect("broker.mqttdashboard.com", 1883)
    mqttClient.subscribe("topic_sensor_temperature")
    while True:
        mqttClient.loop()
        messages = mqttClient.check_msg()
        for message in messages:
            print("Received message '" + str(message.payload) +
                  "' on topic '" + message.topic + "' with QoS " + str(message.qos))

    return {"message": "subscribed xxxx"}
