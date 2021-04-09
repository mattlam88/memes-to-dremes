import sqlite3

class CryptoIDDAO:
    def __init__(self):
        # will include various statements that will pull information from the database or insert in the database
        pass

class CryptoID:
    def __init__(self, id, crypto_name, crypto_ticker, crypto_equivalent_names):
        self._id = id
        self._crypto_name = crypto_name
        self._crytop_ticker = crypto_ticker
        self._crypto_equivalent_names = crypto_equivalent_names