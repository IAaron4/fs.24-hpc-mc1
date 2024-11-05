import asyncio
import random
import time
import json
import pika

# RabbitMQ Configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
AGG_GPS_QUEUE = "agg_gps_data"

# Initialize RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
))
channel = connection.channel()
channel.queue_declare(queue=AGG_GPS_QUEUE)

# Function to consume aggregated GPS data from RabbitMQ queue
def consume_agg_gps_data():
    def agg_gps_data_callback(ch, method, properties, body):
        data = json.loads(body.decode("utf-8"))
        print(f"Consumed aggregated GPS data: {data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=AGG_GPS_QUEUE,
        on_message_callback=agg_gps_data_callback,
        auto_ack=False
    )

    print('Waiting for aggregated GPS data. To exit press CTRL+C')
    channel.start_consuming()

# Run the consumer
if __name__ == "__main__":
    consume_agg_gps_data()