from __future__ import annotations

import re
import time
from typing import cast, Any, Dict, Optional, Tuple

from tweepy import Stream

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

        self._sentimentAnalysis = SentimentAnalysis()
        self._twitterStream: Stream = Optional[Stream]
        self._twitterChannel: TwitterChannel = TwitterChannel()

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

    @property
    def twitterChannel(self) -> TwitterChannel:
        return self._twitterChannel

    def unFollowInfluencer(self, twitterHandle: str) -> None:
        influencersDAO = InfluencersDAO()
        influencersDAO.unfollow_influencer(twitterHandle)
        cast(AppModel, self.model).unFollowInfluencer(twitterHandle)

    def followInfluencer(self, twitterHandle: str) -> None:
        """
        Adds a new influencer to the local database, pulls their tweets, updates sentiment scores, and updates UI.

        :param twitterHandle: The influencer's twitter handle.
        """

        # Step 1: Get influencer data from twitter.
        userID, name, account = self._getUserData(twitterHandle)

        # Step 2: Add influencer to database.
        influencersDAO: InfluencersDAO = InfluencersDAO()
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

        tweetDAO = InfluencersTweetDAO()
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
        # get tweets from database
        tweets = list()
        influencersDAO = InfluencersDAO() # initiates DAO instance
        influencers_tweets = InfluencersTweetDAO()

        # get influencers from db
        influencers = influencersDAO.get_influencers()

        # TODO: will need check who is being followed and then do a of tweets on those individuals
        for person in influencers:
            if not person.following_influencer:
                continue

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
        influencersDAO = InfluencersDAO()
        influencers = influencersDAO.get_influencers()

        return [influencer.influencer_user_id for influencer in influencers if influencer.following_influencer]

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value

    def updatePrice(self) -> None:
        '''
        Calls crypto coin API at regular interval and updates model
        '''
        model: AppModel = cast(AppModel, self.model)
        cryptocoin = CryptoCoin("bitcoin", "btc")
        end = time.time()*1000
        start = now - TWO_WEEKS
        model.cryptopriceHistory = cryptocoin.get_historic_pricing(start_date= start, end_date = end)

    