from confluent_kafka import Producer
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import json
import time
import os

load_dotenv()

KAFKA_BROKER = os.environ.get('KAFKA_BROKER')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
USERNAME = os.environ.get('USER_NAME')
PASSWORD = os.environ.get('PASS_WORD')

# Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})
print(producer)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f"Received from MQTT: {data}")
    
    # Forward message to Kafka
    try:
        producer.produce(KAFKA_TOPIC, data)
        producer.flush() 
        print(f"Sent to Kafka: {data}")
    except Exception as e:
        print(f"Failed to send to Kafka: {e}")

    time.sleep(3)

# MQTT Client Setup with specified protocol version
mqtt_client = mqtt.Client()  
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
