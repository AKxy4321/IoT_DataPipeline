# iot_device_mqtt.py
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import json
import time
import random
import os

load_dotenv()

MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
USERNAME = os.environ.get('USER_NAME')
PASSWORD = os.environ.get('PASS_WORD')

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT, 60)

def publish_sensor_data():
    while True:
        data = {
            "temperature": round(random.uniform(20.0, 30.0), 2)
        }
        message = json.dumps(data)
        client.publish(MQTT_TOPIC, message)
        print(f"IoT Device sent: {message}")
        time.sleep(3)

if __name__ == "__main__":
    publish_sensor_data()
