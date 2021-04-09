import sqlite3

class InfluencersDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect("/Users/mattlam/Documents/OSU-Hackathon-Spring-2021/memes-to-dremes/memesToDremes.db") # give the exact location of the database file
        self.cur = self.conn.cursor()
    
    def add_influencer(self, influencer_name, influcencer_twitter_acc):
        self.cur.execute("""INSERT INTO influencers (influencer_name, influcencer_twitter_acc) VALUES (?,?);""")
        self.conn.commit()

    def get_influencer(self, influencer_name):
        influencer_data = self.cur.execute(f'SELECT id, influencer_name, influencer_twitter_acc FROM influencers WHERE influencer_name="{influencer_name}";')
        influencer_name_data = Influencers(influencer_data[0], influencer_data[1], influencer_data[2])
        return influencer_name_data
    

class Influencers:
    def __init__(self, id, influencer_name, influcencer_twitter_acc):
        self._id = id
        self._influencer_name = influencer_name
        self._influcencer_twitter_acc = influcencer_twitter_acc