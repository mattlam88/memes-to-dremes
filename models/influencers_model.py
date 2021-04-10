import sqlite3

from settings import DB_PATH


class InfluencersDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
    
    def add_influencer(self, influencer_user_id, influencer_name, influencer_twitter_acc):
        self.cur.execute(
            """
            INSERT INTO influencers (influencer_user_id, influencer_name, influencer_twitter_acc) 
            VALUES (?, ?,?);
            """,
            (influencer_user_id, influencer_name, influencer_twitter_acc)
        )
        self.conn.commit()

    def get_influencer(self, influencer_name):
        influencer_data = self.cur.execute(
            f"""
            SELECT id, influencer_user_id, influencer_name, influencer_twitter_acc 
            FROM influencers 
            WHERE influencer_name="{influencer_name}";
            """
        )
        influencer_name_data = Influencers(*influencer_data)
        return influencer_name_data
    

class Influencers:
    def __init__(self, id, influencer_user_id, influencer_name, influencer_twitter_acc):
        self._id = id
        self._influencer_user_id = influencer_user_id
        self._influencer_name = influencer_name
        self._influencer_twitter_acc = influencer_twitter_acc
