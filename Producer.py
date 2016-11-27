from kafka import KafkaProducer
import json
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import ConfigParser
import traceback
import sys

# API Keys
config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))
consumerKey=config.get('API Keys', 'consumerKey')
consumerSecret=config.get('API Keys', 'consumerSecret')
accessToken=config.get('API Keys', 'accessToken')
accessSecret=config.get('API Keys', 'accessSecret')

# Other variables
REQUEST_LIMIT = 420
producer = KafkaProducer(bootstrap_servers=['localhost:9092']) # Create a producer and connect to Zookeeper

class TweetListener(StreamListener):
    def on_data(self, data):
        try:
            sendTweet(data)
        except:
            print("No location data found")
            # traceback.print_exc(file=sys.stdout)

        return(True)

    def on_error(self, status):
        errorMessage = "Error - Status code " + str(status)
        print(errorMessage)
        if status == REQUEST_LIMIT:
            print("Request limit reached. Trying again...")
            exit()

# producer sends tweet to consumer
def sendTweet(data):
    # get tweet text
    json_data_file = json.loads(data)
    tweet = json_data_file["text"]
    print tweet
    # producer send tweets to kafka consumer
    t = tweet.encode('utf-8')
    producer.send('test', t)

def main():
    # Set up API connection info
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    i = 0
    while i < 1:
        try:
            # connect to Twitter API and get tweet
            twitterStream = Stream(auth, TweetListener())
            twitterStream.filter(track="car")
            i = i + 1
        except:
            # print("Print restart")
            # traceback.print_exc(file=sys.stdout)
            i = i + 1
            continue


if __name__ == '__main__':
    main()