from datetime import datetime, timedelta
import time

from pycoingecko import CoinGeckoAPI
from PySide2.QtCore import QObject


class CryptoCoin:
    """
    Creates a CryptoCoin object which contains a name, ticker, and price.
    """

    def __init__(self, name, ticker):
        self._name = name
        self._ticker = ticker
        self._price = None
        self._cg = CoinGeckoAPI()

    @property
    def coin_gecko(self):
        return self._cg

    def update_crypto_price(self, fiat="usd"):
        """
        By default, the price is denominated in usd but by providing an optional fiat argument, the price could
        be displayed in rubles or whatever you are laundering
        """
        self._price = self.coin_gecko.get_price(ids=self._name, vs_currencies=fiat)

    def get_price(self):
        return self._price

    def get_historic_pricing(self, start_date, end_date, fiat="usd"):
        """
        Takes start and end dates as UNIX timestamp and returns pricing during that range.
        """
        return self.coin_gecko.get_coin_market_chart_range_by_id(id=self._name, vs_currency=fiat, from_timestamp=start_date,
                                                    to_timestamp=end_date)

    def get_current_price(self, fiat="usd"):
        return self.coin_gecko.get_price(ids=self._name, vs_currencies=fiat)


class CoinGeckoWorker(QObject):
    # two weeks of time in milliseconds
    TWO_WEEKS = 1209600000

    def __init__(self, model):
        super().__init__(model)
        self._model = model

    def run(self):
        cryptocoin = CryptoCoin("bitcoin", "btc")
        start_date = time.mktime((datetime.today() - timedelta(days=14)).timetuple())
        end_date = time.mktime((datetime.now()).timetuple())
        self._model.cryptoPriceHistory = cryptocoin.get_historic_pricing(start_date=start_date, end_date=end_date)
