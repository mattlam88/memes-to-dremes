from PySide2.QtCore import QObject, Signal, Slot

from .base_model import BaseModel


class DashboardModelMeta(type(QObject), type(BaseModel)):
    pass


class DashboardModel(QObject, BaseModel, metaclass=DashboardModelMeta):
    btnTextChanged: Signal = Signal(str)

    def __init__(self) -> None:
        QObject.__init__(self)
        BaseModel.__init__(self)

        self._btnText: str = str()

    @property
    def btnText(self) -> str:
        return self._btnText

    @btnText.setter
    def btnText(self, value: str) -> None:
        self._btnText = value
        self.btnTextChanged.emit(value)
