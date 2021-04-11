from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QSizePolicy, QComboBox, QLabel, QGridLayout
import seaborn as sns


class DemoPlotWidget(QWidget):
    tips = sns.load_dataset("tips")

    def __init__(self):
        super().__init__()

        self._setupView()
        self._updatePlot()
        self._connectSignals()

    def _setupView(self):
        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["sex", "time", "smoker"])
        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["sex", "time", "smoker", "day"])
        self.dropdown2.setCurrentIndex(2)

        self._createFigure()

        self.layout = QGridLayout(self)
        self.layout.addWidget(QLabel("Select category for subplots"))
        self.layout.addWidget(self.dropdown1)
        self.layout.addWidget(QLabel("Select category for markers"))
        self.layout.addWidget(self.dropdown2)
        self.layout.addWidget(self.canvas)

        self.label = QLabel("A plot:")

    def _createFigure(self):
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122, sharex=self.ax1, sharey=self.ax1)
        self.axes = [self.ax1, self.ax2]

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    def _connectSignals(self):
        self.dropdown1.currentIndexChanged.connect(self._updatePlot)
        self.dropdown2.currentIndexChanged.connect(self._updatePlot)

    def _updatePlot(self):
        colors = ["b", "r", "g", "y", "k", "c"]
        self.ax1.clear()
        self.ax2.clear()

        cat1 = self.dropdown1.currentText()
        cat2 = self.dropdown2.currentText()

        for i, value in enumerate(self.tips[cat1].unique().to_numpy()):
            df = self.tips.loc[self.tips[cat1] == value]
            self.axes[i].set_title(cat1 + ": " + value)
            for j, value2 in enumerate(df[cat2].unique().to_numpy()):
                df.loc[self.tips[cat2] == value2].plot(
                    kind="scatter", x="total_bill", y="tip", ax=self.axes[i], c=colors[j], label=value2
                )
        self.axes[i].legend()
        self.fig.canvas.draw_idle()
