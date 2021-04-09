import sqlite3

class InfluencersTweetDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect("/Users/mattlam/Documents/OSU-Hackathon-Spring-2021/memes-to-dremes/memesToDremes.db") # give the exact location of the database file
        self.cur = self.conn.cursor()
    
    def add_influencer_tweet(self, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score):
        self.cur.execute("""INSERT INTO influencers_tweets (influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score) VALUES (?,?,?,?,?,?);""")
        self.conn.commit()

    def get_influencer_tweets(self, influencer_twitter_acc, crypto_ticker):
        all_influencer_tweets = {}
        tweet_data = self.cur.execute(f'SELECT id, influencer_twitter_acc, tweet_ID, tweet_text, tweet_date_time, crypto_ticker, sentiment_score FROM influencer_tweets WHERE influencer_twitter_acc={influencer_twitter_acc} AND crypto_ticker={crypto_ticker};')
        for data in tweet_data:
            influencer_name = data[1]
            all_influencer_tweets[influencer_name] = InfluencersTweet(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
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
