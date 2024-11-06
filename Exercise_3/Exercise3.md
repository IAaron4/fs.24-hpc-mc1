
### Part 3: Communication Patterns

1. Rewrite your application of part 1 using another communication framework such as RabbitMQ and/or another underlying messaging protocol such as ZeroMQ or MQTT.
    
2. Pack your rewritten application into containers.

3. Answer the following questions and interpret your experiments or results: 
      * Compare the communication patterns of Kafka and your chosen technology. Where are they similar, where different? How do those patterns work? Are there advantages or disadvantages of those patterns? 
      * Are there any known issues with those patterns? If yes, how could those issues be mitigated or on the other hand provoked? If possible, show this with an experiment.
      * How scalable are those two approaches? What challenges need to be considered?

**Communication Patterns**
- **Kafka**: Primarily uses a high-throughput **pub-sub pattern** with persistent message storage in **topics**. Ideal for event streaming and data pipelines, allowing replays but with potentially higher latency.
- **RabbitMQ**: Offers **message queuing** with flexible routing via **exchanges** (direct, topic, fanout, headers). Optimized for low-latency, transactional tasks, and supports complex workflows, but may lose messages without persistence enabled.

**Known Issues**
- **Kafka**:
  - **Consumer Lag**: Slow consumers can fall behind with high message volumes. *Mitigation*: Add consumers or auto-scale, monitor lag.
  - **Rebalancing Delays**: Consumer group rebalances can briefly disrupt processing. *Mitigation*: Configure timeouts, use sticky partitioning.
- **RabbitMQ**:
  - **Message Loss Without Persistence**: Messages may be lost if consumers are down. *Mitigation*: Enable persistent queues and acknowledgments.
  - **Queue Bottlenecks**: High-load queues can limit throughput. *Mitigation*: Shard queues across nodes, use clustering.

**Scalability**
- **Kafka**: Scales horizontally by adding brokers and partitions, suitable for large-scale streaming. Challenges include network bandwidth and data rebalancing.
- **RabbitMQ**: Scales through clustering and sharding queues, but less suited for high throughput compared to Kafka. Works best for smaller-scale, low-latency applications.

#### Bonus 3
Show how your container setup could be integrated into a container orchestration system (such as Kubernets) and how it would profit from this. Or show how you could replace some of the components with cloud-based offers and what changes/considerations come with this.


#### Differences in the files

##### rabbitmq_consumer_agg_gps.py
The key changes in the updated code are:

- Replaced Kafka-specific configuration (broker, topic) with RabbitMQ configuration (host, user, password, queue name).
- Initialized the RabbitMQ connection and channel using the pika library.
- Defined the consume_agg_gps_data function to consume messages from the RabbitMQ aggregated GPS data queue.
- Inside the consume_agg_gps_data function:
  - Implemented the RabbitMQ message callback function to handle incoming aggregated GPS data messages.
  - Printed the consumed aggregated GPS data.
  - Acknowledged the message to RabbitMQ after processing.


Called the consume_agg_gps_data function in the if __name__ == "__main__": block to run the consumer.

##### rabbitmq_consumer_gps.py
The key changes in the updated code are:

- Replaced Kafka-specific configuration (broker, topics) with RabbitMQ configuration (host, user, password, queue names).
- Initialized the RabbitMQ connection and channels using the pika library.
- Defined the consume_gps_data function to consume messages from the RabbitMQ GPS data queue.
- Inside the consume_gps_data function:

  - Implemented the RabbitMQ message callback function to handle incoming GPS data messages.
  - Buffered the GPS data and calculated the average latitude and longitude every 2 seconds.
  - Wrote the aggregated GPS data to the aggregated_gps_data.csv file.
  - Published the aggregated GPS data to the RabbitMQ aggregated GPS data queue.
  - Acknowledged the message to RabbitMQ after processing.


Called the consume_gps_data function in the if __name__ == "__main__": block to run the consumer.

##### rabbitmq_consumer_sensor.py
The key changes in the updated code are:

- Replaced Kafka-specific configuration (broker, topic) with RabbitMQ configuration (host, user, password, queue name).
- Initialized the RabbitMQ connection and channel using the pika library.
- Defined the consume_sensor_data function to consume messages from the RabbitMQ queue.
- Inside the consume_sensor_data function:
  - Implemented the RabbitMQ message callback function to handle incoming messages.
  - Wrote the event data to the event_data.txt file.
  - Acknowledged the message to RabbitMQ after processing.

##### rabbitmq_publisher.py
The key changes are:

- Replaced Kafka broker and schema registry configuration with RabbitMQ host, user, and password.
- Replaced Kafka topic names with RabbitMQ queue names.
- Used pika.basic_publish to publish data to the RabbitMQ queues instead of Kafka.
- Removed all Avro-related code and dependencies.
