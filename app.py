from __future__ import annotations

from typing import cast, TYPE_CHECKING

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
import tweepy as tp

from controllers.app_controller import AppController
from models.app_model import AppModel
from utils.stream_listener import StreamListener
from settings import API_KEY, API_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
from views.app_view import AppView

if TYPE_CHECKING:
    from tweepy import Stream
    from controllers.base_controller import BaseController
    from views.base_view import BaseView


# Handles authentication by pulling API key information from config file
auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tp.API(auth)


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

        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(600)
        # self.timer.timeout.connect(self._controller.update_plot)
        # self.timer.start()

    def _subscribeToTwitterStream(self) -> Stream:
        stream_listener: StreamListener = StreamListener()
        stream_listener.controller = self.controller
        stream: Stream = tp.Stream(auth=api.auth, listener=stream_listener)

        return stream

    @property
    def controller(self) -> BaseController:
        return self._controller
