from collections.abc import Callable
from rich.text import TextType
from typing import TYPE_CHECKING, Optional
from dooit.ui.events.events import DooitEvent

if TYPE_CHECKING:
    from dooit.ui.api.dooit_api import DooitAPI


class StatusBarWidget:
    def __init__(
        self, func: Callable[..., TextType], width: Optional[int] = None
    ) -> None:
        self.func = func
        self.width = width
        self.value = ""

    def has_event(self, event: DooitEvent) -> bool:
        from dooit.ui.api.events import DOOIT_EVENT_ATTR

        return event.__class__ in getattr(self.func, DOOIT_EVENT_ATTR, [])

    def calculate(self, api: "DooitAPI", event: DooitEvent) -> TextType:
        self.value = self.func(api, event)
        return self.value

    def render(self) -> TextType:
        return self.value
