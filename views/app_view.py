from __future__ import annotations

from typing import cast, TYPE_CHECKING

from PySide2.QtWidgets import QMainWindow

from controllers.app_controller import AppController
from models.app_model import AppModel
from views.base_view import BaseView
from views.app_ui import Ui_App

if TYPE_CHECKING:
    from controllers.base_controller import BaseController
    from models.base_model import BaseModel


class AppViewMeta(type(QMainWindow), type(BaseView)):
    pass


class AppView(QMainWindow, BaseView, metaclass=AppViewMeta):
    """Main app window that displays crypto dashboard."""

    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QMainWindow.__init__(self)
        BaseView.__init__(self, model, controller, Ui_App())

        self._updateUI()

    def _connectSignals(self) -> None:
        self.ui.pushButton_5.clicked.connect(self._onBtnClicked)
        cast(AppModel, self.model).btnTextChanged.connect(self._onBtnTextChanged)

    def _updateUI(self) -> None:
        cast(AppController, self.controller).updateTweetHistory()

    def _onBtnClicked(self) -> None:
        cast(AppController, self.controller).changeBtnText("What's up?")

    def _onBtnTextChanged(self) -> None:
        self.ui.pushButton_5.setText(cast(AppModel, self.model).btnText)
