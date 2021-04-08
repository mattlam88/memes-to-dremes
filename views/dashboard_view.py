from __future__ import annotations

from typing import cast, TYPE_CHECKING

from PySide2.QtWidgets import QMainWindow

from controllers.dashboard_controller import DashboardController
from models.dashboard_model import DashboardModel
from views.base_view import BaseView
from views.dashboard_ui import Ui_Dashboard

if TYPE_CHECKING:
    from controllers.base_controller import BaseController
    from models.base_model import BaseModel


class DashboardViewMeta(type(QMainWindow), type(BaseView)):
    pass


class DashboardView(QMainWindow, BaseView, metaclass=DashboardViewMeta):
    """Main app window that displays crypto dashboard."""

    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QMainWindow.__init__(self)
        BaseView.__init__(self, model, controller, Ui_Dashboard())

    def _connectSignals(self) -> None:
        self.ui.pushButton_5.clicked.connect(self._onBtnClicked)
        cast(DashboardModel, self.model).btnTextChanged.connect(self._onBtnTextChanged)

    def _onBtnClicked(self) -> None:
        cast(DashboardController, self.controller).changeBtnText("What's up?")

    def _onBtnTextChanged(self) -> None:
        self.ui.pushButton_5.setText(cast(DashboardModel, self.model).btnText)
