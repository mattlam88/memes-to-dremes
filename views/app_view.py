from __future__ import annotations

from typing import cast, TYPE_CHECKING

from PySide2.QtWidgets import QMainWindow, QVBoxLayout

from controllers.app_controller import AppController
from models.app_model import AppModel
from views.base_view import BaseView
from views.app_ui import Ui_App

if TYPE_CHECKING:
    from controllers.base_controller import BaseController
    from models.base_model import BaseModel


from widgets.bar_chart_widget import BarChartWidget
from widgets.demo_plot_widget import DemoPlotWidget
from widgets.pie_chart_widget import PieChartWidget
from widgets.tweet_stream_widget import TweetStreamWidget


class AppViewMeta(type(QMainWindow), type(BaseView)):
    pass


class AppView(QMainWindow, BaseView, metaclass=AppViewMeta):
    """Main app window that displays crypto dashboard."""

    def __init__(self, model: BaseModel, controller: BaseController) -> None:
        QMainWindow.__init__(self)
        BaseView.__init__(self, model, controller, Ui_App())

        """
        self.ui.plot = PlotView()
        self.ui.plot.setObjectName(u"plot")
        self.ui.gridLayout.addWidget(self.ui.plot, 1, 0, 2, 2)
        """
        self._influencers = list()
        self._tweets = list()
        self._tweetStream = TweetStreamWidget()
        self._barChart = BarChartWidget({"2021-10-11": (33, 22), "2021-10-12": (31, 4),"2021-10-13": (33, 22), "2021-10-14": (31, 4), "2021-10-15": (33, 22), "2021-10-16": (31, 4)})
        self._pieChart = PieChartWidget((10, 10))

        self._updateUI()

    def _connectSignals(self) -> None:
        pass
        """
        self.ui.pushButton_5.clicked.connect(self._onBtnClicked)
        cast(AppModel, self.model).btnTextChanged.connect(self._onBtnTextChanged)
        """

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

    """
    def _updateUI(self) -> None:
        cast(AppController, self.controller).updateTweetHistory()
    """

    def _onBtnClicked(self) -> None:
        cast(AppController, self.controller).changeBtnText("What's up?")

    def _onBtnTextChanged(self) -> None:
        self.ui.pushButton_5.setText(cast(AppModel, self.model).btnText)
