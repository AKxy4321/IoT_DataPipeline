# IoT_DataPipeline

## Requirements 
- Apache Kafka
- Mosquitto MQTT Broker
- Influxdb

## Setup 
Python = 3.10
```
pip install paho-mqtt confluent-kafka influxdb-client
```

## Workings
1. IoT Device (iot_device_mqtt.py) sends temperature readings every 3s.
2. Mosquitto MQTT Broker receives the readings from the IoT device and sends it to Kafka.
3. From Kafka, we save the readings to influxdb.
4. We then have read_influxdb.py query influxdb every 3s and get the latest readings, it will then determine if its hot or cold and print output to command line.