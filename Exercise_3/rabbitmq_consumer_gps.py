import asyncio
import random
import time
import json
import csv
import pika
from datetime import datetime

# RabbitMQ Configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
GPS_QUEUE = "gps_data"
AGG_GPS_QUEUE = "agg_gps_data"
GPS_CSV_FILE = "aggregated_gps_data.csv"

# Initialize RabbitMQ connection and channels
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
))
channel_gps = connection.channel()
channel_gps.queue_declare(queue=GPS_QUEUE)

channel_agg = connection.channel()
channel_agg.queue_declare(queue=AGG_GPS_QUEUE)

# Write headers to CSV if the file does not exist
with open(GPS_CSV_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "center_latitude", "center_longitude"])

# Function to consume GPS data from RabbitMQ queue
def consume_gps_data():

    def gps_data_callback(ch, method, properties, body):
        global gps_buffer
        global last_aggregation_time

        data = json.loads(body.decode("utf-8"))

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

                # Publish aggregated GPS data to RabbitMQ
                channel_agg.basic_publish(exchange='', routing_key=AGG_GPS_QUEUE, body=json.dumps(agg_gps_data))

                # Reset buffer and aggregation time
                gps_buffer = []
                nonlocal last_aggregation_time
                last_aggregation_time = current_time

        ch.basic_ack(delivery_tag=method.delivery_tag)

    gps_buffer = []
    last_aggregation_time = time.time()

    channel_gps.basic_consume(
        queue=GPS_QUEUE,
        on_message_callback=gps_data_callback,
        auto_ack=False
    )

    print('Waiting for GPS data. To exit press CTRL+C')
    channel_gps.start_consuming()

# Run the consumer
if __name__ == "__main__":

    consume_gps_data()