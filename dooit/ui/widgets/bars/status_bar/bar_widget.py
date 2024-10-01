from collections.abc import Callable
from rich.text import TextType
from typing import Optional


class StatusBarWidget:
    def __init__(
        self, func: Callable[..., TextType], width: Optional[int] = None
    ) -> None:
        self.func = func
        self.width = width
        self.value = self.calculate()

    def calculate(self) -> TextType:
        self.value = self.func()
        return self.value

    def get_value(self):
        return self.value
