from typing import cast

from .base_controller import BaseController
from models.app_model import AppModel


class AppController(BaseController):
    def __init__(self, model) -> None:
        super().__init__(model)

    def changeBtnText(self, value):
        cast(AppModel, self.model).btnText = value

    def addInfluencer(self, value) -> None:
        pass

    def removeInfluencer(self, value) -> None:
        pass

    def updateTweetHistory(self) -> None:
        # get tweets from database
        # pass tweets to model
        pass

    def addTweet(self, value) -> None:
        # add tweet to database
        # pass tweet to model
        # manually trigger signal here
        model: AppModel = cast(AppModel, self.model)
        model.btnText = value
