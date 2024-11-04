import asyncio
import random
import time
import json
from kafka import KafkaProducer, KafkaConsumer

# Kafka Configuration
KAFKA_BROKER = "kafka1:9092,kafka2:9092,kafka3:9092"  # Replace with your Kafka broker address
SENSOR_TOPIC = "sensor_data"
GPS_TOPIC = "gps_data"

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

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

        # Produce event data to Kafka
        producer.send(SENSOR_TOPIC, sensor_data)
        producer.flush()  # Ensure data is sent

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

        # Produce GPS data to Kafka
        producer.send(GPS_TOPIC, gps_data)
        producer.flush()  # Ensure data is sent

        print(f"GPS Data (2 Hz): {gps_data}")
        await asyncio.sleep(0.5)  # 2 Hz -> every 0.5 seconds

# Main function to run both generators concurrently
async def main():
    # Run producers as background tasks
    await asyncio.gather(
        sensor_data_generator(),
        gps_data_generator(),
    )

# Run the main function
asyncio.run(main())