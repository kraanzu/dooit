from typing import Callable
from rich.console import RenderableType
from textual import events

from .._base import BarBase
from ...inputs._input import Input


class SearchBar(BarBase):
    def __init__(self, callback: Callable, *args, **kwargs):
        super().__init__(callback, *args, **kwargs)
        self._search = Input(value="/")
        self._search.is_editing = True

    def perform_action(self, cancel: bool):
        if cancel:
            self.callback("")

    async def handle_key(self, event: events.Key) -> bool:
        if event.key == "enter":
            self.dismiss(cancel=False)

        elif event.key == "escape":
            self.dismiss(cancel=True)

        else:
            self._search.keypress(event.key)
            filter = self._search.value[1:]
            self.callback(filter)
            self.refresh()

        return True

    def render(self) -> RenderableType:
        return self._search.draw()
