import sqlite3

# This file is used to start a new database on a local machine
# Running this file will create a database if it doesn't exist
# If this file is ran for a second time it reinitialize the previous database and start it from scratch

conn = sqlite3.connect("memesToDremes.db")
c = conn.cursor()

c.execute("""DROP TABLE IF EXISTS crypto_ID;""")
c.execute("""DROP TABLE IF EXISTS influencers;""")
c.execute("""DROP TABLE IF EXISTS influencer_tweets;""")

c.execute(
    """
    CREATE TABLE crypto_ID (
        id INTEGER PRIMARY KEY,
        crypto_name TEXT,
        crypto_ticker TEXT,
        crypto_equivalent_names TEXT
    );
    """
)

c.execute(
    """
    CREATE TABLE influencers (
        id INTEGER PRIMARY KEY,
        influencer_user_id TEXT,
        influencer_name TEXT,
        influencer_twitter_acc TEXT,
        following_influencer INTEGER
    );
    """
)

c.execute(
    """
    CREATE TABLE influencer_tweets (
        id INTEGER PRIMARY KEY,
        influencer_twitter_acc TEXT,
        tweet_ID INTEGER,
        tweet_text TEXT,
        tweet_date_time TEXT,
        crypto_ticker TEXT,
        sentiment_score INTEGER
    );
    """
)

conn.commit()
c.close()

print("Looks like we're all good to go!")
