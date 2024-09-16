from collections.abc import Callable
from typing import Any, Generic, TypeVar
from dooit.api.model import DooitModel
from rich.text import TextType
from ._input import Input
from ._cacher import input_cache

ModelType = TypeVar("ModelType", bound=DooitModel)


def max_width_cache(func):

    def wrapper(obj: "SimpleInput"):
        key = [obj.model.uuid, obj._property, obj.model_value]
        cache = input_cache.get(*key)

        if cache:
            return cache

        res = func(obj)
        key += [res]
        input_cache.set(*key)

        return res

    return wrapper


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
    def model_value(self) -> Any:
        return getattr(self.model, self._property)

    @model_value.setter
    def model_value(self, value: str) -> None:
        return setattr(self.model, self._property, value)

    @max_width_cache
    def get_max_width(self) -> int:
        return max(
            len(self.value),
            len(self.render()),
        )

    def _typecast_value(self, value: str) -> Any:
        return value

    def reset(self) -> str:
        self._cursor_pos = len(self.value)
        return self.value

    def stop_edit(self, cancel: bool = False) -> None:
        super().stop_edit()

        if not cancel:
            self.model_value = self._typecast_value(self.value)
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
        if self.is_editing:
            return super().render()

        raw = self.model_value
        for formatter in self.formatters:
            raw = formatter(raw, self.model)

        return str(raw)
