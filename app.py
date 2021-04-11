from __future__ import annotations

from typing import cast, List, TYPE_CHECKING

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
import tweepy as tp

from controllers.app_controller import AppController
from models.app_model import AppModel
from utils.tweet_feed import StreamListener
from views.app_view import AppView

if TYPE_CHECKING:
    from tweepy import Stream
    from controllers.base_controller import BaseController
    from views.base_view import BaseView


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self._model: BaseModel = AppModel()
        self._controller: BaseController = AppController(model=self._model)
        self._view: BaseView = AppView(self._model, self._controller)

        # run twitter stream
        self._controller.twitterStream = self._subscribeToTwitterStream()
        cast(AppController, self._controller).startStream()

        cast(AppView, self._view).show()

    @property
    def controller(self) -> BaseController:
        return self._controller

    def _subscribeToTwitterStream(self) -> Stream:
        controller: AppController = cast(AppController, self.controller)

        influencers: List[str] = controller.getInfluencerIds()
        stream_listener: StreamListener = StreamListener(controller.api, controller, influencers)
        stream: Stream = tp.Stream(auth=controller.api.auth, listener=stream_listener)

        return stream
