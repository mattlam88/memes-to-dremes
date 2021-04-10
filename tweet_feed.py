import tweepy as tp
import settings
import datetime

# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(settings.API_KEY, settings.API_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tp.API(auth)  # , wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to capture tweets from the Twitter API.
    """

    def on_status(self, status):
        """
        A tweet object contains an id_str value which represents the user ID of the tweeting user. Checks if the tweet
        is from one of the users in the list of influencers and then adds the tweet to the db.
        """
        if status.user.id_str not in influencers:
            return
        print(status.text)
        #return status

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

    def get_user_info(self):
        pass

    def get_user_tweets(self, username):
        start_date = datetime.datetime(2021, 3, 26, 0, 0, 0, 0)
        end_date = datetime.datetime(2021, 4, 9, 0, 0, 0, 0)

        tweets = []
        temp_tweets = api.user_timeline(username)
        for tweet in temp_tweets:
            print(tweet.created_at)
            #if tweet.created_at < end_date:
                #tweets.append(tweet)

        #while temp_tweets[-1].created_at > start_date:
        #    temp_tweets = api.user_timeline(username, max_id=temp_tweets[-1].id)
        #    for tweet in temp_tweets:
        #        if tweet.id not in tweets:
        #            if end_date > tweet.created_at > start_date:
        #                tweets.append(tweet)

        return tweets


def username_to_id(username):
    """
    Takes a username and uses the Twitter API to return their corresponding ID numbers
    """
    username_obj = tp.api.get_user(username)
    user_id = username_obj.id_str
    return user_id


usernames = {}
keywords = ["bitcoin", "btc"]
influencers = ["1309965256286973955"]

historic_elon = TwitterChannel()
print(historic_elon.get_user_tweets("elonmusk"))
"""
stream_listener = StreamListener()
stream = tp.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords, follow=influencers)
"""