from typing import cast

from .base_controller import BaseController
from models.app_model import AppModel

from models.influencers_tweet_model import InfluencersTweet, InfluencersTweetDAO
from models.influencers_model import Influencers, InfluencersDAO
from models.crypto_ID_model import CryptoID, CryptoIDDAO

from ShaunsWork.sentimentanalysis import SentimentAnalysis

#function()
# static_method = InfluencersTweetDAO()
# When new tweet comes in static_method.add(elon, tweet id, text, date, crypto ticker, sentiment score)


class AppController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value

    def addInfluencer(self, value) -> None:
        # DAO instance, run add method    
        pass

    def updateTweetHistory(self) -> None:
        # get tweets from database
        # pass tweets to model
        pass

    def addTweet(self, tweet_data, crypto_ticker) -> None:
        # Create instance of DAO and object
        influencers_tweet_DAO = InfluencersTweetDAO()
        # run SentinmentAnalysis, score the tweet, append to tweet data
        sentiment_score = SentimentAnalysis.get_tweet_sentiment(tweet_data)
        # add tweet to database - running the DAO method to add to the database
        influencer_twitter_acc = tweet_data['user']['screen_name']
        tweet_ID = tweet_data['id']
        tweet_text = tweet_data['text']
        # convert tweet date-time to ISO-8601 format before adding to database
        tweet_date_time_list = tweet_data['created_at'].split()
        tweet_year = tweet_date_time_list[5]
        month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 
        'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        tweet_month = month_dict[tweet_date_time_list[1]]
        tweet_day = tweet_date_time_list[2]
        tweet_time = tweet_date_time_list[3]
        tweet_date_time = tweet_year + '-' + tweet_month + '-' + tweet_day + ' ' + tweet_time
        influencers_tweet_DAO.add_influencer_tweet(influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score)
        # pass tweet to model
        # manually trigger signal here
        model: AppModel = cast(AppModel, self.model)
        model.btnText = value


