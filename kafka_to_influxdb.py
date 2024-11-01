# kafka_to_influxdb.py
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from confluent_kafka import Consumer
from dotenv import load_dotenv
import json
import time
import os

load_dotenv()

KAFKA_BROKER = os.environ.get('KAFKA_BROKER')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
INFLUXDB_URL = os.environ.get('INFLUXDB_URL')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.environ.get('INFLUXDB_BUCKET')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN')

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'iot_group',
    'auto.offset.reset': 'latest'
}

# Initialize InfluxDB Client
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

# Kafka Consumer to Process and Store Data in InfluxDB
consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Process data
        data = json.loads(msg.value().decode())
        print(f"Received from Kafka: {data}")
        
        # Store in InfluxDB
        point = Point("sensor_data") \
            .field("temperature", data["temperature"]) 
        
        write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        print("Data written to InfluxDB:", data)
        time.sleep(3)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    consumer.close()
    influxdb_client.close()
