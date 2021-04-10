from __future__ import annotations

from typing import cast, Any, Dict, Optional, Tuple

from tweepy import Stream

from .base_controller import BaseController
from models.app_model import AppModel
from models.influencers_tweet_model import InfluencersTweetDAO
from models.influencers_model import InfluencersDAO
from ShaunsWork.sentimentanalysis import SentimentAnalysis


class AppController(BaseController):
    MONTH_MAP = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    def __init__(self, model) -> None:
        super().__init__(model)

        self._sentimentAnalysis = SentimentAnalysis()
        # TODO: add instance of twitter api class for making calls to api

        self._twitterStream: Stream = Optional[Stream]

    """
    WORKFLOWS:
    
    1. User adds new influencer to follow.
    2. User removes influencer from following.
    3. Influencer makes a tweet.
    4. User reopens app after closing it.
    """

    @property
    def twitterStream(self) -> Stream:
        return self._twitterStream

    @twitterStream.setter
    def twitterStream(self, value) -> None:
        self._twitterStream = value

    @property
    def sentimentAnalysis(self) -> SentimentAnalysis:
        return self._sentimentAnalysis

    def addInfluencer(self, twitterHandle: str) -> None:
        """
        Adds a new influencer to the local database, pulls their tweets, updates sentiment scores, and updates UI.
        
        :param twitterHandle: The influencer's twitter handle.
        """
        
        # Step 1: Get influencer data from twitter.
        userID, name, account = self._getUserData(twitterHandle)

        # Step 2: Add influencer to database.
        influencersDAO: InfluencersDAO = InfluencersDAO()
        influencersDAO.add_influencer(userID, name, account)

        # Step 3: Get historic tweets for influencer.
        rawTweets: List[Dict[str, Any]] = self._getUserTweets(twitterHandle)

        # Step 4: Perform sentiment analysis on historic data and add scores to db.
        for tweet in rawTweets:
            self.addTweet(tweet)

        # Step 5: Restart streamer so it picks up new influencer to follow.
        self.restartStream()

    # TODO: use class for api calls to retrieve user data.
    def _getUserData(self, twitterHandle: str) -> Tuple[str, str, str]:
        pass

    # TODO: use class for api calls to retrieve user tweet history.
    def _getUserTweets(self, twitterHandle: str) -> List[Dict[str, Any]]:
        pass

    def addTweet(self, tweetStatus) -> None:
        # run SentimentAnalysis, score the tweet, append to tweet data
        sentimentScore: int = self._scoreTweet(tweetStatus)

        # add tweet to database - running the DAO method to add to the database
        screenName: str = tweetStatus['user']['screen_name']
        tweetID: str = tweetStatus['id']
        tweetText: str = tweetStatus['text']
        createdAt: str = self._convertDate(tweetStatus['created_at'])
        
        # get crypto ticker from tweet
        cryptoTicker: str = self._extractTicker(tweetStatus)
        
        if cryptoTicker is None:
            cryptoTicker = ''

        tweetDAO = InfluencersTweetDAO()
        tweetDAO.add_influencer_tweet(
            screenName, tweetID, tweetText, createdAt, cryptoTicker, sentimentScore
        )
        
        # pass tweet to model
        # manually trigger signal here
        # TODO: find a way to update model with data so it works and triggers UI update.
        model: AppModel = cast(AppModel, self.model)
        model.btnText = str(sentimentScore)

    def _scoreTweet(self, tweetStatus: Dict[str, Any]) -> int:
        return self.sentimentAnalysis.get_tweet_sentiment(tweetStatus)

    def _convertDate(self, date: str) -> str:
        dateComponents: list[str] = date.split()
        year: str = dateComponents[5]

        month: str = self.MONTH_MAP[dateComponents[1]]
        day: str = dateComponents[2]
        time: str = dateComponents[3]
        
        return year + '-' + month + '-' + day + ' ' + time 

    def _extractTicker(self, tweetStatus) -> str:
        pass

    def removeInfluencer(self, twitterHandle: str) -> None:
        pass

    def updateTweetHistory(self) -> None:
        # get tweets from database
        # pass tweets to model
        pass

    def startStream(self) -> None:
        self.twitterStream.influencers = self._getInfluencerIds()
        self.twitterStream.filter(track=self._getCryptoKeywords(), follow=self._getInfluencerIds(), is_async=True)

    def restartStream(self) -> None:
        self.twitterStream.disconnect()
        self.startStream()

    # TODO: get followers and filters
    def _getCryptoKeywords(self) -> List[str]:
        keywords = ["bitcoin", "btc"]
        return keywords

    def _getInfluencerIds(self) -> List[str]:
        influencers = ["1309965256286973955"]
        return influencers

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value
