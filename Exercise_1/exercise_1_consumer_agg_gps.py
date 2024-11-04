import asyncio
import random
import time
import json

## Issue since python 3.12 https://github.com/dpkp/kafka-python/issues/2412
from kafka import KafkaProducer, KafkaConsumer

# Kafka Configuration
KAFKA_BROKER = "localhost:9092,localhost:9093,localhost:9094"  # Replace with your Kafka broker address
# Internal Listeners kafka1:9092,kafka2:9092,kafka3:9092
AGG_GPS_TOPIC = "agg_gps_topic"

#tion to consume data from Kafka topics Func
def consume_sensor_data():
    # Initialize Kafka Consumer for both topics
    consumer = KafkaConsumer(
        AGG_GPS_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        group_id="data_consumers",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    for message in consumer:
        topic = message.topic
        data = message.value
        print(f"Consumed from {topic}: {data}")

# run the consumer
if __name__ == "__main__":
    consume_sensor_data()