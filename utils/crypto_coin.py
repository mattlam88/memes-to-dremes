from pycoingecko import CoinGeckoAPI


class CryptoCoin:
    """
    Creates a CryptoCoin object which contains a name, ticker, and price.
    """

    # region Properties

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value) -> None:
        self._price = value

    @property
    def api(self):
        return self._api

    # endregion

    # region Constructor

    def __init__(self, name, ticker):
        self._name = name
        self._ticker = ticker
        self._price = None
        self._api = CoinGeckoAPI()

    # endregion

    def update_crypto_price(self, fiat="usd"):
        """
        By default, the price is denominated in usd but by providing an optional fiat argument, the price could
        be displayed in rubles or whatever you are laundering
        """

        self.price = self.api.get_price(ids=self.name, vs_currencies=fiat)

    def get_historic_pricing(self, start_date, end_date, fiat="usd"):
        """
        Takes start and end dates as UNIX timestamp and returns pricing during that range.
        """

        return self.api.get_coin_market_chart_range_by_id(
            id=self.name, vs_currency=fiat, from_timestamp=start_date, to_timestamp=end_date
        )

    def get_current_price(self, fiat="usd"):
        return self.api.get_price(ids=self.name, vs_currencies=fiat)
