from collections.abc import Callable
from rich.text import TextType, Text
from typing import Optional


class StatusBarWidget:
    def __init__(
        self, func: Callable[..., TextType], width: Optional[int] = None
    ) -> None:
        self.func = func
        self.width = width

    @property
    def value(self) -> str:
        res = getattr(self.func, "__dooit_value", "")

        if isinstance(res, Text):
            return res.markup

        return str(res)

    def render(self) -> TextType:
        return Text.from_markup(self.value)
