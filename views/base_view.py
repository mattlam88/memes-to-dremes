from __future__ import annotations

import abc
from typing import Any, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.base_controller import BaseController
    from models.base_model import BaseModel


class BaseView(metaclass=abc.ABCMeta):
    """App view base class."""

    # region Properties

    @property
    def model(self) -> Type[BaseModel]:
        return self._model

    @property
    def controller(self) -> Type[BaseController]:
        return self._controller

    @property
    def ui(self) -> Optional[Any]:
        return self._ui

    # endregion

    # region Constructor

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return (hasattr(subclass, "_connectSignals") and callable(subclass._connectSignals) or
                NotImplemented)

    def __init__(self, model, controller, ui=None) -> None:
        super().__init__()

        self._model: Type[BaseModel] = model
        self._controller: Type[BaseController] = controller
        self._ui = ui

        if self.ui is not None:
            self.ui.setupUi(self)

    # endregion

    @abc.abstractmethod
    def _connectSignals(self) -> None:
        raise NotImplementedError
