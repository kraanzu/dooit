from collections.abc import Callable
from typing import Generic, TypeVar
from dooit.api.model import DooitModel
from rich.text import TextType
from ._input import Input

ModelType = TypeVar("ModelType", bound=DooitModel)


class SimpleInput(Input, Generic[ModelType]):
    """
    A simple single line Text Input widget
    """

    _cursor_pos: int = 0
    _cursor: str = "|"

    def __init__(self, model: ModelType) -> None:
        super().__init__()

        self.model = model
        self.formatters = set()
        self.reset()

    def add_formatter(self, formatter: Callable[[str], TextType]):
        self.formatters.add(formatter)

    @property
    def _property(self) -> str:
        return self.__class__.__name__.lower()

    @property
    def model_value(self) -> str:
        return getattr(self.model, self._property) or ""

    def reset(self) -> str:
        self.value = str(self.model_value)
        self._cursor_pos = len(self.value)
        return self.value

    def stop_edit(self, cancel: bool = False) -> None:
        super().stop_edit()

        if not cancel:
            setattr(self.model, self._property, self.value)
            self.model.save()
        else:
            self.reset()

    def cancel_edit(self) -> None:
        return self.stop_edit(cancel=True)

    def keypress(self, key: str) -> None:
        super().keypress(key)

        if key == "escape":
            self.stop_edit()

    def render(self) -> str:
        raw = super().render()
        if self.is_editing:
            return raw

        for formatter in self.formatters:
            raw = formatter(raw, self.model)

        return raw
