import time
import json
import csv
from kafka import KafkaProducer

# Kafka Configuration
KAFKA_BROKER = "localhost:9092,localhost:9093,localhost:9094"
TOPIC_NAME = "ex_2_consumergroups_topic"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# File to log all produced messages
PRODUCER_CSV_FILE = "producer_messages.csv"

# Initialize CSV file with headers
with open(PRODUCER_CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "value", "timestamp"])


def produce_messages():
    for i in range(100):  # Producing 1000 messages
        message = {"id": i, "value": f"Message {i}", "timestamp": time.time()}

        # Send message to Kafka
        producer.send(TOPIC_NAME, message)
        print(f"Produced: {message}")

        # Log message to CSV file
        with open(PRODUCER_CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([message["id"], message["value"], message["timestamp"]])

        time.sleep(0.1)  # Slight delay between messages for demonstration

    producer.flush()
    producer.close()


if __name__ == "__main__":
    produce_messages()