from collections.abc import Callable
from typing import Union
from rich.text import Text, TextType
from inspect import getfullargspec as get_args


class BarWidget:
    def __init__(self, func: Union[Callable[..., TextType], TextType], delay=0) -> None:
        if not isinstance(func, Callable):
            self.func = lambda: func
        else:
            self.func = func

        self.delay = delay

    def get_value(self, **kwargs) -> Text:
        args = get_args(self.func).args
        value = self.func(**{i: kwargs[i] for i in args})
        if isinstance(value, str):
            value = Text.from_markup(value)

        return value
