# Mini-Challenge 1 - High Performance Computing (hpc) FS24

## Containers, Communication Patterns/Frameworks and Performance Analysis

You design a micro service based application, which has multiple producers of data, as well as multiple different consumers of the data. To do this, you want to use the [Apache Kafka - Data Streaming Platform](https://kafka.apache.org/) in a first step. In a second step it will use a different communication pattern (and/or framework). The application runs distributed in different Docker containers. Define what kind of data your application has and what problem they want to solve with it. Describe the initial situation and the problem to be solved. Then implement your methods according to the tasks below. Write a short report and answer the questions of each of the 4 parts bellow. Include measurements/plots where meaningful.

[Use GitHubClassroom to work on this mini challenge](https://classroom.github.com/a/18HqjioC)

### Intro to Kafka using Docker containers

1. Set up Kafka locally on your computer by using the provided Docker Compose file or create your own setup. Command line:`docker-compose up -d`.

    We start with a Docker compose template, which launches 5 containers:

    * broker-[x] - Kafka brokers
    * jupyter    - Jupyter environment for the connection to our Kafka cluster using notebooks (This is not good, you should atleast preinstall wand fully)
    * I removed the instance because it's hard to install wand
    * kafdrop    - web UI for browsing and monitoring Kafka clusters

2. Open the Jupyter notebook on your machine using: http://127.0.0.1:8888. Start to play around with sending and receiving messages. Use [Kafdrop]( https://github.com/obsidiandynamics/kafdrop) to monitor/explore your cluster, topics, and messages. For example, start and stop individual brokers (e.g. via Docker Desktop) or change Kafka parameters such as the replication factor and watch how the cluster behaves via Kafdrop.

3. Make sure you understand how each container can talk to the other containers and how you can access a network interface of the containers.

### Part 1: Kafka Cluster and Application Setup

1. Write at least two different data generator functions, which regularly send messages containing data. One generator should send 10 messages at least every second (10Hz). Choose yourself which data is sent. The application of the data can be chosen freely, but choose a good mixture of a simple and a complex message. The data should be variable. The data generator can send simulated data or real data. Use suitable Kafka components and meaningful names of functions, variables etc. for the implementation.

    Tips:
    * Use several notebooks so that you can start and stop the endless loops of data processing individually.
    * Use python programs rather than notebooks to automatically start the producers/consumers within their own containers.
    * After testing, stop the endless loop again, otherwise your computer resources are unnecessarily occupied or at the limit.

2. Write at least one data consumer that regularly reads and processes the data from the generators and re-inserts the processed data into the Kafka cluster, e.g., a calculation or a machine learning application on the retrieved data; a data enrichment; or the extraction or enrichment of information based on the message. Also, write at least two data sinks which process the retrieved data and store it to the disk, e.g. in a CSV file. Use appropriate Kafka components and meaningful names of functions, variables, etc. for the implementation. The image below shows a schematic overview over the basic implementation requirements.

![Kafka Base Schema](images/kafka-base-schema.png)

3. Draw an overview of your application components including interfaces and data flows, for example using a component diagram. Write a proper architecture and design overview which ansers at least the following questions.

      * What are the tasks of the components?
      * Which interfaces do the components have?
      * Why did you decide to use these components?
      * Are there any other design decisions you have made? Which requirements (e.g. libraries, hardware, ...) does a component have?
      * Which features of Kafka do you use and how does this correlate to the cluster / topic settings you choose?
      * Describe the Docker setup of your application.

#### Bonus 1
Use more efficient serializers/deserializers than JSON for the messages.
 