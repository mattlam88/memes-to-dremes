from typing import List, Type

from PySide2.QtCore import QObject, Signal

from .base_model import BaseModel


class AppModelMeta(type(QObject), type(BaseModel)):
    pass


class AppModel(QObject, BaseModel, metaclass=AppModelMeta):
    btnTextChanged: Signal = Signal(str)
    tweetHistoryChanged: Signal = Signal(list)

    def __init__(self) -> None:
        QObject.__init__(self)
        BaseModel.__init__(self)

        self._btnText: str = str()
        self._tweetHistory: List[str] = list()

    @property
    def btnText(self) -> str:
        return self._btnText

    @btnText.setter
    def btnText(self, value: str) -> None:
        self._btnText = value
        self.btnTextChanged.emit(value)

    @property
    def tweetHistory(self) -> List[str]:
        return self._tweetHistory

    @tweetHistory.setter
    def tweetHistory(self, value) -> None:
        self._tweetHistory = value
        self.tweetHistoryChanged.emit(value)
