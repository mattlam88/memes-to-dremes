from __future__ import annotations

from typing import cast, TYPE_CHECKING

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QAction, QMainWindow, QVBoxLayout

if TYPE_CHECKING:
    from PySide2.QtGui import QCloseEvent

    from controllers.base_controller import BaseController
    from models.base_model import BaseModel

from controllers.app_controller import AppController
from controllers.app_settings_controller import AppSettingsController
from models.app_model import AppModel
from models.app_settings_model import AppSettingsModel
from views.app_ui import Ui_App
from views.base_view import BaseView
from views.app_settings import AppSettingsDialog
from widgets.bar_chart_widget import BarChartWidget
from widgets.demo_plot_widget import DemoPlotWidget
from widgets.influencer_widget import InfluencerWidget
from widgets.pie_chart_widget import PieChartWidget
from widgets.tweet_widget import TweetWidget
from widgets.tweet_stream_widget import TweetStreamWidget


class AppViewMeta(type(QMainWindow), type(BaseView)):
    pass


class AppView(QMainWindow, BaseView, metaclass=AppViewMeta):
    """Main app window that displays crypto dashboard."""

    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QMainWindow.__init__(self)
        BaseView.__init__(self, model, controller, Ui_App())

        self._influencers = list()
        self._tweets = list()
        self._tweetStream = TweetStreamWidget()
        self._barChart = BarChartWidget({"k1": [1, 2], "k2": [3, 4]})
        self._pieChart = PieChartWidget((10, 10))

        self._settingsDialogModel = AppSettingsModel()
        self._settingsDialogController = AppSettingsController(self._settingsDialogModel)
        self._settingsDialog = AppSettingsDialog(self._settingsDialogModel, self._settingsDialogController)

        self._loadSettings()
        self._connectSignals()
        self._updateUI()

    @property
    def tweetStream(self) -> TweetStreamWidget:
        return self._tweetStream

    @property
    def barChart(self) -> BarChartWidget:
        return self._barChart

    @property
    def pieChart(self) -> PieChartWidget:
        return self._pieChart

    @property
    def settingsDialog(self) -> AppSettingsDialog:
        return self._settingsDialog

    def _loadSettings(self) -> None:
        settings: QSettings = cast(AppController, self.controller).settings
        try:
            self.resize(settings.value("window size"))
            self.move(settings.value("window position"))
        except:
            pass

    def _connectSignals(self) -> None:
        self.tweetStream.ui.followInfluencerBtn.clicked.connect(self._onFollowInfluencerBtnClicked)
        self.ui.actionSettings.triggered.connect(self._onSettingsBtnClicked)
        self.ui.actionClose.triggered.connect(self.close)
        cast(AppSettingsModel, self.settingsDialog.model).settingsChanged.connect(self._onSettingsSaved)
        model: AppModel = cast(AppModel, self.model)
        model.tweetHistoryChanged.connect(self._onTweetHistoryChanged)
        model.tweetAdded.connect(self._onNewTweetAdded)
        model.influencerFollowed.connect(self._onInfluencerFollowed)
        model.influencerUnFollowed.connect(self._onInfluencerUnFollowed)

    def _updateUI(self) -> None:
        # add widgets to ui
        tweetStreamLayout = QVBoxLayout()
        tweetStreamLayout.addWidget(self._tweetStream)
        self.ui.tweetStreamFrame.setLayout(tweetStreamLayout)

        barChartLayout = QVBoxLayout()
        barChartLayout.addWidget(self._barChart)
        self.ui.leftTopChartFrame.setLayout(barChartLayout)

        pieChartLayout = QVBoxLayout()
        pieChartLayout.addWidget(self._pieChart)
        self.ui.rightTopChartFrame.setLayout(pieChartLayout)

        plot = DemoPlotWidget()
        demoChart = QVBoxLayout()
        demoChart.addWidget(plot)
        self.ui.bottomChartFrame.setLayout(demoChart)

        self.tweetStream.ui.tweetStreamScrollAreaContents.setLayout(QVBoxLayout())
        self.tweetStream.ui.followingInfluencersScrollArea.setLayout(QVBoxLayout())

        cast(AppController, self.controller).updateTweetHistory()

    def _onFollowInfluencerBtnClicked(self) -> None:
        twitterHandle: str = self.tweetStream.ui.lineEditTwitterHandle.text()
        cast(AppController, self.controller).followInfluencer(twitterHandle)
        self.tweetStream.ui.lineEditTwitterHandle.clear()

    def _onTweetHistoryChanged(self) -> None:
        # update graphs and tweet stream display
        pass

    def _onNewTweetAdded(self, tweet) -> None:
        tweetWidget = TweetWidget()
        tweetWidget.ui.tweet.setText(tweet.get("tweetText"))
        tweetWidget.ui.twitterHandle.setText("@" + tweet.get("screenName"))
        tweetWidget.ui.cryptoTicker.setText(tweet.get("cryptoTicker"))

        self.tweetStream.ui.tweetStreamScrollAreaContents.layout().addWidget(tweetWidget)

    def _onInfluencerFollowed(self, twitterHandle: str) -> None:
        influencerWidget = InfluencerWidget()
        influencerWidget.ui.twitterHandle.setText(twitterHandle)
        self.tweetStream.ui.followingInfluencersScrollArea.layout().addWidget(influencerWidget)

    def _onInfluencerUnFollowed(self, twitterHandle: str) -> None:
        pass

    def _onSettingsBtnClicked(self) -> None:
        settings: QSettings = cast(AppController, self.controller).settings
        self.settingsDialog.ui.apiKeyLineEdit.setText(settings.value("API_KEY", ''))
        self.settingsDialog.ui.apiSecretLineEdit.setText(settings.value("API_SECRET", ''))
        self.settingsDialog.ui.accessTokenLineEdit.setText(settings.value("ACCESS_TOKEN", ''))
        self.settingsDialog.ui.accessTokenSecretLineEdit.setText(settings.value("ACCESS_TOKEN_SECRET", ''))
        self.settingsDialog.ui.databaseNameLineEdit.setText(settings.value("DB_NAME", ''))
        self.settingsDialog.ui.databasePathLineEdit.setText(settings.value("DB_PATH", ''))
        self.settingsDialog.exec_()

    def _onSettingsSaved(self, newSettings) -> None:
        settings: QSettings = cast(AppController, self.controller).settings
        for key, value in newSettings.items():
            settings.setValue(key, value)

        controller: AppController = cast(AppController, self.controller)
        controller.restartStream()
        controller.updateTweetHistory()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())
        cast(AppController, self.controller).tearDown()
        event.accept()
