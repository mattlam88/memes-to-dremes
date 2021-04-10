from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


class CryptoCoin:
    """
    Creates a CryptoCoin object which contains a name, ticker, and price.
    """
    def __init__(self, name, ticker):
        self._name = name
        self._ticker = ticker
        self._price = None

    def update_crypto_price(self, fiat="usd"):
        """
        By default, the price is denominated in usd but by providing an optional fiat argument, the price could
        be displayed in rubles or whatever you are laundering
        """
        self._price = cg.get_price(ids=self._name, vs_currencies=fiat)

    def get_price(self):
        return self._price

# This is just an example to test the code
btc = CryptoCoin("bitcoin", "btc")
btc.update_crypto_price()
print(btc.get_price())

