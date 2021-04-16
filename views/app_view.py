from __future__ import annotations

from datetime import datetime, timedelta
from typing import cast, TYPE_CHECKING

from PySide2.QtCore import QSettings, QPoint, QSize
from PySide2.QtWidgets import QMainWindow, QVBoxLayout

from controllers import AppController, AppSettingsController
from models import AppModel, AppSettingsModel
from views import AppSettingsView, Ui_App
from views.base_view import BaseView
from widgets import BarChartWidget, InfluencerWidget, LinePlotWidget, PieChartWidget, TweetWidget, TweetStreamWidget

if TYPE_CHECKING:
    from PySide2.QtGui import QCloseEvent

    from controllers import BaseController
    from models import BaseModel


class AppViewMeta(type(QMainWindow), type(BaseView)):
    pass


class AppView(QMainWindow, BaseView, metaclass=AppViewMeta):
    """Main app window that displays crypto dashboard."""

    # region Properties

    @property
    def barChart(self) -> BarChartWidget:
        return self._barChart

    @property
    def pieChart(self) -> PieChartWidget:
        return self._pieChart

    @property
    def linePlot(self) -> LinePlotWidget:
        return self._linePlot

    @property
    def tweetStream(self) -> TweetStreamWidget:
        return self._tweetStream

    @property
    def settingsDialog(self) -> AppSettingsView:
        return self._settingsDialog

    # endregion

    # region Constructor

    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QMainWindow.__init__(self)
        BaseView.__init__(self, model, controller, Ui_App())

        # Initialize widgets.
        self._tweetStream = TweetStreamWidget()
        self._barChart = BarChartWidget()
        self._pieChart = PieChartWidget()
        self._linePlot = LinePlotWidget()

        # TODO: Find a way to move this outside the class.
        # Initialize settings dialog.
        self._settingsDialogModel = AppSettingsModel()
        self._settingsDialogController = AppSettingsController(self._settingsDialogModel)
        self._settingsDialog = AppSettingsView(self._settingsDialogModel, self._settingsDialogController)

        # Configure UI.
        self._loadSettings()
        self._connectSignals()
        self._updateUI()

        # TODO: Move this somewhere else.
        # Retrieve data for UI.
        cast(AppController, self.controller).updateTweetHistory()
        cast(AppController, self.controller).updatePrice()

    def _loadSettings(self) -> None:
        """Loads UI settings from device registry."""

        settings: QSettings = cast(AppController, self.controller).settings
        try:
            self.resize(settings.value("window size"))
            self.move(settings.value("window position"))
        except:
            self.resize(QSize(1200, 900))
            self.move(QPoint(0, 0))

    def _connectSignals(self) -> None:
        """
        Connects view to all relevant signals.

        Called during constructor phase.
        """

        # Connect to UI buttons.
        self.ui.actionSettings.triggered.connect(self._onSettingsBtnClicked)
        self.ui.actionClose.triggered.connect(self.close)
        self.tweetStream.ui.followInfluencerBtn.clicked.connect(self._onFollowInfluencerBtnClicked)

        # Connect to settings updates.
        cast(AppSettingsModel, self.settingsDialog.model).settingsChanged.connect(self._onSettingsSaved)

        # Connect to model updates.
        model: AppModel = cast(AppModel, self.model)
        model.tweetAdded.connect(self._onNewTweetAdded)
        model.tweetHistoryChanged.connect(self._onTweetHistoryChanged)
        model.influencerFollowed.connect(self._onInfluencerFollowed)
        model.influencerUnFollowed.connect(self._onInfluencerUnFollowed)
        model.cryptoPriceUpdated.connect(self._onCryptoPriceUpdated)
        model.aggregateScoreUpdated.connect(self._onAggregateScoreUpdated)

    def _updateUI(self) -> None:
        """
        Draws the UI and all its sub-widgets.

        Called during constructor phase.
        """

        # TODO: Move sub-widget drawing to tweet stream widget class.
        # Draw tweet stream widget and its sub-widgets.
        self.tweetStream.ui.tweetStreamScrollAreaContents.setLayout(QVBoxLayout())
        self.tweetStream.ui.influencers.setLayout(QVBoxLayout())
        tweetStreamLayout = QVBoxLayout()
        tweetStreamLayout.addWidget(self.tweetStream)
        self.ui.tweetStreamFrame.setLayout(tweetStreamLayout)

        # Draw bar chart widget.
        barChartLayout = QVBoxLayout()
        barChartLayout.addWidget(self.barChart)
        self.ui.leftTopChartFrame.setLayout(barChartLayout)

        # Draw pie chart widget.
        pieChartLayout = QVBoxLayout()
        pieChartLayout.addWidget(self.pieChart)
        self.ui.rightTopChartFrame.setLayout(pieChartLayout)

        # Draw line plot widget.
        linePlotLayout = QVBoxLayout()
        linePlotLayout.addWidget(self._linePlot)
        self.ui.bottomChartFrame.setLayout(linePlotLayout)

    # endregion

    # region Event Handlers

    def _onFollowInfluencerBtnClicked(self) -> None:
        twitterHandle: str = self.tweetStream.ui.lineEditTwitterHandle.text()
        cast(AppController, self.controller).followInfluencer(twitterHandle)
        self.tweetStream.ui.lineEditTwitterHandle.clear()
        cast(AppController, self.controller).updateTweetHistory()

    def _onTweetHistoryChanged(self) -> None:
        cast(AppController, self.controller).computeAggregateScore(datetime.today())
        tweets = cast(AppModel, self.model).tweetHistory

        oneWeekDateRange = [datetime.today() - timedelta(days=x) for x in range(7)]
        oneWeekDateRange.reverse()

        oneWeekScores = dict()

        for date in oneWeekDateRange:
            cast(AppController, self.controller).computeAggregateScore(date)
            score = cast(AppModel, self.model).aggregateScore
            formattedDate = f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
            oneWeekScores[formattedDate] = score

        self.barChart.updatePlot(oneWeekScores)

        for tweet in tweets:
            tweetWidget = TweetWidget()
            tweetWidget.ui.tweet.setText(tweet.get("tweetText"))
            tweetWidget.ui.twitterHandle.setText("@" + tweet.get("screenName"))
            tweetWidget.ui.cryptoTicker.setText(tweet.get("cryptoTicker"))

            self.tweetStream.ui.tweetStreamScrollAreaContents.layout().addWidget(tweetWidget)

    def _onNewTweetAdded(self, tweet) -> None:
        cast(AppController, self.controller).computeAggregateScore(datetime.today())
        tweetWidget = TweetWidget()
        tweetWidget.ui.tweet.setText(tweet.get("tweetText"))
        tweetWidget.ui.twitterHandle.setText("@" + tweet.get("screenName"))
        tweetWidget.ui.cryptoTicker.setText(tweet.get("cryptoTicker"))

        self.tweetStream.ui.tweetStreamScrollAreaContents.layout().addWidget(tweetWidget)

    def _onInfluencerFollowed(self, twitterHandle: str) -> None:
        influencerWidget = InfluencerWidget()
        influencerWidget.ui.twitterHandle.setText(twitterHandle)
        self.tweetStream.ui.influencers.layout().addWidget(influencerWidget)

    def _onCryptoPriceUpdated(self, historic_data):
        self.linePlot.updatePlot(historic_data)

    def _onInfluencerUnFollowed(self, twitterHandle: str) -> None:
        pass

    def _onAggregateScoreUpdated(self, score) -> None:
        self.pieChart.updatePlot(score)

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
        settings: QSettings = cast(AppController, self.controller).settings
        settings.setValue("window size", self.size())
        settings.setValue("window position", self.pos())
        cast(AppController, self.controller).tearDown()
        event.accept()

    # endregion
