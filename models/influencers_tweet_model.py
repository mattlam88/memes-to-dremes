import os
import sqlite3


class InfluencersTweetDAO:
    # region Constructor

    def __init__(self, db_path, db_name):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect(os.path.join(db_path, db_name)) # give the exact location of the database file
        self.cur = self.conn.cursor()

    # endregion
    
    def add_influencer_tweet(self, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker,
                             sentiment_score):
        self.cur.execute(
            """
            INSERT or IGNORE INTO influencer_tweets (
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
        """Gets all the tweets of a single influencer from the database"""

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

    def get_all_influencer_tweets(self, influencer_twitter_acc):
        """Gets all the tweets of all the influencers from the database"""

        all_influencer_tweets = []
        tweet_data = self.cur.execute(
            f"""
            SELECT id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score
            FROM influencer_tweets
            WHERE influencer_twitter_acc="{influencer_twitter_acc}";
            """
        )
        for data in tweet_data:
            all_influencer_tweets.append(InfluencersTweet(*data))

        return all_influencer_tweets

    def get_weekly_sentiment_score(self, start_date, end_date, twitter_handle):
        """Runs a query to count up all the weekly sentiment score by date returns a list of sentiment score objects"""

        weekly_sentiment_count = []
        
        weekly_data = self.cur.execute(
            f"""
            SELECT tweet_date_time, sentiment_score, count(sentiment_score)
            FROM influencer_tweets
            WHERE tweet_date_time BETWEEN {start_date} AND {end_date}
            GROUP BY day(tweet_date_time), sentiment_score
            ORDER BY tweet_date_time ASC, sentiment_score ASC;
            """
        )

        for data in weekly_data:
            weekly_sentiment_score = InfluencerTweetSentimentScore(data[0], data[1], data[2])
            weekly_sentiment_count.append(weekly_sentiment_score)
        return weekly_sentiment_count

    def get_daily_sentiment_score(self, current_date):
        """Runs a query to count up sentiment scores of a single day and returns a list of sentiment score objects"""

        daily_sentiment_count = {}

        daily_data = self.cur.execute(
            f"""
            SELECT sentiment_score, count(sentiment_score)
            FROM influencer_tweets
            WHERE STRFTIME('%Y', tweet_date_time) = '{current_date["year"]}'
              AND STRFTIME('%m', tweet_date_time) = '{current_date["month"]}'
              AND STRFTIME('%d', tweet_date_time) = '{current_date["day"]}'
            GROUP BY sentiment_score
            ORDER BY tweet_date_time ASC, sentiment_score ASC;
            """
        )

        for data in daily_data:
            daily_sentiment_count[data[0]] = data[1]

        return daily_sentiment_count


class InfluencersTweet:
    # region Properties

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

    # endregion

    # region Constructor

    def __init__(self, id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker,
                 sentiment_score):
        self._id = id
        self._influencer_twitter_acc = influencer_twitter_acc
        self._tweet_ID = tweet_ID
        self._tweet_text = tweet_text
        self._tweet_date_time = tweet_date_time
        self._crypto_ticker = crypto_ticker
        self._sentiment_score = sentiment_score

    # endregion

    def to_dict(self):
        return {
            "screenName": self.influencer_twitter_acc,
            "tweetID": self.tweet_ID,
            "tweetText": self.tweet_text,
            "createdAt": self.tweet_date_time,
            "cryptoTicker": self.crypto_ticker,
            "sentimentScore": self.sentiment_score
        }


class InfluencerTweetSentimentScore:
    # region Constructor

    def __init__(self, date, following_influencer, sentiment_score_total):
        self._date = date
        self._following_influencer = following_influencer
        self._sentiment_score_total = sentiment_score_total

    # endregion
