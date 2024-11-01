# IoT_DataPipeline

## Workings
1. IoT Device (iot_device_mqtt.py) sends temperature readings every 3s.
2. Mosquitto MQTT Broker receives the readings from the IoT device and sends it to Kafka.
3. From Kafka, we save the readings to influxdb.
4. We then have read_influxdb.py query influxdb every 3s and get the latest readings, it will then determine if its hot or cold and print output to command line.

## Requirements 
- Apache Kafka
- Mosquitto MQTT Broker
- Influxdb

## Setup 
Python = 3.10
```
pip install paho-mqtt confluent-kafka influxdb-client
```
.env = Sample given below
```
MQTT_BROKER=localhost
MQTT_PORT=port
MQTT_TOPIC=topic

// Setup authorisation with USER_NAME and PASS_WORD credentials
KAFKA_BROKER=localhost:port
KAFKA_TOPIC=topic

INFLUXDB_URL=localhost:port
INFLUXDB_TOKEN=token
INFLUXDB_ORG=org
INFLUXDB_BUCKET=bucket

// You will need to setup authorisation with MQTT to allow IoT device to send data to your pc
USER_NAME=abc
PASS_WORD=xyz
```
configuration.h
```
#ifndef DATAPIPELINE_H
#define DATAPIPELINE_H

#include <WiFi.h>

const char* ssid = ssid;
const char* password = password;

const char* mqtt_server = laptop's ip
const int mqtt_port = port
const char* mqtt_topic = topic

const char* user_name=abc
const char* pass_word=xyz
#endif
```
