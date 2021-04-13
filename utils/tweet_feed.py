import tweepy as tp
from datetime import *

from typing import Tuple


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to capture tweets from the Twitter API.
    """

    def __init__(self, api, controller, influencers):
        super().__init__(api)

        self._controller = controller
        self._influencers = influencers

    @property
    def controller(self):
        return self._controller

    @property
    def influencers(self):
        return self._influencers

    def on_status(self, status):
        """
        A tweet object contains an id_str value which represents the user ID of the tweeting user. Checks if the tweet
        is from one of the users in the list of influencers and then adds the tweet to the db.
        """
        if status.user.id_str not in self.influencers:
            return
        
        # TODO: Figure out how we want to return this information for integration into db

        self.controller.addTweet(status._json)

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False


class TwitterChannel:
    """
    Class is used to fetch historic twitter feed data
    """
    def __init__(self, api):
        self._api = api

    @property
    def api(self):
        return self._api

    def get_user_info(self, twitter_handle: str) -> Tuple[str, str, str]:
        user = self.api.get_user(twitter_handle)
        user_id: str = user.id_str
        name: str = user.name
        account: str = user.screen_name

        return user_id, name, account

    def get_user_tweets(self, username):
        start_date = datetime(2021, 3, 26, 0, 0, 0, 0)

        tweets = []

        for status in tp.Cursor(self.api.user_timeline, id=username, include_retweets=False).items():

            if status.created_at > start_date:
                if status.in_reply_to_status_id is None:
                    tweets.append(status._json)
                elif status.in_reply_to_screen_name == username and status.user.screen_name == username:
                    tweets.append(status._json)
            else:
                break

        return tweets


def username_to_id(username):
    """
    Takes a username and uses the Twitter API to return their corresponding ID numbers
    """
    username_obj = tp.api.get_user(username)
    user_id = username_obj.id_str
    return user_id
