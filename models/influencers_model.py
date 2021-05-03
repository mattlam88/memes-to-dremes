import os
import sqlite3


class InfluencersDAO:
    # region Constructor

    def __init__(self, db_path, db_name):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect(os.path.join(db_path, db_name))
        self.cur = self.conn.cursor()

    # endregion
    
    def add_influencer(self, influencer_user_id, influencer_name, influencer_twitter_acc, following_influencer):
        """
        Adds influencer to the database by taking in the unique user id, name, twitter handle and whether or they are
        being followed
        """

        self.cur.execute(
            """
            INSERT or IGNORE INTO influencers (
                influencer_user_id, 
                influencer_name, 
                influencer_twitter_acc, 
                following_influencer
            ) 
            VALUES (?, ?, ?, ?);
            """,
            (influencer_user_id, influencer_name, influencer_twitter_acc, following_influencer)
        )
        self.conn.commit()

    def follow_influencer(self, influencer_twitter_acc):
        """
        Updates influencer in the database by taking chaning their current status to followed
        """

        self.cur.execute(
            f"""
            UPDATE influencers SET following_influencer=1 WHERE influencer_twitter_acc='{influencer_twitter_acc}';
            """
        )
        self.conn.commit()

    def unfollow_influencer(self, influencer_twitter_acc):
        """
        Updates influencer in the database by taking chaning their current status to unfollowed
        """

        self.cur.execute(
            f"""
            UPDATE influencers SET following_influencer=0 WHERE influencer_twitter_acc='{influencer_twitter_acc}'
            """
        )
        self.conn.commit()

    def get_influencer(self, influencer_name):
        """
        Retrieves a single influencer's data from the database
        """

        influencer_data = self.cur.execute(
            f"""
            SELECT id, influencer_user_id, influencer_name, influencer_twitter_acc, following_influencer
            FROM influencers 
            WHERE influencer_name='{influencer_name}';
            """
        )
        influencer_name_data = Influencers(*influencer_data)
        return influencer_name_data

    def get_influencers(self):
        """
        Retrieves all influencers' data from the database
        """

        influencers_data = self.cur.execute(
            f"""
            SELECT id, influencer_user_id, influencer_name, influencer_twitter_acc, following_influencer
            FROM influencers;
            """
        )
        influencers = [Influencers(*data) for data in influencers_data]
        return influencers


class Influencers:
    """Represents an Influencer which takes in an id, user id, name, twitter handle, and a following status"""

    # region Properties

    @property
    def influencer_user_id(self):
        return self._influencer_user_id

    @property
    def influencer_twitter_acc(self):
        return self._influencer_twitter_acc

    @property
    def following_influencer(self):
        return self._following_influencer

    # endregion

    # region Constructor

    def __init__(self, id, influencer_user_id, influencer_name, influencer_twitter_acc, following_influencer):
        self._id = id
        self._influencer_user_id = influencer_user_id
        self._influencer_name = influencer_name
        self._influencer_twitter_acc = influencer_twitter_acc
        self._following_influencer = following_influencer

    # endregion
