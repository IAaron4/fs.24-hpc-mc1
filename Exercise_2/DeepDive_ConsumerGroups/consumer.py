import json
import csv
from kafka import KafkaConsumer
import sys
import time

# Kafka Configuration
KAFKA_BROKER = "localhost:9092,localhost:9093,localhost:9094"
TOPIC_NAME = "ex_2_consumergroups_topic"
GROUP_ID = "ex_2_consumergroups"  # All consumers in this group share the load


def consume_messages(consumer_id):
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    # CSV file for each consumer based on its ID
    consumer_csv_file = f"consumer_{consumer_id}_messages.csv"

    # Initialize CSV file with headers
    with open(consumer_csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "value", "timestamp", "consumer_id"])

    print(f"Consumer {consumer_id} started.")

    for message in consumer:
        message_value = message.value
        message_value["consumer_id"] = consumer_id  # Adding consumer_id to track source

        print(f"Consumer {consumer_id} consumed: {message_value}")

        # Write the message to the consumer's CSV file
        with open(consumer_csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([message_value["id"], message_value["value"], message_value["timestamp"], consumer_id])


if __name__ == "__main__":
    # Pass a unique identifier to each consumer (e.g., 1, 2, or 3)
    if len(sys.argv) != 2:
        print("Usage: python consumer.py <consumer_id>")
        sys.exit(1)

    consumer_id = sys.argv[1]
    consume_messages(consumer_id)
