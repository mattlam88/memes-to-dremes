from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide2.QtWidgets import QWidget, QSizePolicy, QGridLayout


class PieChartWidget(QWidget):
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

    def updatePlot(self, aggregate_values: tuple):
        labels = ['Positive', 'Negative']
        self.ax1.clear()
        self.ax1.pie(
            aggregate_values,
            colors=['green', 'red'],
            labels=labels,
            autopct=self.make_autopct(aggregate_values),
            startangle=45
        )
        self.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.()
        self.ax1.title.set_text('Sentiment of Today\'s Tweets')
        self.fig.canvas.draw_idle()

    def make_autopct(self, values):
        """
        Helper function for updatePlot - Decorator for autopct to display both percentage and raw values in parens
        """

        def my_autopct(pct):
            if pct > 0:
                total = sum(values)
                val = int(round(pct*total/100.0))
                return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
            else:
                return ''
        return my_autopct
