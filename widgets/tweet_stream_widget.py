from PySide2.QtWidgets import QWidget

from widgets.tweet_stream_widget_ui import Ui_TweetStream


class TweetStreamWidget(QWidget):
    # region Properties

    @property
    def ui(self) -> Ui_TweetStream:
        return self._ui

    # endregion

    # region Constructor

    def __init__(self) -> None:
        super().__init__()

        self._ui: Ui_TweetStream = Ui_TweetStream()
        self.ui.setupUi(self)
        self._connectSignals()

    def _connectSignals(self) -> None:
        pass

    # endregion
