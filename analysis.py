import tweepy
import sys
from credentials import *
import pandas as pd
import numpy as np
import pylab
from IPython.display import display
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

# OAuth for tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
NoOfTerms = 0

searchTerm = input("Enter Keyword/Tag to search for your game:")
while NoOfTerms < 100:
    NoOfTerms = int(input("Okay how many tweets you want to search (Try 100 for a good sentiment analysis): "))

tweets = tweepy.Cursor(api.search, q=searchTerm, lang='en').items(NoOfTerms)

for tweet in tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
for tweet in tweets:
    print(tweet.text.translate(non_bmp_map))
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)

tweets = api.search(
    lang="en",
    q=searchTerm,
    count=NoOfTerms
)

# Create Data Frame

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
display(data.head(100))

data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

# Show some interesting information of game
# We extract the mean of length using numpy on data frame:

mean = np.mean(data['len'])

print("The length's average in tweets: {}".format(mean))

fav_max = np.max(data['Likes'])
rt_max = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt = data[data.RTs == rt_max].index[0]

# Max FAVs:
print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))

# Max RTs:
print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))

# Create graph for the above data:

time_len = pd.Series(data=data['len'].values, index=data['Date'])
time_fav = pd.Series(data=data['Likes'].values, index=data['Date'])
time_ret = pd.Series(data=data['RTs'].values, index=data['Date'])

time_len.plot(figsize=(16, 4), label="Length", color='r', legend=True)
time_fav.plot(figsize=(16, 4), label="Likes", color='g', legend=True)
time_ret.plot(figsize=(16, 4), label="Retweets", color='b', legend=True)
pylab.ylabel("Count")
pylab.title("Graph Information")
pylab.show()

