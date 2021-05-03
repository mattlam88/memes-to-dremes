from PySide2.QtWidgets import QWidget

from widgets.tweet_widget_ui import Ui_Tweet


class TweetWidget(QWidget):
    # region Properties

    @property
    def ui(self) -> Ui_Tweet:
        return self._ui

    # endregion

    # region Constructor

    def __init__(self) -> None:
        super().__init__()

        self._ui: Ui_Tweet = Ui_Tweet()
        self.ui.setupUi(self)
        self._connectSignals()

    def _connectSignals(self) -> None:
        pass

    # endregion
