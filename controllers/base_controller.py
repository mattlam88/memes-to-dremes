from __future__ import annotations

import abc
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.base_model import BaseModel


class BaseController(metaclass=abc.ABCMeta):
    """App controller base class."""

    def __init__(self, model):
        self._model = model

    @property
    def model(self) -> BaseModel:
        return self._model
