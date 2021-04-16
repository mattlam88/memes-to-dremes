from typing import Dict, List, Tuple

from PySide2.QtCore import QObject, Signal

from .base_model import BaseModel


class AppModelMeta(type(QObject), type(BaseModel)):
    pass


class AppModel(QObject, BaseModel, metaclass=AppModelMeta):
    # region Signals

    btnTextChanged: Signal = Signal(str)
    tweetHistoryChanged: Signal = Signal(list)
    tweetAdded: Signal = Signal(dict)
    influencerFollowed: Signal = Signal(str)
    influencerUnFollowed: Signal = Signal(str)
    cryptoPriceUpdated: Signal = Signal(dict)
    aggregateScoreUpdated: Signal = Signal(tuple)

    # endregion

    # region Properties

    @property
    def tweetHistory(self) -> List[Dict[str, str]]:
        return self._tweetHistory

    @tweetHistory.setter
    def tweetHistory(self, value) -> None:
        self._tweetHistory = value
        self.tweetHistoryChanged.emit(value)

    @property
    def cryptoPriceHistory(self) -> Dict[str, float]:
        return self._cryptoPriceHistory

    @cryptoPriceHistory.setter
    def cryptoPriceHistory(self, value: Dict[str, float]) -> None:
        self._cryptoPriceHistory: Dict[str, float] = value
        self.cryptoPriceUpdated.emit(value)

    @property
    def followingInfluencers(self) -> List[str]:
        return self._followingInfluencers

    @property
    def aggregateScore(self) -> Tuple[int, int]:
        return self._aggregateScore

    @aggregateScore.setter
    def aggregateScore(self, value: Tuple[int, int]) -> None:
        self._aggregateScore = value
        self.aggregateScoreUpdated.emit(value)

    # endregion

    # region Constructor

    def __init__(self) -> None:
        QObject.__init__(self)
        BaseModel.__init__(self)

        self._tweetHistory: List[Dict[str, str]] = list()
        self._followingInfluencers: List[str] = list()
        self._cryptoPriceHistory: Dict[str, float] = dict()
        self._aggregateScore: Tuple[int, int] = (0, 0)

    # endregion

    def addTweet(self, tweet) -> None:
        self.tweetHistory.append(tweet)
        self.tweetAdded.emit(tweet)

    def followInfluencer(self, twitterHandle: str) -> None:
        self.followingInfluencers.append(twitterHandle)
        self.influencerFollowed.emit(twitterHandle)

    def unFollowInfluencer(self, twitterHandle: str) -> None:
        self.followingInfluencers.remove(twitterHandle)
        self.influencerUnFollowed.emit(twitterHandle)
