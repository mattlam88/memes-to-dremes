import tweepy as tp

# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(config.API_KEY, config.API_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tp.API(auth)

#username = input()
#user_id = tp.API.get_user(username)


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to
    """

    def on_status(self, status):
        """
        A tweet object contains an id_str value which represents the user ID of the tweeting user. Checks if the tweet
        is from one of the users in the list of influencers and then adds the tweet to the db.
        """
        if status.user.id_str not in influencers:
            return
        print(status.text)

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False


keywords = ["bitcoin", "btc"]
influencers = ["1309965256286973955"]
stream_listener = StreamListener()
stream = tp.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords, follow=influencers)