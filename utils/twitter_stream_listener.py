import tweepy as tp


class TwitterStreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to capture tweets from the Twitter API.
    """

    # region Properties

    @property
    def controller(self):
        return self._controller

    @property
    def influencers(self):
        return self._influencers

    # endregion

    # region Constructor

    def __init__(self, api, controller, influencers):
        super().__init__(api)

        self._controller = controller
        self._influencers = influencers

    # endregion

    def on_status(self, status):
        """
        A tweet object contains an id_str value which represents the user ID of the tweeting user. Checks if the tweet
        is from one of the users in the list of influencers and then adds the tweet to the db.
        """

        if status.user.id_str not in self.influencers:
            return

        self.controller.addTweet(status._json)

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """

        if status_code == 420:
            return False
