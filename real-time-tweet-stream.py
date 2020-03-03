import tweepy
import numpy as np
import pandas as pd
from textblob import TextBlob
import re
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot
import sys

# consumer key & secret
CONSUMER_KEY = "t2EGDozPRRXDoa2rYtQkXnWYw"
CONSUMER_SECRET = "L3EyOsXiM0I6SLePDWf9sjU1dNyVogjHgoDjx8Qmqdl6PCpPTO"

# access token
ACCESS_TOKEN = "3881605529-EmvIVAo28rkuMmmjPo70rJf2Y7aVXbg86Rh6Ts8"
ACCESS_TOKEN_SECRET = "GjcA5iXvPFnYsd0ElU5NhSFoLcryBYD37ELL8DsYdVm7E"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#for tweet in api.search('food',count = 100):
#    print(tweet.text)

df = pd.DataFrame(columns = ['Tweets', 'User', 'User_statuses_count', 
                             'user_followers', 'User_location', 'User_verified',
                             'fav_count', 'rt_count', 'tweet_date'])
							 
def stream(data, file_name):

    i = 0

    for tweet in tweepy.Cursor(api.search, q=data, count=100, lang='en',tweet_mode='extended').items():

        print(i, end='\r')

        df.loc[i, 'Tweets'] = tweet.full_text

        df.loc[i, 'User'] = tweet.user.name

        df.loc[i, 'User_statuses_count'] = tweet.user.statuses_count

        df.loc[i, 'user_followers'] = tweet.user.followers_count

        df.loc[i, 'User_location'] = tweet.user.location

        df.loc[i, 'User_verified'] = tweet.user.verified

        df.loc[i, 'fav_count'] = tweet.favorite_count

        df.loc[i, 'rt_count'] = tweet.retweet_count

        df.loc[i, 'tweet_date'] = tweet.created_at

        df.to_csv('{}.csv'.format(file_name))
		
        df['clean_tweet'] = df['Tweets'].apply(lambda x: clean_tweet(x))
		
        df['Sentiment'] = df['clean_tweet'].apply(lambda x: analyze_sentiment(x))
        i+=1

        if i == 100:

            break

        else:

            pass
	
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())
	
	
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity ==0:
        return 'Neutral'
    else:
        return 'Negative'
		


stream(data = sys.argv[1:], file_name = 'my_tweets')
