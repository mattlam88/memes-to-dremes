import tweepy as tp
import settings

# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(settings.API_KEY, settings.API_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tp.API(auth)


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
        return status

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False

class TwitterChannel():
    pass


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
stream_listener = StreamListener()
stream = tp.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords, follow=influencers)