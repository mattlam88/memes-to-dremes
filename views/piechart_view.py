from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QSizePolicy, QComboBox, QLabel, QGridLayout

from views.base_plot_view import BasePlotView

class PieChartView(QWidget):
    def __init__(self, aggregate_values: tuple):
        super().__init__()
        self._setupView()
        self._updatePlot(aggregate_values)

    def _setupView(self):
        self._createFigure()

    def _createFigure(self):
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    def _updatePlot(self, aggregate_values: tuple):
        labels = ['Positive', 'Negative']
        self.ax1.clear()
        self.ax1.pie(aggregate_values, labels=labels, autopct= make_autopct(aggregate_values), startangle=90)
        self.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.()
        self.ax1.title.set_text('Sentiment of Today\'s Tweets')
        self.fig.canvas.draw_idle()

        def make_autopct(values):
            ''' helper function for _updatePlot - Decorator for autopct to display both percentage and raw values in parens '''
            def my_autopct(pct):
                if pct > 0:
                    total = sum(values)
                    val = int(round(pct*total/100.0))
                    return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
                else:
                    return ''
            return my_autopct