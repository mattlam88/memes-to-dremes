from __future__ import annotations

from typing import cast, Any, Dict, Optional, Tuple, TYPE_CHECKING

from .base_controller import BaseController
from models.app_model import AppModel
from models.influencers_model import InfluencersDAO
from tweepy import Stream


class AppController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

        self._influencersDAO = InfluencersDAO()
        # TODO: add instance of twitter api class for making calls to api

        self._twitterStream: Stream = Optional[Stream]

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
        keywords = ["bitcoin", "btc"]
        influencers = ["1309965256286973955"]
        self.twitterStream.influencers = influencers
        self.twitterStream.filter(track=keywords, follow=influencers, is_async=True)

    def restartStream(self) -> None:
        self.twitterStream.disconnect()
        self.startStream()

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value

    def addInfluencer(self, twitterHandle: str) -> None:
        # Step 1: Get influencer data from twitter.
        userID, name, account = self._getUserData(twitterHandle)

        # Step 2: Add influencer to database.
        # TODO: use updated method that takes in userID as well.
        self.influencersDAO.add_influencer(name, account)

        # Step 3: Get historic tweets for influencer.
        rawTweets: List[Dict[str, Any]] = self._getUserTweets(twitterHandle)

        # Step 4: Perform sentiment analysis on historic data.
        # TODO: figure out return type of sentiment analysis method
        tweets = self._performSentimentAnalysis(rawTweets)

        # Step 5: Add tweets to database alongside their sentiment score.
        # TODO: insert results into database
        for tweet in tweets:
            self.addTweet(tweet)

        # TODO: automatically update influencer / coin lists
        # Step 6: Restart streamer so it picks up new influencer to follow.
        self.restartStream()

        # TODO: find a way to update model with data so it works and triggers UI update.
        # Step 7: Update UI with new data
        cast(AppModel, self.model).tweetHistory = tweets

    # TODO: use class for api calls to retrieve user data.
    def _getUserData(self, twitterHandle: str) -> Tuple[str, str, str]:
        pass

    # TODO: use class for api calls to retrieve user tweet history.
    def _getUserTweets(self, twitterHandle: str) -> List[Dict[str, Any]]:
        pass

    # TODO: use class for sentiment analysis to perform analysis on tweets.
    def _performSentimentAnalysis(self, tweets: List[Dict[str, Any]]):
        pass

    def updateTweetHistory(self) -> None:
        # get tweets from database
        # pass tweets to model
        pass

    def addTweet(self, value) -> None:
        model: AppModel = cast(AppModel, self.model)
        model.btnText = value
