from datetime import datetime
import time

from PySide2.QtCore import QObject

from .crypto_coin import CryptoCoin


class CoinGeckoWorker(QObject):
    """Handles threaded calls to CoinGecko API"""

    # region Properties

    @property
    def model(self):
        return self._model

    # endregion

    # region Constructor

    def __init__(self, model):
        super().__init__(model)
        self._model = model

    # endregion

    def run(self, name: str, ticker: str, startDate: datetime, endDate: datetime):
        """Get 14 days worth of crypto-currency prices for bitcoin."""

        cryptoCoin = CryptoCoin(name, ticker)

        self.model.cryptoPriceHistory = cryptoCoin.get_historic_pricing(
            start_date=time.mktime(startDate.timetuple()), end_date=time.mktime(endDate.timetuple())
        )
