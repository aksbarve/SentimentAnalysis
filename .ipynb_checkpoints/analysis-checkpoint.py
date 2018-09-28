import tweepy
from textblob import TextBlob
import sys
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# query = "call of duty battle royale"
#
# tweets = api.search(
#     lang="en",
#     q=query,
#     count=100
# )
#
# for tweet in tweets[:100]:
#     print(tweet.id, tweet.text)
#
# data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
#
# display(data.head(100))
#
# data['len'] = np.array([len(tweet.text) for tweet in tweets])
# data['ID'] = np.array([tweet.id for tweet in tweets])
# data['Date'] = np.array([tweet.created_at for tweet in tweets])
# data['Source'] = np.array([tweet.source for tweet in tweets])
# data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
# data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
#
# display(data.head(100))
#
# mean = np.mean(data['len'])
#
# print("The lenght's average in tweets: {}".format(mean))
#
# fav_max = np.max(data['Likes'])
# rt_max = np.max(data['RTs'])


searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms = int(input("Enter how many tweets to search: "))

tweets = tweepy.Cursor(api.search, q=searchTerm, lang='en').items(NoOfTerms)

for tweet in tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
for tweet in tweets:
    print (tweet.text.translate(non_bmp_map))
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)



