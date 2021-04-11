import os
import sqlite3


class CryptoIDDAO:
    def __init__(self, db_path, db_name):
        # will include various statements that will pull information from the database or insert in the database
        self.conn = sqlite3.connect(os.path.join(db_path, db_name)) # give the exact location of the database file
        self.cur = self.conn.cursor()
    
    def add_crypto_id(self, crypto_name, crypto_ticker, crypto_equivalent_names):
        self.cur.execute(
            """
            INSERT INTO crypto_ID (crypto_name, crypto_ticker, crypto_equivalent_names) 
            VALUES (?,?,?);
            """,
            (crypto_name, crypto_ticker, crypto_equivalent_names)
        )
        self.conn.commit()

    def get_crypto_equivalent_names(self, crypto_ticker):
        lst_equivalent_names = []

        equivalent_names = self.cur.execute(
            f"""
            SELECT crypto_equivalent_names 
            FROM crypto_ID 
            WHERE crypto_ticker="{crypto_ticker}";
            """
        )
        for name in equivalent_names:
            lst_equivalent_names.append(name)
        return lst_equivalent_names
    

class CryptoID:
    def __init__(self, id, crypto_name, crypto_ticker, crypto_equivalent_names):
        self._id = id
        self._crypto_name = crypto_name
        self._crypto_ticker = crypto_ticker
        self._crypto_equivalent_names = crypto_equivalent_names
