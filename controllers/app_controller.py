from typing import cast

from .base_controller import BaseController
from models.app_model import AppModel

from models.influencers_tweet_model import InfluencersTweet, InfluencersTweetDAO
from models.influencers_model import Influencers, InfluencersDAO
from models.crypto_ID_model import CryptoID, CryptoIDDAO
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

    def addTweet(self, value) -> None:
        # Create instance of DAO and object
        # run SentinmentAnalysis, score the tweet
        # add tweet to database - running the DAO method to add to the database
        # pass tweet to model
        # manually trigger signal here
        model: AppModel = cast(AppModel, self.model)
        model.btnText = value


class SentimentAnalysis:
    def __init__(self):
        # add Influencers tweet model DAO instance
        pass

    def sentimenet_scorer(self):
        # create logic that would score each tweet with 1 or 0
        pass
    
    def sentimenet_buy_sell_analysis(self):
        # pull data using DAO method
        # run a script to count the zeros and ones
        # buy or sell = ones / zeros and ones
        pass

    def sentimenet_buy_sell_analysis_weekly(self):
        # need the date of the tweets and the count of zeros and ones for each day
        # store information in JSON
        pass
