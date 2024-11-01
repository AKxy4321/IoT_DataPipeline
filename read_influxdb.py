from influxdb_client import InfluxDBClient
from dotenv import load_dotenv
import time
import os

load_dotenv()

INFLUXDB_URL = os.environ.get('INFLUXDB_URL')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.environ.get('INFLUXDB_BUCKET')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN')

influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

# Define the temperature threshold (Cold if <= 25, else Hot)
TEMPERATURE_THRESHOLD = 25  

# Loop to continuously check the temperature
try:
    while True:
        # Query to get the latest temperature
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -1h)  // Get data from the last hour
        |> filter(fn: (r) => r["_measurement"] == "sensor_data" and r["_field"] == "temperature")
        |> last()  // Get the most recent entry
        '''

        result = influxdb_client.query_api().query(query)

        # Process the query result
        for table in result:
            for record in table.records:
                temperature = record.get_value()
                print(f"Received Temperature: {temperature} °C")
                
                if temperature > TEMPERATURE_THRESHOLD:
                    print("It's hot!")
                else:
                    print("It's cold!")

        # Add delay
        time.sleep(3) 

except KeyboardInterrupt:
    print("Stopping the temperature monitor.")

finally:
    influxdb_client.close()
