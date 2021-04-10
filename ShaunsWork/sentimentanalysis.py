import json
import re

from textblob import TextBlob

from models.influencers_tweet_model import InfluencersTweetDAO


class SentimentAnalysis:
    def __init__(self):
        # add Influencers tweet model DAO instance
        self.influencers_tweet_model = InfluencersTweetDAO()
        pass
    
    def sentiment_buy_sell_analysis_agg(self):
        # pull data using DAO method
        # run a script to count the zeros and ones
        # buy or sell = ones / zeros and ones
        pass

    def sentiment_buy_sell_analysis_daily(self):
        # need the date of the tweets and the count of zeros and ones for each day
        # store information in JSON
        pass

    def get_tweet_sentiment(self, tweet) -> int:
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        tweetTxt = json.dumps(tweet)
        analysis = TextBlob(self.clean_tweet(tweetTxt))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return 0

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())