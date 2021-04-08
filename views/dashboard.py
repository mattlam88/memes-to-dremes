from PySide2.QtWidgets import QMainWindow

from views.ui_dashboard import Ui_Dashboard


class Dashboard(QMainWindow, Ui_Dashboard):
    """Main app window that displays crypto dashboard."""

    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.setupUi(self)
