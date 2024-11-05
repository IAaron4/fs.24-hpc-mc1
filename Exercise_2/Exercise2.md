
### Part 2: Performance Analysis and Evaluation of Kafka

In this part you will adjust the application you developed in part 1. In the following list you find a multitude of "Deep Dives" where you use advanced Kafka topics. Use at least two of them and apply those on your application.   

* Consumer Groups (@Aaron)
  * https://docs.confluent.io/platform/current/clients/consumer.html
* Find out the limits of send/receive of your application (and of Kafka in general)
* Distribution of brokers and partitions
* *Replication factors and partition counts* (@Aaron)
  * https://docs.confluent.io/kafka/design/replication.html
  * https://learn.conduktor.io/kafka/kafka-topics-choosing-the-replication-factor-and-partitions-count/
* Offset/Reprocessing (@Aaron)
  * https://dattell.com/data-architecture-blog/understanding-kafka-consumer-offset/
  * https://www.redpanda.com/guides/kafka-architecture-kafka-offset
  * https://www.confluent.io/events/kafka-summit-london-2023/reliable-message-reprocessing-patterns-for-kafka/
* Retention/Compaction
* *Kafka Streams* (@Aaron)
  * https://stackoverflow.com/questions/51918941/does-kafka-python-api-support-stream-processing
  * https://docs.confluent.io/platform/current/streams/introduction.html
* Retries
* How does a key have to look like?

Perform different experiments with your chosen DeepDives with different configurations/scenarios and describe the results. Conclude with effective use cases for those features in case your own application is not really a use case for them.

#### Bonus 2
Make more than 2 DeepDives. (This one I got)