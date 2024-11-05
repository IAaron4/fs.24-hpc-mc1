import asyncio
import random
import time
import json
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

# Kafka Configuration
KAFKA_BROKER = "localhost:9092,localhost:9093,localhost:9094"
GPS_TOPIC = "gps_data"
SCHEMA_REGISTRY_URL = "http://localhost:8081"

# Load the Avro schema
with open("ex_2_raw_gps_schema.avsc") as f:
    avro_schema_str = f.read()

schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(schema_registry_client,
                                 avro_schema_str)

string_serializer = StringSerializer('utf_8')

producer_conf = {'bootstrap.servers': KAFKA_BROKER}

producer = Producer(producer_conf)

# Mocked GPS data generator (2 Hz)
async def gps_data_generator():
    lat, lon = 37.7749, -122.4194  # Starting coordinates (e.g., San Francisco)
    while True:
        # Random small variation in latitude and longitude to simulate movement
        lat += random.uniform(-0.0001, 0.0001)
        lon += random.uniform(-0.0001, 0.0001)
        timestamp = time.time()
        gps_data = {
            "timestamp": timestamp,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "speed": round(random.uniform(0, 20), 2),  # Speed in m/s
        }

        producer.produce(topic=GPS_TOPIC,
                         key=string_serializer(str(uuid4())),
                         value=avro_serializer(gps_data, SerializationContext(GPS_TOPIC, MessageField.VALUE)))

        producer.flush()

        await asyncio.sleep(0.1)  # 10 Hz -> every 0.2seconds

# Main function to run both generators concurrently
async def main():
    # Run producers as background tasks
    await asyncio.gather(
        gps_data_generator()
    )

# Run the main function
asyncio.run(main())