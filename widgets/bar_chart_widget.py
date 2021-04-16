from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, Tuple

from PySide2.QtWidgets import QWidget, QSizePolicy, QGridLayout


class BarChartWidget(QWidget):
    # region Constructor

    def __init__(self):
        super().__init__()
        self._setupView()

    def _setupView(self):
        self._createFigure()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.canvas)

    def _createFigure(self):
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    # endregion

    def updatePlot(self, historical_data: Dict[str, Tuple[int, int]]) -> None:
        """
        Input format:
        date: (num positive tweets, num negative tweets)

        Example:
        historical_data =  {'2021-12-30': (55, 25), '2021-12-31': (32, 11)}
        """

        # dates for each data point in historical data
        labels = [key[5:] for key in historical_data.keys()]

        # get list of positive tweet totals for each day
        positive_totals = [value[0] for value in historical_data.values()]

        # get list of negative tweet totals for each day
        negative_totals = [value[1] for value in historical_data.values()]

        x = np.arange(len(historical_data))  # the label locations
        width = 0.35  # the width of the bars
        rects1 = self.ax1.bar(x - width/2, positive_totals, width, color='green', label='Positive')
        rects2 = self.ax1.bar(x + width/2, negative_totals, width, color='red', label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        max_daily_value = round(1.1* max([max(positive_totals), max(negative_totals)]), 0)
        self.ax1.set_ylim(0, max_daily_value)
        self.ax1.set_ylabel('No. Tweets')
        self.ax1.set_title('7-day Sentiment')
        self.ax1.set_xticks(x)
        self.ax1.set_xticklabels(labels, rotation = 45)
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['left'].set_visible(False)
        self.ax1.spines['bottom'].set_color('#DDDDDD')
        self.ax1.tick_params(left=False)
        self.ax1.set_axisbelow(True)
        self.ax1.yaxis.grid(True, color='#EEEEEE')
        self.ax1.xaxis.grid(False)
        self.fig.canvas.draw_idle()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""

            for rect in rects:
                height = rect.get_height()
                self.ax1.annotate('{}'.format(height),
                                  xy=(rect.get_x() + rect.get_width() / 2, height),
                                  xytext=(0, 1),  # 1 points vertical offset
                                  textcoords="offset points",
                                  ha='center', va='bottom')

        # add totals above each bar
        autolabel(rects1)
        autolabel(rects2)

        self.fig.tight_layout()
