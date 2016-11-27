+ Open terminal & go into kafka installation folder 

+ Run the following commands
  + start zookeeper from one terminal: 
  ```
  bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
  + start kafka from another terminal: 
  ```
  bin/kafka-server-start.sh config/server.properties
  ```
  + create a topic name `test`: 
  ```
  bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
  ```
  + show list of topics: 
  ```
  bin/kafka-topics.sh --list --zookeeper localhost:2181
  ```

+ Go into the Spark_mini_js4722_ig2333 folder
  + run producer.py from one terminal : 
  ```
  python Producer.py
  ```
+ Open another terminal, go into the spark folder, run the following command:
  + run spark on topic `test`: 
  ```
  bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 /Users/susheryl/Desktop/Spark_mini/wordcount.py localhost:2181 test
  ```
  + You can replace "/Users/susheryl/Desktop/Spark_mini/wordcount.py" with the local path to the wordcount.py on your machine
  + After you set up all of these four terminals, you should be able to see the word count of the real data stream in the terminal that runs spark-submit