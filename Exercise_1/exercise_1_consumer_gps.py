import asyncio
import random
import time
import json
import csv
from kafka import KafkaProducer, KafkaConsumer
from datetime import datetime

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
EVENT_TOPIC = "event_data"
GPS_TOPIC = "gps_data"
AGG_GPS_TOPIC = "agg_gps_topic"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# CSV Files for Storing Data
GPS_CSV_FILE = "aggregated_gps_data.csv"

# Write headers to CSV if the file does not exist
with open(GPS_CSV_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "center_latitude", "center_longitude"])

#tion to consume data from Kafka topics Func
def consume_gps_data():
    # Initialize Kafka Consumer for both topics
    consumer = KafkaConsumer(
        GPS_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        group_id="data_consumers",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    gps_buffer = []
    last_aggregation_time = time.time()

    for message in consumer:
        topic = message.topic
        data = message.value
        print(f"Consumed from {topic}: {data}")

        gps_buffer.append(data)

        # Check if 2 seconds have passed to aggregate
        current_time = time.time()
        if current_time - last_aggregation_time >= 2:
            if gps_buffer:
                # Calculate center of buffered GPS points
                avg_lat = sum(point["latitude"] for point in gps_buffer) / len(gps_buffer)
                avg_lon = sum(point["longitude"] for point in gps_buffer) / len(gps_buffer)
                aggregation_timestamp = datetime.now().isoformat()

                # Write aggregated GPS data to CSV
                with open(GPS_CSV_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([aggregation_timestamp, avg_lat, avg_lon])

                agg_gps_data = {
                    "timestamp": aggregation_timestamp,
                    "avg_latitude": avg_lat,
                    "avg_longitude": avg_lon
                }

                # Produce event data to Kafka
                producer.send(AGG_GPS_TOPIC, agg_gps_data)
                producer.flush()  # Ensure data is sent


                # Reset buffer and aggregation time
                gps_buffer = []
                last_aggregation_time = current_time

# run the consumer
if __name__ == "__main__":
    consume_gps_data()