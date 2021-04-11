from typing import Dict

from PySide2.QtCore import QObject, Signal

from .base_model import BaseModel


class AppSettingsModelMeta(type(QObject), type(BaseModel)):
    pass


class AppSettingsModel(QObject, BaseModel, metaclass=AppSettingsModelMeta):
    settingsChanged: Signal = Signal(dict)

    def __init__(self) -> None:
        QObject.__init__(self)
        BaseModel.__init__(self)

        self._settings: Dict[str, str] = dict()

    @property
    def settings(self) -> Dict[str, str]:
        return self._settings

    @settings.setter
    def settings(self, value: Dict[str, str]) -> None:
        self._settings = value
        self.settingsChanged.emit(value)
