from __future__ import annotations

from typing import cast, Any, Dict, Optional, Tuple, TYPE_CHECKING

from .base_controller import BaseController
from models.app_model import AppModel
from models.influencers_model import InfluencersDAO

if TYPE_CHECKING:
    from tweepy import Stream


class AppController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

        self._influencersDAO = InfluencersDAO()
        # TODO: add instance of twitter api class for making calls to api

        self._twitterStream = None

    @property
    def twitterStream(self) -> Stream:
        return self._twitterStream

    @twitterStream.setter
    def twitterStream(self, value) -> None:
        self._twitterStream = value

    @property
    def influencersDAO(self) -> InfluencersDAO:
        return self._influencersDAO

    def startStream(self) -> None:
        # TODO: get followers and filters
        self.twitterStream.filter(track=["bitcoin"], is_async=True)

    def restartStream(self) -> None:
        self.twitterStream.disconnect()
        self.startStream()

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value

    def addInfluencer(self, twitterHandle: str) -> None:
        userID, name, account = self._getUserData(twitterHandle)

        # TODO: use updated method that takes in userID as well.
        self.influencersDAO.add_influencer(name, account)

        rawTweets: List[Dict[str, Any]] = self._getUserTweets(twitterHandle)

        # TODO: figure out return type of sentiment analysis method
        tweets = self._performSentimentAnalysis(rawTweets)

        # TODO: insert results into database
        for tweet in tweets:
            self._addTweet(tweet)

    # TODO: use class for api calls to retrieve user data.
    def _getUserData(self, twitterHandle: str) -> Tuple[str, str, str]:
        pass

    # TODO: use class for api calls to retrieve user tweet history.
    def _getUserTweets(self, twitterHandle: str) -> List[Dict[str, Any]]:
        pass

    # TODO: use class for sentiment analysis to perform analysis on tweets.
    def _performSentimentAnalysis(self, tweets: List[Dict[str, Any]]):
        pass

    def _addTweet(self, tweet):
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

    """
    SCENARIO:
    
    App started for first time:
        Start UI but with no information.
        
    User add an influencer to follow:
        Get influencer data from twitter.
        Add influencer to database.
        Get historic data from twitter.
        Perform sentiment analysis on historic data.
        Add results to database.
        Add influencer to list of users for streamer to follow.
        Update UI with new data.
    """