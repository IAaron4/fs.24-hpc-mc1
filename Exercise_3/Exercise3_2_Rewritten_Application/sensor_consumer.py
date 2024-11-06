import asyncio
import random
import time
import json
import pika
import os

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
SENSOR_QUEUE = "sensor_data"
EVENT_FILE = "/app/data/event_data.txt"

# Initialize RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
))
channel = connection.channel()
channel.queue_declare(queue=SENSOR_QUEUE)


# Function to consume data from RabbitMQ queue
def consume_sensor_data():
    def callback(ch, method, properties, body):
        data = json.loads(body.decode("utf-8"))

        # Write event data to disk
        with open(EVENT_FILE, mode="a") as file:
            file.write(json.dumps(data) + "\n")

        print(f"Event Data Written: {data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=SENSOR_QUEUE,
        on_message_callback=callback,
        auto_ack=False
    )

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Run the consumer
if __name__ == "__main__":
    consume_sensor_data()