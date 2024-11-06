### Part 4: Performance Analysis and Evaluation of your Application

Profile your producers and consumers/data sinks. Describe the patterns and bottlenecks you see while executing different scenarios and workloads. Perform 2-3 experiments with different configurations.

  Some example experiments:
  
  * Measure the average time incl. standard deviation required by your producer/consumer loop over several runs.
  * Determine which call of your producer/consumer takes the most time. Which 3 methods are called the most or need the most time and how much time?
  * Create a profile of your producer/consumer code in a xxxxx.prof file and create 1-2 visualizations of the profile (e.g. with [SnakeViz](https://jiffyclub.github.io/snakeviz/)) to which you explain in the context of the profiling work.

#### Bonus 4
Mitigate or produce a bottleneck.


## Reflection

Write a reflection on the realization of the mini-challenge. What went well? Where did problems occur? Where did you need more time than planned? 
What would you do differently in the future? What would you change in the assignment? Give examples in each case.


### Exercise 1

For the reflection of this mini-challenge I will focus on each exercise separately. Starting of with the first exercise, I had a lot of fun with the first task. And tried to though of a good case, where we can add some easy aggregation on self-generated data. I believe that the gps data has a nice touch but average aggregation over 2s could have been a bit more creative. The visualization in the sub task 3 of the exercise was really good, because I needed to rethink how the kafka brokers are accessed and how the data is being synchronized over all partitions and replications over the brokers. 

### Exercise 2

The second exercise was a perfect preparation for the [confluent developer certification](https://training.confluent.io/examdetail/confluent-dev). The deep dives I made were interesting and good learning experiences, I will go a bit deeper in each point in the following part:

- Consumer_Groups: The consumer group is a really nice way to split up work between parrallely running consumers from a topic. Because they are structured that all the messages are only consumed exactly once instead. Therefore, the risk of redundancy is completely minimized. 
- Transformation: I've never worked together with python and kafka. It was a really good experience to implement the avro conversion not with a java custom processor in NiFi. By adding the schema registry you have a lot more that is being tracked. There's a completely new component in the mixed that needs to be managed.
- Offset and Reprocessing: The offset is quite a interesting structure that kafka integrated, I think the concept behind it is quite exciting. I have more information summarized in the Deepdive.md. The delivery strategie is also a really important point, the 'exactly once' strategy, I've experienced the most when setting up Kafka clusters
- Replication Factor and Partition Counts: The partitioning over all the brokers is quite a interesting topics, but it's also documented in the deep dive.

### Exercise 3

Previously, I've never worked with RabbitMQ, therefore this task was really interesting. I made my first experiences with RabbitMQ. The major differences and informations gotten in this task are following:

- Kafka: Best for high-throughput, persistent event streaming and data pipelines with message replay. Optimized for log-based, distributed messaging where messages are retained in topics for a set duration.
- RabbitMQ: Ideal for low-latency, transactional messaging, and task queues. Messages are routed flexibly but are transient unless explicitly persisted.
- Consumer Model: Kafka uses consumer groups for scalable partitioned processing; RabbitMQ allows flexible routing and direct queue-based consumption.
- Performance: Kafka handles high message rates; RabbitMQ excels in low-latency delivery for synchronous tasks.

The second and bonus task was focusing on the dockerization of the application and integrating it in k8s. I've experienced a few problems with the dockerization with the networking structure. At first I had the configuration wrongly configured, and the kafka brokers and kafdrop wasn't working. But after some testing and reconfiguration the services/apps inside the docker-compose were able to talk with eachother. I lost about 2.5 hours on this issue and got a bit desperated. For the k8s integration, I wasn't able to setup k8s on my laptop, but I'm quite experienced with k8s and Openshift (on top of k8s). 

### Exercise 4

In the exercise 4, I've tried to make some performance tests. Firstly I did it with rabbitmq. the problem I've sent there was not the queueing up of new messages, but the consuming part of it, seems to be not as fast. In the performance example 2 we see that more messages are being queued and not being acknowledged. That seems to verify that we are hitting a bottleneck on the consuming. The producing part seems to be more efficient.

In comparison to RabbitMQ, Kafka is a lot more performant than rabbit mq, it seems that most of the limitation I have in this bottleneck are caused by my hardware instead of the Kafka capabilities. I've also made quite a lot of discoveries in a customer project, in this project the resources were outstanding, compared what you would have on a normal computer. More detailed information can be found here [best practices kafka](https://aws.amazon.com/de/blogs/big-data/best-practices-for-right-sizing-your-apache-kafka-clusters-to-optimize-performance-and-cost/)