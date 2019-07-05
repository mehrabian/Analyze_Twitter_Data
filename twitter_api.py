# Import package
import tweepy
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from sys import *

matplotlib.use('Agg')

stream_the_data = int(argv[1])
print(stream_the_data)

# Create a list of labels:cd
cd = ['Obama', 'trump', 'sanders', 'Iran']

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.txt", "w")

    def on_status(self, status):
        tweet = status._json
        self.file.write( json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        if self.num_tweets < 100:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)

def word_in_text(word, text):
    word = str(word).lower()
    text = str(tweet).lower()
    match = re.search(word, text)

    if match:
        return True
    return False

if(stream_the_data==1):
    # Store OAuth authentication credentials in relevant variables
    access_token = ""
    access_token_secret = ""
    consumer_key = ""
    consumer_secret = ""

    # Pass OAuth details to tweepy's OAuth handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    # Initialize Stream listener
    l = MyStreamListener()
    # Create your Stream object with authentication
    stream = tweepy.Stream(auth, l)
    # Filter Twitter Streams to capture data by the keywords:
    stream.filter(track =cd,languages = ["en"])

# String of path to file: tweets_data_path
tweets_data_path='tweets.txt'
# Initialize empty list to store tweets: tweets_data
tweets_data=[]

# Open connection to file
tweets_file = open(tweets_data_path, "r")

# Read in tweets and store in list: tweets_data
for line in tweets_file:
    tweet=json.loads(line)
    tweets_data.append(tweet)

# Close connection to file
tweets_file.close()

# Print the keys of the first tweet dict
print(tweets_data[0].keys())

# Build DataFrame of tweet texts and languages
df = pd.DataFrame(tweets_data, columns=['text','lang'])

# Print head of DataFrame
print(df.head(500))


# Initialize list to store tweet counts
[Obama, trump, sanders, Iran] = [0, 0, 0, 0]

# Iterate through df, counting the number of tweets in which
# each candidate is mentioned
for index, row in df.iterrows():
    Obama += word_in_text('obama', row['text'])
    trump += word_in_text('trump', row['text'])
    sanders += word_in_text('sanders', row['text'])
    Iran += word_in_text('Iran', row['text'])

print([Obama, trump, sanders, Iran])
# Set seaborn style
sns.set(color_codes=True)

# Plot histogram
ax = sns.barplot(cd, [Obama,trump,sanders,Iran])
ax.set(ylabel="count")
plt.savefig('histogram.png')
#plt.show()
