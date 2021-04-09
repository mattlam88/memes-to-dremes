import sqlite3

class InfluencersDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        pass

class Influencers:
    def __init__(self, id, influencer_name, influcencer_twitter_acc):
        self._id = id
        self._influencer_name = influencer_name
        self._influcencer_twitter_acc = influcencer_twitter_acc