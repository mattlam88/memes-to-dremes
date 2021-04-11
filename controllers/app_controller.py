from __future__ import annotations

import os
import re
import time
from typing import cast, Any, Dict, Optional, Tuple

from PySide2.QtCore import QSettings
import tweepy as tp
from tweepy import API, Stream

from .base_controller import BaseController
from models.app_model import AppModel
from models.influencers_tweet_model import InfluencersTweetDAO
from models.influencers_model import InfluencersDAO

from utils.crypto_coin import CryptoCoin
from utils.sentimentanalysis import SentimentAnalysis
from utils.tweet_feed import TwitterChannel


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
    TWO_WEEKS = 1209600000 # two weeks of time in milliseconds

    def __init__(self, model) -> None:
        super().__init__(model)

        self._api = None
        self._sentimentAnalysis = SentimentAnalysis()
        self._twitterStream: Stream = Optional[Stream]
        self._settings: QSettings = QSettings("MemesToDremes", "App")

        self._configureApi()
        self._twitterChannel: TwitterChannel = TwitterChannel(self.api)

    """
    WORKFLOWS:

    1. User adds new influencer to follow.
    2. User removes influencer from following.
    3. Influencer makes a tweet.
    4. User reopens app after closing it.
    """

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

    def _configureApi(self) -> None:
        API_KEY: str = self.settings.value("API_KEY", '')
        API_SECRET: str = self.settings.value("API_SECRET", '')
        ACCESS_TOKEN: str = self.settings.value("ACCESS_TOKEN", '')
        ACCESS_TOKEN_SECRET: str = self.settings.value("ACCESS_TOKEN_SECRET", '')

        auth = tp.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tp.API(auth)

    def unFollowInfluencer(self, twitterHandle: str) -> None:
        if not self._dbExists():
            return

        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        influencersDAO.unfollow_influencer(twitterHandle)
        cast(AppModel, self.model).unFollowInfluencer(twitterHandle)

    def followInfluencer(self, twitterHandle: str) -> None:
        """
        Adds a new influencer to the local database, pulls their tweets, updates sentiment scores, and updates UI.

        :param twitterHandle: The influencer's twitter handle.
        """

        if not self._dbExists():
            return

        # Step 1: Get influencer data from twitter.
        userID, name, account = self._getUserData(twitterHandle)

        # Step 2: Add influencer to database.
        influencersDAO: InfluencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
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

    # TODO: use class for api calls to retrieve user data.
    def _getUserData(self, twitterHandle: str) -> Tuple[str, str, str]:
        return self.twitterChannel.get_user_info(twitterHandle)

    # TODO: use class for api calls to retrieve user tweet history.
    def _getUserTweets(self, twitterHandle: str) -> List[Dict[str, Any]]:
        return self.twitterChannel.get_user_tweets(twitterHandle)

    def addTweet(self, tweetStatus) -> None:
        if not self._dbExists():
            return

        # run SentimentAnalysis, score the tweet, append to tweet data
        sentimentScore: int = self._scoreTweet(tweetStatus)

        # add tweet to database - running the DAO method to add to the database
        screenName: str = tweetStatus['user']['screen_name']
        tweetID: str = tweetStatus['id']
        tweetText: str = tweetStatus['text']
        createdAt: str = self._convertDate(tweetStatus['created_at'])

        # get crypto ticker from tweet
        cryptoTicker: str = self._extractTicker(tweetText)

        if cryptoTicker == '':
            return

        tweetDAO = InfluencersTweetDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        tweetDAO.add_influencer_tweet(
            screenName, tweetID, tweetText, createdAt, cryptoTicker, sentimentScore
        )

        # pass tweet to model
        # manually trigger signal here
        # TODO: find a way to update model with data so it works and triggers UI update.
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

    def _convertDate(self, date: str) -> str:
        dateComponents: list[str] = date.split()
        year: str = dateComponents[5]
        month: str = self.MONTH_MAP[dateComponents[1]]
        day: str = dateComponents[2]
        time: str = dateComponents[3]

        return year + '-' + month + '-' + day + ' ' + time

    def _extractTicker(self, tweetStatus) -> str:
        txt = tweetStatus
        bitcoin_finder = re.search('bitcoin|Bitcoin|BITCOIN|btc|BTC', txt)

        if bitcoin_finder is None:
            return str()

        # if bitcoin is contained in the tweet it will return out the string "BTC"
        return 'BTC'

    def updateTweetHistory(self) -> None:
        if not self._dbExists():
            return

        # get tweets from database
        tweets = list()
        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", '')) # initiates DAO instance
        influencers_tweets = InfluencersTweetDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))

        # get influencers from db
        influencers = influencersDAO.get_influencers()

        # TODO: will need check who is being followed and then do a of tweets on those individuals
        for person in influencers:
            if not person.following_influencer:
                continue

            # add influencer to following
            cast(AppModel, self.model).followInfluencer(person.influencer_twitter_acc)

            # For each individual the person is followed and then pulls their tweet history in the database
            # influencersDAO.follow_influencer(person)
            _tweets = influencers_tweets.get_all_influencer_tweets(person.influencer_twitter_acc)
            influencerTweets = influencers_tweets.get_all_influencer_tweets(person.influencer_twitter_acc)

            for influencerTweet in influencerTweets:
                tweets.append(influencerTweet.to_dict())

        # pass tweets to model
        for tweet in tweets:
            cast(AppModel, self.model).addTweet(tweet)

    def startStream(self) -> None:
        if not self._dbExists():
            return

        self.twitterStream.influencers = self.getInfluencerIds()
        self.twitterStream.filter(track=self._getCryptoKeywords(), follow=self.getInfluencerIds(), is_async=True)

    def restartStream(self) -> None:
        self.twitterStream.disconnect()
        self.startStream()

    # TODO: get followers and filters
    def _getCryptoKeywords(self) -> List[str]:
        keywords = ["bitcoin", "btc"]
        return keywords

    def _dbExists(self) -> bool:
        dbPath: str = os.path.join(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        return os.path.isfile(dbPath)

    def getInfluencerIds(self) -> List[str]:
        if not self._dbExists():
            return list()

        influencersDAO = InfluencersDAO(self.settings.value("DB_PATH", ''), self.settings.value("DB_NAME", ''))
        influencers = influencersDAO.get_influencers()

        return [influencer.influencer_user_id for influencer in influencers if influencer.following_influencer]

    def tearDown(self) -> None:
        self.twitterStream.disconnect()

    def updatePrice(self) -> None:
        '''
        Calls crypto coin API at regular interval and updates model
        '''
        model: AppModel = cast(AppModel, self.model)
        cryptocoin = CryptoCoin("bitcoin", "btc")
        end = time.time()*1000
        start = end - self.TWO_WEEKS
        model.cryptoPriceHistory = cryptocoin.get_historic_pricing(start_date= start, end_date = end)
