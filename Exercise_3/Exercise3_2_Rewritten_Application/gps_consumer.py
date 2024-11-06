import time
import json
import csv
import pika
from datetime import datetime
from collections import deque
from threading import Lock, Timer
import os

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
GPS_QUEUE = "gps_data"
AGG_GPS_QUEUE = "AGG_GPS_DATA"
GPS_CSV_FILE = "/app/data/aggregated_gps_data.csv"


class GPSDataConsumer:
    def __init__(self):
        # Initialize RabbitMQ connection and channels
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        ))

        self.connection2 = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        ))

        # Channel for publishing aggregated data
        self.channel_agg = self.connection2.channel()
        self.channel_agg.queue_declare(queue=AGG_GPS_QUEUE)

        # Channel for consuming GPS data
        self.channel_gps = self.connection.channel()
        self.channel_gps.queue_declare(queue=GPS_QUEUE)

        # Initialize buffer and lock
        self.gps_buffer = deque()
        self.buffer_lock = Lock()

        # Create CSV file with headers if it doesn't exist
        with open(GPS_CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if file is empty
                writer.writerow(["timestamp", "center_latitude", "center_longitude"])

        # Start the aggregation timer
        self.start_aggregation_timer()

    def start_aggregation_timer(self):
        """Start a timer that triggers aggregation every 2 seconds"""
        Timer(2.0, self.aggregate_gps_data).start()

    def aggregate_gps_data(self):
        """Aggregate GPS data from the buffer"""
        with self.buffer_lock:
            if len(self.gps_buffer) > 0:
                # Calculate averages
                avg_lat = sum(point["latitude"] for point in self.gps_buffer) / len(self.gps_buffer)
                avg_lon = sum(point["longitude"] for point in self.gps_buffer) / len(self.gps_buffer)
                aggregation_timestamp = datetime.now().isoformat()

                # Write to CSV
                with open(GPS_CSV_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([aggregation_timestamp, avg_lat, avg_lon])

                # Prepare aggregated data
                agg_gps_data = {
                    "timestamp": aggregation_timestamp,
                    "avg_latitude": avg_lat,
                    "avg_longitude": avg_lon
                }

                # Publish aggregated data
                self.channel_agg.basic_publish(
                    exchange='',
                    routing_key=AGG_GPS_QUEUE,
                    body=json.dumps(agg_gps_data)
                )

                print(f"Aggregated {len(self.gps_buffer)} points: {agg_gps_data}")

                # Clear the buffer
                self.gps_buffer.clear()

        # Schedule next aggregation
        self.start_aggregation_timer()

    def callback(self, ch, method, properties, body):
        """Callback function for handling incoming GPS data"""
        try:
            data = json.loads(body.decode("utf-8"))

            # Add data to buffer
            with self.buffer_lock:
                self.gps_buffer.append(data)

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError as e:
            print(f"Error decoding message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        """Start consuming messages from the GPS queue"""
        try:
            self.channel_gps.basic_consume(
                queue=GPS_QUEUE,
                on_message_callback=self.callback,
                auto_ack=False
            )

            print('Started consuming GPS data. To exit press CTRL+C')
            self.channel_gps.start_consuming()

        except KeyboardInterrupt:
            print("Shutting down consumer...")
            self.channel_gps.stop_consuming()
            self.connection.close()


def main():
    consumer = GPSDataConsumer()
    consumer.start_consuming()


if __name__ == "__main__":
    main()