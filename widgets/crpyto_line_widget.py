from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import pandas as pd

from PySide2.QtWidgets import QWidget, QSizePolicy, QGridLayout


class LinePlotWidget(QWidget):
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
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    # endregion

    def updatePlot(self, historic_pricing: dict):
        """
        Input format:
        prices: [[timestamp, price], ... ]

        Example:
        historic_pricing = {'prices': [[1618023871411, 58760.18558489944], ... ]}
        """

        df = pd.DataFrame(historic_pricing['prices'], columns = ['time', 'price'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time', inplace=True, drop=True)
        df.plot(kind = 'line', ax=self.ax1, xlabel='date', ylabel='price (USD)', x_compat=True)
        self.ax1.get_legend().remove()
        self.ax1.set_title('Crypto Price Tracker')

        # Create custom ticks using matplotlib date tick locator and formatter
        self.ax1.xaxis.set_major_locator(mdates.DayLocator())
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        self.fig.canvas.draw_idle()
