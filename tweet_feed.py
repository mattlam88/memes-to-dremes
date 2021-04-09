import config
import tweepy as tp

# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(config.API_KEY, config.API_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tp.API(auth)


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to
    """
    def on_status(self, status):

        print(status.text)

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tp.Stream(auth=api.auth, listener=stream_listener)
#stream.filter(follow=["1309965256286973955"])
stream.filter(track=["bitcoin", "btc"])