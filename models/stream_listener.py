import tweepy as tp


class StreamListener(tp.StreamListener):
    """
    Creates a StreamListener object which Tweepy uses to
    """

    controller = None

    def on_status(self, status):
        self.controller.addTweet(status.text)

    def on_error(self, status_code):
        """
        A 420 status code is issued if you get rate limited. This will just have the program return False if we
        hit our rate limit.
        """
        if status_code == 420:
            return False
