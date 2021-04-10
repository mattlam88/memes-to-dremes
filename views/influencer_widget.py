from PySide2.QtWidgets import QWidget

from views.influencer_widget_ui import Ui_Influencer


class InfluencerWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._ui: Ui_Influencer = Ui_Influencer()
        self._connectSignals()

    def _connectSignals(self) -> None:
        pass

    @property
    def ui(self) -> Ui_Influencer:
        return self._ui
