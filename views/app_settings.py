from typing import cast, Dict

from PySide2.QtWidgets import QDialog

from controllers.app_settings_controller import AppSettingsController
from controllers.base_controller import BaseController
from models.base_model import BaseModel
from views.app_settings_ui import Ui_AppSettings
from views.base_view import BaseView


class AppSettingsDialogMeta(type(QDialog), type(BaseView)):
    pass


class AppSettingsDialog(QDialog, BaseView, metaclass=AppSettingsDialogMeta):
    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QDialog.__init__(self)
        BaseView.__init__(self, model, controller, Ui_AppSettings())

        self._connectSignals()

    def _connectSignals(self) -> None:
        self.ui.saveBtn.clicked.connect(self._onSaveBtnClicked)
        self.ui.closeBtn.clicked.connect(self._onCloseBtnClicked)

    def _onSaveBtnClicked(self) -> None:
        settings: Dict[str, str] = {
            "API_KEY": self.ui.apiKeyLineEdit.text(),
            "API_SECRET": self.ui.apiSecretLineEdit.text(),
            "ACCESS_TOKEN": self.ui.accessTokenLineEdit.text(),
            "ACCESS_TOKEN_SECRET": self.ui.accessTokenSecretLineEdit.text(),
            "DB_NAME": self.ui.databaseNameLineEdit.text(),
            "DB_PATH": self.ui.databasePathLineEdit.text()
        }

        cast(AppSettingsController, self.controller).saveSettings(settings)

    def _onCloseBtnClicked(self) -> None:
        self.close()
