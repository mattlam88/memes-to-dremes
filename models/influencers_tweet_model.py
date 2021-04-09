import sqlite3

class InfluencersTweetDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        pass

class InfluencersTweet:
    def __init__(self, id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentimenet_score):
        self._id = id
        self._influencer_twitter_acc = influencer_twitter_acc
        self._tweet_ID = tweet_ID
        self._tweet_text = tweet_text
        self._tweet_date_time = tweet_date_time
        self._crypto_ticker = crypto_ticker
        self._sentimenet_score = sentimenet_score
