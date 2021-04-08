from typing import cast

from .base_controller import BaseController
from models.dashboard_model import DashboardModel


class DashboardController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

    def changeBtnText(self, value):
        cast(DashboardModel, self.model).btnText = value
