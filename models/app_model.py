from typing import Dict, List, Type

from PySide2.QtCore import QObject, Signal

from .base_model import BaseModel


class AppModelMeta(type(QObject), type(BaseModel)):
    pass


class AppModel(QObject, BaseModel, metaclass=AppModelMeta):
    btnTextChanged: Signal = Signal(str)
    tweetHistoryChanged: Signal = Signal(list)
    tweetAdded: Signal = Signal(dict)
    influencerFollowed: Signal = Signal(str)
    influencerUnFollowed: Signal = Signal(str)

    def __init__(self) -> None:
        QObject.__init__(self)
        BaseModel.__init__(self)

        self._tweetHistory: List[Dict[str, str]] = list()
        self._followingInfluencers: List[str] = list()

    @property
    def tweetHistory(self) -> List[Dict[str, str]]:
        return self._tweetHistory

    @tweetHistory.setter
    def tweetHistory(self, value) -> None:
        self._tweetHistory = value
        self.tweetHistoryChanged.emit(value)

    @property
    def followingInfluencers(self) -> List[str]:
        return self._followingInfluencers

    def addTweet(self, tweet) -> None:
        self.tweetHistory.append(tweet)
        self.tweetAdded.emit(tweet)

    def followInfluencer(self, twitterHandle: str) -> None:
        self.followingInfluencers.append(twitterHandle)
        self.influencerFollowed.emit(twitterHandle)

    def unFollowInfluencer(self, twitterHandle: str) -> None:
        self.followingInfluencers.remove(twitterHandle)
        self.influencerUnFollowed.emit(twitterHandle)
