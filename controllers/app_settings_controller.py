from typing import cast, Dict

from .base_controller import BaseController
from models.app_settings_model import AppSettingsModel


class AppSettingsController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

    def saveSettings(self, newSettings: Dict[str, str]) -> None:
        cast(AppSettingsModel, self.model).settings = newSettings
