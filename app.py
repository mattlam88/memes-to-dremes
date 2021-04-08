from PySide2.QtWidgets import QApplication

from controllers.dashboard_controller import DashboardController
from models.dashboard_model import DashboardModel
from views.dashboard_view import DashboardView


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self._model = DashboardModel()
        self._controller = DashboardController(model=self._model)
        self._view = DashboardView(self._model, self._controller)

        self._view.show()
