from __future__ import print_function

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import sys, traceback


def calculate_count(time, rdd):
    print('\n')
    print('========= %s =========' % str(time))
    print('\n')

    try:
        local_counts = rdd.map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a + b)
        for x in local_counts.collect():
            print(x)

    except:
        print('Did not print rdd properly')
        traceback.print_exc(file=sys.stdout)
        pass


def main():
    if len(sys.argv) != 3:
        print("Usage: wordcount.py <zookeeper_localhost_address> <topic_name>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="Spark_Streaming_Kafka_WordCount")
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])  # map() returns a new DStream
    counts = lines.flatMap(lambda line: line.split(" "))

    counts.foreachRDD(calculate_count)
    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    main()
