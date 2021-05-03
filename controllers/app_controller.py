from __future__ import annotations

from datetime import datetime, timedelta
from functools import wraps
import os
import re
from typing import cast, Any, Dict, Optional, Tuple

from PySide2.QtCore import QSettings, QThread
import tweepy as tp
from tweepy import API, Stream

from .base_controller import BaseController
from models import AppModel, InfluencersDAO, InfluencersTweetDAO
from utils import CoinGeckoWorker, Converter, SentimentAnalysis, TwitterChannel


class AppController(BaseController):
    # region Properties

    @property
    def api(self) -> API:
        return self._api

    @api.setter
    def api(self, value: API) -> None:
        self._api = value

    @property
    def twitterStream(self) -> Stream:
        return self._twitterStream

    @twitterStream.setter
    def twitterStream(self, value) -> None:
        self._twitterStream = value

    @property
    def sentimentAnalysis(self) -> SentimentAnalysis:
        return self._sentimentAnalysis

    @property
    def twitterChannel(self) -> TwitterChannel:
        return self._twitterChannel

    @property
    def settings(self) -> QSettings:
        return self._settings

    # endregion

    # region Constructor

    def __init__(self, model) -> None:
        super().__init__(model)

        self._api = None
        self._sentimentAnalysis = SentimentAnalysis()
        self._twitterStream: Stream = Optional[Stream]
        self._settings: QSettings = QSettings("MemesToDremes", "App")

        self._configureApi()
        self._twitterChannel: TwitterChannel = TwitterChannel(self.api)

    def _configureApi(self) -> None:
        API_KEY: str = self.settings.value("API_KEY", '')
        API_SECRET: str = self.settings.value("API_SECRET", '')
        ACCESS_TOKEN: str = self.settings.value("ACCESS_TOKEN", '')
        ACCESS_TOKEN_SECRET: str = self.settings.value("ACCESS_TOKEN_SECRET", '')

        auth = tp.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tp.API(auth)

    # endregion

    def _dbContext(func):
        """Checks if database exists before calling wrapped method."""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._dbExists():
                return func(self, *args, **kwargs)
        return wrapper

    @_dbContext
    def followInfluencer(self, twitterHandle: str) -> None:
        """
        Adds a new influencer to the local database, pulls their tweets, updates sentiment scores, and updates UI.

        :param twitterHandle: The influencer's twitter handle.
        """

        # Step 1: Get influencer data from twitter.
        userID, name, account = self._getUserData(twitterHandle)

        # Step 2: Add influencer to database.
        influencersDAO: InfluencersDAO = InfluencersDAO(
            self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", '')
        )
        influencersDAO.add_influencer(userID, name, account, True)

        # Step 3: Get historic tweets for influencer.
        rawTweets: List[Dict[str, Any]] = self._getUserTweets(twitterHandle)

        # Step 4: Perform sentiment analysis on historic data and add scores to db.
        for tweet in rawTweets:
            self.addTweet(tweet)

        # Step 5: Update app model to include influencer
        cast(AppModel, self.model).followInfluencer(twitterHandle)

        # Step 6: Restart streamer so it picks up new influencer to follow.
        self.restartStream()

    @_dbContext
    def unFollowInfluencer(self, twitterHandle: str) -> None:
        """
        Given an influencer's twitter handle, signals app to stop requesting tweets from influencer, and updates UI to
        remove the influencer's tweets and data.

        :param twitterHandle: The influencer's twitter handle.
        """

        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        influencersDAO.unfollow_influencer(twitterHandle)
        cast(AppModel, self.model).unFollowInfluencer(twitterHandle)

    def _getUserData(self, twitterHandle: str) -> Tuple[str, str, str]:
        return self.twitterChannel.get_user_info(twitterHandle)

    def _getUserTweets(self, twitterHandle: str) -> List[Dict[str, Any]]:
        return self.twitterChannel.get_user_tweets(twitterHandle, datetime.today() - timedelta(days=7))

    @_dbContext
    def addTweet(self, tweetStatus) -> None:
        # run SentimentAnalysis, score the tweet, append to tweet data
        sentimentScore: int = self._scoreTweet(tweetStatus)

        # add tweet to database - running the DAO method to add to the database
        screenName: str = tweetStatus['user']['screen_name']
        tweetID: str = tweetStatus['id']
        tweetText: str = tweetStatus['text']
        createdAt: str = Converter.convertDate(tweetStatus['created_at'])

        # get crypto ticker from tweet
        cryptoTicker: str = self._extractTicker(tweetText)

        if cryptoTicker == '':
            return

        tweetDAO = InfluencersTweetDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        tweetDAO.add_influencer_tweet(
            screenName, tweetID, tweetText, createdAt, cryptoTicker, sentimentScore
        )

        tweet = {
            "screenName": screenName,
            "tweetID": tweetID,
            "tweetText": tweetText,
            "createdAt": createdAt,
            "cryptoTicker": cryptoTicker,
            "sentimentScore": sentimentScore
        }
        model: AppModel = cast(AppModel, self.model)
        model.addTweet(tweet)

    def _scoreTweet(self, tweetStatus: Dict[str, Any]) -> int:
        return self.sentimentAnalysis.get_tweet_sentiment(tweetStatus)

    # TODO: Use search keywords from a database or other external source.
    def _extractTicker(self, tweetStatus) -> str:
        txt = tweetStatus
        bitcoin_finder = re.search('bitcoin|Bitcoin|BITCOIN|btc|BTC', txt)

        if bitcoin_finder is None:
            return str()

        # if bitcoin is contained in the tweet it will return out the string "BTC"
        return 'BTC'

    @_dbContext
    def startStream(self) -> None:
        self.twitterStream.influencers = self._getInfluencerIDs()
        self.twitterStream.filter(
            track=self._getCryptoKeywords(), follow=self._getInfluencerIDs() or list(), is_async=True
        )

    def restartStream(self) -> None:
        self.twitterStream.disconnect()
        self.startStream()

    # TODO: pull keywords from database or other source.
    def _getCryptoKeywords(self) -> List[str]:
        keywords = ["bitcoin", "btc"]
        return keywords

    def _dbExists(self) -> bool:
        dbPath: str = os.path.join(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        return os.path.isfile(dbPath)

    @_dbContext
    def _getInfluencerIDs(self) -> List[str]:
        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        influencers = influencersDAO.get_influencers()

        return [influencer.influencer_user_id for influencer in influencers if influencer.following_influencer]

    @_dbContext
    def updateTweetHistory(self) -> None:
        # get tweets from database
        tweets = list()
        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        influencers_tweets = InfluencersTweetDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))

        # get influencers from db
        influencers = influencersDAO.get_influencers()

        for person in influencers:
            if not person.following_influencer:
                continue

            # add influencer to following
            cast(AppModel, self.model).followInfluencer(person.influencer_twitter_acc)

            # For each individual the person is followed and then pulls their tweet history in the database
            _tweets = influencers_tweets.get_all_influencer_tweets(person.influencer_twitter_acc)
            influencerTweets = influencers_tweets.get_all_influencer_tweets(person.influencer_twitter_acc)

            for influencerTweet in influencerTweets:
                tweets.append(influencerTweet.to_dict())

        # pass tweets to model
        cast(AppModel, self.model).tweetHistory = tweets

    def computeAggregateScore(self, date: datetime) -> None:
        tweetDAO = InfluencersTweetDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        scores: Dict[int, int] = tweetDAO.get_daily_sentiment_score(
            {"year": str(date.year), "month": str(date.month).zfill(2), "day": str(date.day).zfill(2)}
        )

        model: AppModel = cast(AppModel, self.model)
        model.aggregateScore = scores.get(1, 0), scores.get(0, 0)

    @_dbContext
    def updatePrice(self) -> None:
        """
        Calls crypto coin API at regular interval and updates model
        """

        # TODO: extract these variables outside so they can be passed in via calling method / some other source.
        name: str = "bitcoin"
        ticker: str = "btc"
        endDate: datetime = datetime.today()
        startDate: datetime = endDate - timedelta(days=14)

        self.thread = QThread()
        self.worker = CoinGeckoWorker(self.model)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.run(name, ticker, startDate, endDate))
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def tearDown(self) -> None:
        self.twitterStream.disconnect()
