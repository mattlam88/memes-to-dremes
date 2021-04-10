import abc

from views.base_view import BaseView


class BasePlotView(BaseView):
    """Stats figure base view."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (super().__subclasshook__(cls) and
                hasattr(subclass, "_setupView") and callable(subclass._setupView) and
                hasattr(subclass, "_updatePlot") and callable(subclass._updatePlot))

    def __init__(self, model, controller):
        super().__init__(self, model, controller)

        self._setupView()

        # set plot to initial data so its not blank
        self._updatePlot()

    @abc.abstractmethod
    def _setupView(self):
        pass

    @abc.abstractmethod
    def _updatePlot(self):
        pass
