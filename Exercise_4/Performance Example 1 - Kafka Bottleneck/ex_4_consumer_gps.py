import asyncio
import random
import time
import json
import csv
from uuid import uuid4
from datetime import datetime

from confluent_kafka import Producer, Consumer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer

# Kafka Configuration
KAFKA_BROKERS = "kafka1:19092,kafka2:19093,kafka3:19094"
GPS_TOPIC = "gps_data"
AGG_GPS_TOPIC = "agg_gps_topic"
GROUP_ID = "consumer_group_gps"
SCHEMA_REGISTRY_URL = "http://schema-registry:8081"

avro_raw_schema_str = '{"type": "record","name": "Message","namespace": "com.gps","fields": [{"name": "latitude", "type": "double"},{"name": "longitude", "type": "double"},{"name": "speed", "type": "double"},{"name": "timestamp", "type": "double"}]}'

# Load the Avro schema
avro_agg_schema_str = '{"type": "record","name": "Message","namespace": "com.gps.agg","fields": [{"name": "id", "type": "int"},{"name": "avg_latitude", "type": "double"}, {"name": "avg_longitude", "type": "double"},{"name": "num", "type": "double"},{"name": "timestamp", "type": "double"}]}'

schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

### Consumer Configuration
avro_deserializer = AvroDeserializer(schema_registry_client,
                                     avro_raw_schema_str)

consumer_conf = {'bootstrap.servers': KAFKA_BROKERS,
                 'group.id': GROUP_ID,
                 'auto.offset.reset': "earliest"}

### Producer Configuration
avro_serializer = AvroSerializer(schema_registry_client,
                                 avro_agg_schema_str)

string_serializer = StringSerializer('utf_8')

producer_conf = {'bootstrap.servers': KAFKA_BROKERS}

producer = Producer(producer_conf)

# CSV Files for Storing Data
GPS_CSV_FILE = "/app/data/aggregated_gps_data.csv"

# Write headers to CSV if the file does not exist
with open(GPS_CSV_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "center_latitude", "center_longitude"])

def consume_gps_data():
    consumer = Consumer(consumer_conf)
    consumer.subscribe([GPS_TOPIC])

    gps_buffer = []
    last_aggregation_time = time.time()

    id = 0

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        # Deserialize Avro to JSON
        data = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
        topic = msg.topic()

        gps_buffer.append(data)

        # Check if 2 seconds have passed to aggregate
        current_time = time.time()
        if current_time - last_aggregation_time >= 2:
            if gps_buffer:
                # Calculate center of buffered GPS points
                avg_lat = sum(point["latitude"] for point in gps_buffer) / len(gps_buffer)
                avg_lon = sum(point["longitude"] for point in gps_buffer) / len(gps_buffer)
                aggregation_timestamp = datetime.now()

                # Write aggregated GPS data to CSV
                with open(GPS_CSV_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([aggregation_timestamp.isoformat(), avg_lat, avg_lon])

                id += 1

                unix_timestamp = datetime.timestamp(aggregation_timestamp)*1000

                agg_gps_data = {
                    "id": id,
                    "timestamp": unix_timestamp,
                    "avg_latitude": avg_lat,
                    "avg_longitude": avg_lon,
                    "num": len(gps_buffer)
                }

                producer.produce(topic=AGG_GPS_TOPIC,
                                 key=string_serializer(str(uuid4())),
                                 value=avro_serializer(agg_gps_data, SerializationContext(AGG_GPS_TOPIC, MessageField.VALUE)))

                producer.flush()

                # Reset buffer and aggregation time
                gps_buffer = []
                last_aggregation_time = current_time


if __name__ == "__main__":
    consume_gps_data()