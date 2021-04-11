from PySide2.QtWidgets import QWidget

from widgets.tweet_widget_ui import Ui_Tweet


class TweetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._ui: Ui_Tweet = Ui_Tweet()
        self.ui.setupUi(self)
        self._connectSignals()

    def _connectSignals(self) -> None:
        pass

    @property
    def ui(self) -> Ui_Tweet:
        return self._ui
