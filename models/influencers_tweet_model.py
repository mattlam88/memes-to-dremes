import sqlite3

from settings import DB_PATH


class InfluencersTweetDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect(DB_PATH) # give the exact location of the database file
        self.cur = self.conn.cursor()
    
    def add_influencer_tweet(self, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score):
        self.cur.execute(
            """
            INSERT INTO influencer_tweets (
                influencer_twitter_acc,
                tweet_ID, 
                tweet_text, 
                tweet_date_time, 
                crypto_ticker, 
                sentiment_score
            ) 
            VALUES (?,?,?,?,?,?);
            """,
            (influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score)
        )
        self.conn.commit()

    def get_influencer_tweets(self, influencer_twitter_acc, crypto_ticker):
        all_influencer_tweets = []
        tweet_data = self.cur.execute(
            f"""
            SELECT id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score
            FROM influencer_tweets
            WHERE influencer_twitter_acc="{influencer_twitter_acc}" AND crypto_ticker="{crypto_ticker}";
            """
        )
        for data in tweet_data:
            all_influencer_tweets.append(InfluencersTweet(*data))

        return all_influencer_tweets


class InfluencersTweet:
    def __init__(self, id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score):
        self._id = id
        self._influencer_twitter_acc = influencer_twitter_acc
        self._tweet_ID = tweet_ID
        self._tweet_text = tweet_text
        self._tweet_date_time = tweet_date_time
        self._crypto_ticker = crypto_ticker
        self._sentiment_score = sentiment_score

    @property
    def id(self):
        return self._id

    @property
    def influencer_twitter_acc(self):
        return self._influencer_twitter_acc
    
    @property
    def tweet_ID(self):
        return self._tweet_ID

    @property
    def tweet_text(self):
        return self._tweet_text
    
    @property
    def tweet_date_time(self):
        return self._tweet_date_time
    
    @property
    def crypto_ticker(self):
        return self._crypto_ticker

    @property
    def sentiment_score(self):
        return self._sentiment_score
