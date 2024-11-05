import asyncio
import random
import time
import json
import pika

# RabbitMQ Configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
SENSOR_QUEUE = "sensor_data"
GPS_QUEUE = "gps_data"

# Initialize RabbitMQ connection and channels
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
))
channel_sensor = connection.channel()
channel_sensor.queue_declare(queue=SENSOR_QUEUE)

channel_gps = connection.channel()
channel_gps.queue_declare(queue=GPS_QUEUE)

# Event-based data generator (10 Hz)
async def sensor_data_generator():
    while True:
        timestamp = time.time()
        sensor_data = {
            "timestamp": timestamp,
            "event_id": random.randint(1000, 9999),
            "value": random.random(),
            "status": random.choice(["active", "inactive"]),
        }

        # Publish sensor data to RabbitMQ
        channel_sensor.basic_publish(exchange='', routing_key=SENSOR_QUEUE, body=json.dumps(sensor_data))
        print(f"Event Data (10 Hz): {sensor_data}")
        await asyncio.sleep(0.1)  # 10 Hz -> every 0.1 seconds

# Mocked GPS data generator (2 Hz)
async def gps_data_generator():
    lat, lon = 37.7749, -122.4194  # Starting coordinates (e.g., San Francisco)
    while True:
        # Random small variation in latitude and longitude to simulate movement
        lat += random.uniform(-0.0001, 0.0001)
        lon += random.uniform(-0.0001, 0.0001)
        timestamp = time.time()
        gps_data = {
            "timestamp": timestamp,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "speed": round(random.uniform(0, 20), 2),  # Speed in m/s
        }

        # Publish GPS data to RabbitMQ
        channel_gps.basic_publish(exchange='', routing_key=GPS_QUEUE, body=json.dumps(gps_data))
        await asyncio.sleep(0.5)  # 2 Hz -> every 0.5 seconds

# Main function to run both generators concurrently
async def main():
    # Run producers as background tasks
    await asyncio.gather(
        sensor_data_generator(),
        gps_data_generator(),
    )

    # Close the RabbitMQ connection when the main function exits
    connection.close()

# Run the main function
asyncio.run(main())