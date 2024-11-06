import asyncio
import random
import time
import json

from confluent_kafka import Consumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField

# Kafka Configuration
KAFKA_BROKER = "kafka1:19092,kafka2:19093,kafka3:19094"
# Internal Listeners kafka1:9092,kafka2:9092,kafka3:9092
AGG_GPS_TOPIC = "agg_gps_topic"
GROUP_ID = "agg_gps_consumer_group"
SCHEMA_REGISTRY_URL = "http://schema-registry:8081"

# Initialize schema registry client and load schema
schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Load the Avro schema
avro_agg_schema_str = '{"type": "record","name": "Message","namespace": "com.gps.agg","fields": [{"name": "id", "type": "int"},{"name": "avg_latitude", "type": "double"}, {"name": "avg_longitude", "type": "double"},{"name": "num", "type": "double"},{"name": "timestamp", "type": "double"}]}'

### Consumer Configuration
avro_deserializer = AvroDeserializer(schema_registry_client,
                                     avro_agg_schema_str)

consumer_conf = {'bootstrap.servers': KAFKA_BROKER,
                 'group.id': GROUP_ID,
                 'auto.offset.reset': "earliest"}


#tion to consume data from Kafka topics Func
def consume_sensor_data():
    consumer = Consumer(consumer_conf)
    consumer.subscribe([AGG_GPS_TOPIC])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        # Deserialize Avro to JSON
        data = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
        topic = msg.topic()

        print(f"Consumed from {topic}: {data}")

# run the consumer
if __name__ == "__main__":
    consume_sensor_data()