from collections.abc import Callable
from rich.text import TextType
from typing import Optional

from dooit.ui.events.events import DooitEvent


class StatusBarWidget:
    def __init__(
        self, func: Callable[..., TextType], width: Optional[int] = None
    ) -> None:
        self.func = func
        self.width = width
        self.value = ""

    def has_event(self, event: DooitEvent) -> bool:
        return getattr(self.func, "__dooit_event", None) == event.__class__

    def calculate(self, api,  event: DooitEvent) -> TextType:
        self.value = self.func(api, event)
        return self.value

    def get_value(self):
        return self.value
