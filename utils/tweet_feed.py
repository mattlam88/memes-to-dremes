import tweepy as tp
import settings
from datetime import *

from typing import Tuple

# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(settings.API_KEY, settings.API_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tp.API(auth)


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to capture tweets from the Twitter API.
    """

    controller = None
    influencers = list()

    def on_status(self, status):
        """
        A tweet object contains an id_str value which represents the user ID of the tweeting user. Checks if the tweet
        is from one of the users in the list of influencers and then adds the tweet to the db.
        """
        if status.user.id_str not in self.influencers:
            return
        print(status.text)
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
    auth = tp.OAuthHandler(settings.API_KEY, settings.API_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    api = tp.API(auth)

    def get_user_info(self, twitter_handle: str) -> Tuple[str, str, str]:
        user = self.api.get_user(twitter_handle)
        user_id: str = user.id_str
        name: str = user.name
        account: str = user.screen_name

        return user_id, name, account

    def get_user_tweets(self, username):
        start_date = datetime(2021, 3, 26, 0, 0, 0, 0)

        tweets = []

        for status in tp.Cursor(api.user_timeline, id=username, include_retweets=False).items():

            if status.created_at > start_date:

                if status.in_reply_to_status_id is None:
                    print("date time is:", status.created_at)
                    print("tweet is: ", status.text)
                    tweets.append(status._json)
                elif status.in_reply_to_screen_name == username and status.user.screen_name == username:
                    print("date time is:", status.created_at)
                    print("tweet is: ", status.text)
                    tweets.append(status._json)

        return tweets


def username_to_id(username):
    """
    Takes a username and uses the Twitter API to return their corresponding ID numbers
    """
    username_obj = tp.api.get_user(username)
    user_id = username_obj.id_str
    return user_id

"""
# Usernames and keyword will need to be supplied from the user somewhere, these are placeholders
keywords = ["bitcoin", "btc"]
influencers = ["1309965256286973955"]

# Used to test historic tweet grabs
historic_tweets = TwitterChannel()
print(historic_tweets.get_user_tweets("elonmusk"))

# Code initiates the stream
stream_listener = StreamListener()
stream = tp.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords, follow=influencers)
"""