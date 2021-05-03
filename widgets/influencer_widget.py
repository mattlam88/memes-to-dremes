from PySide2.QtWidgets import QWidget

from widgets.influencer_widget_ui import Ui_Influencer


class InfluencerWidget(QWidget):
    # region Properties

    @property
    def ui(self) -> Ui_Influencer:
        return self._ui

    # endregion

    # region Constructor

    def __init__(self) -> None:
        super().__init__()

        self._ui: Ui_Influencer = Ui_Influencer()
        self.ui.setupUi(self)
        self._connectSignals()

    def _connectSignals(self) -> None:
        pass

    # endregion
