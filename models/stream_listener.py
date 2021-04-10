import tweepy as tp


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to
    """

    controller = None
    influencers = list()

    def on_status(self, status):
        """
        if status.user.id_str not in self.influencers:
            return
        """

        self.controller.addTweet(status._json, '')

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False
